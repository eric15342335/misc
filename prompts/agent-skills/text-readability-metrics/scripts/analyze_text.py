#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = [
#   "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
#   "lexical-diversity==0.1.1",
#   "pydantic==2.13.4",
#   "setuptools==80.10.2",
#   "spacy==3.8.16",
#   "textstat==0.7.13",
#   "typer==0.26.3",
# ]
# ///
"""Measure English readability, lexical diversity, syntax, and passive voice."""

from __future__ import annotations

import json
import re
import statistics
import sys
import warnings as py_warnings
from collections import Counter
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from pydantic import BaseModel
from spacy import load
from spacy.tokens import Doc, Span, Token
from textstat.textstat import textstat  # type: ignore[import-untyped]

with py_warnings.catch_warnings():
    py_warnings.filterwarnings(
        "ignore",
        message="pkg_resources is deprecated as an API.*",
        category=UserWarning,
    )
    from lexical_diversity import lex_div as ld  # type: ignore[import-untyped]

MODEL_NAME = "en_core_web_sm"
CONTENT_POS = frozenset({"NOUN", "PROPN", "VERB", "ADJ", "ADV"})
PASSIVE_DEPS = frozenset({"auxpass", "nsubjpass", "csubjpass"})
VERBAL_AUX_DEPS = frozenset({"aux", "auxpass", "cop"})
BE_GET_LEMMAS = frozenset({"be", "get"})


class Mode(StrEnum):
    """Text selection mode."""

    EXACT = "exact"
    PROSE = "prose"


class InputMetrics(BaseModel):
    """Input size and selection details."""

    analyzed_chars: int
    mode: Mode
    raw_chars: int


class CountMetrics(BaseModel):
    """Counts from each analysis engine."""

    lexical_tokens: int
    lexical_types: int
    sentences_textstat: int
    spacy_sentences: int
    spacy_tokens_nonpunct: int
    syllables_textstat: int
    words_textstat: int


class ReadabilityMetrics(BaseModel):
    """Common readability scores."""

    automated_readability_index: float
    coleman_liau_index: float
    dale_chall_readability: float
    flesch_kincaid_grade: float
    flesch_reading_ease: float
    gunning_fog: float
    linsear_write: float
    smog_index: float


class LexicalMetrics(BaseModel):
    """Lexical diversity scores."""

    hdd: float | None
    mattr_50: float | None
    msttr_50: float | None
    mtld: float | None
    ttr: float


class SyntaxMetrics(BaseModel):
    """Part-of-speech, dependency, and sentence metrics."""

    dependency_arc_count: int
    lexical_density_content_pos_pct: float
    mean_dependency_distance: float | None
    pos_percent_nonpunct: dict[str, float]
    sentence_length_cv_spacy_nonpunct: float
    sentence_length_mean_spacy_nonpunct: float
    sentence_length_population_sd_spacy_nonpunct: float


class PassiveSentence(BaseModel):
    """One sentence with passive voice."""

    predicate_indices: list[int]
    predicates: list[str]
    sentence_index: int
    text: str


class PassiveMetrics(BaseModel):
    """Passive voice counts and rates."""

    passive_predicate_clause_pct: float | None
    passive_predicate_count: int
    passive_sentence_count: int
    passive_sentence_denominator: int
    passive_sentence_pct: float
    passive_sentences: list[PassiveSentence]
    verbal_clause_head_denominator: int


class AnalysisResult(BaseModel):
    """Complete analysis result."""

    counts: CountMetrics
    input: InputMetrics
    lexical_diversity: LexicalMetrics
    passive_voice: PassiveMetrics
    readability: ReadabilityMetrics
    syntax: SyntaxMetrics
    warnings: list[str]

    def render(self, *, pretty: bool) -> str:
        """Serialize with stable key order and UTF-8 text."""
        return (
            json.dumps(
                self.model_dump(mode="json"),
                indent=2 if pretty else None,
                sort_keys=True,
                ensure_ascii=False,
            )
            + "\n"
        )


def preprocess_text(text: str, mode: Mode) -> str:
    """Apply the selected text rules."""
    if mode is Mode.EXACT:
        return text

    output: list[str] = []
    in_fence = False
    fence_marker: str | None = None
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        fence_match = re.match(r"^(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence, fence_marker = False, None
            continue
        if in_fence or re.match(r"^#{1,6}\s+", stripped):
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            continue
        newline = "\n" if line.endswith("\n") else ""
        body = line[:-1] if newline else line
        output.append(re.sub(r"^(\s*)[-*+]\s+", r"\1", body) + newline)
    return "".join(output)


def _dependency_distances(doc: Doc) -> list[int]:
    return [
        abs(token.i - token.head.i)
        for token in doc
        if not token.is_space
        and not token.is_punct
        and token.dep_ != "ROOT"
        and token.head != token
        and not token.head.is_space
        and not token.head.is_punct
    ]


def _passive_heads(doc: Doc) -> set[int]:
    heads = {
        (token.head if token.dep_ in PASSIVE_DEPS else token).i
        for token in doc
        if token.dep_ in PASSIVE_DEPS
        or "Pass" in token.morph.to_dict().get("Voice", "")
    }
    heads.update(
        token.i
        for token in doc
        if token.tag_ == "VBN"
        and token.pos_ in {"VERB", "AUX"}
        and any(
            child.pos_ == "AUX" and child.lemma_.lower() in BE_GET_LEMMAS
            for child in token.children
        )
    )
    return heads


def _passive_sentences(
    doc: Doc, sentences: list[Span], passive_heads: set[int]
) -> list[PassiveSentence]:
    records: list[PassiveSentence] = []
    for sentence_index, sentence in enumerate(sentences, start=1):
        heads = [
            doc[index]
            for index in passive_heads
            if sentence.start <= index < sentence.end
        ]
        if heads:
            records.append(
                PassiveSentence(
                    sentence_index=sentence_index,
                    predicate_indices=sorted({token.i for token in heads}),
                    predicates=sorted({token.text for token in heads}),
                    text=sentence.text.strip().replace("\n", " "),
                )
            )
    return records


def _lexical_metrics(tokens: list[str]) -> tuple[LexicalMetrics, list[str]]:
    count = len(tokens)
    notes = [
        message
        for threshold, message in (
            (50, "MATTR-50 and MSTTR-50 need at least 50 lexical tokens."),
            (42, "HD-D needs at least 42 lexical tokens."),
            (10, "MTLD needs at least 10 lexical tokens."),
        )
        if count < threshold
    ]
    return (
        LexicalMetrics(
            ttr=ld.ttr(tokens),
            mattr_50=ld.mattr(tokens, window_length=50) if count >= 50 else None,
            msttr_50=ld.msttr(tokens, window_length=50) if count >= 50 else None,
            hdd=ld.hdd(tokens) if count >= 42 else None,
            mtld=ld.mtld(tokens) if count >= 10 else None,
        ),
        notes,
    )


def _textstat_metrics(text: str) -> tuple[int, int, int, ReadabilityMetrics]:
    textstat.set_lang("en_US")
    words = textstat.lexicon_count(text, removepunct=True)
    sentences = textstat.sentence_count(text)
    syllables = textstat.syllable_count(text)
    if words <= 0 or sentences <= 0:
        raise ValueError("textstat needs at least one word and one sentence")
    return (
        words,
        sentences,
        syllables,
        ReadabilityMetrics(
            flesch_reading_ease=textstat.flesch_reading_ease(text),
            flesch_kincaid_grade=textstat.flesch_kincaid_grade(text),
            gunning_fog=textstat.gunning_fog(text),
            smog_index=textstat.smog_index(text),
            automated_readability_index=textstat.automated_readability_index(text),
            coleman_liau_index=textstat.coleman_liau_index(text),
            dale_chall_readability=textstat.dale_chall_readability_score(text),
            linsear_write=textstat.linsear_write_formula(text),
        ),
    )


def _syntax_metrics(sentences: list[Span], tokens: list[Token]) -> SyntaxMetrics:
    token_count = len(tokens)
    sentence_lengths = [
        length
        for sentence in sentences
        if (
            length := sum(
                not token.is_space and not token.is_punct for token in sentence
            )
        )
    ]
    if not sentence_lengths:
        raise ValueError("spaCy found no non-empty sentence")

    pos_counts = Counter(token.pos_ for token in tokens)
    sentence_mean = statistics.mean(sentence_lengths)
    sentence_sd = statistics.pstdev(sentence_lengths)
    distances = _dependency_distances(tokens[0].doc)
    return SyntaxMetrics(
        pos_percent_nonpunct={
            pos: 100.0 * count / token_count
            for pos, count in sorted(pos_counts.items())
        },
        lexical_density_content_pos_pct=(
            100.0 * sum(token.pos_ in CONTENT_POS for token in tokens) / token_count
        ),
        mean_dependency_distance=statistics.mean(distances) if distances else None,
        dependency_arc_count=len(distances),
        sentence_length_mean_spacy_nonpunct=sentence_mean,
        sentence_length_population_sd_spacy_nonpunct=sentence_sd,
        sentence_length_cv_spacy_nonpunct=sentence_sd / sentence_mean,
    )


def _passive_metrics(
    doc: Doc, sentences: list[Span], notes: list[str]
) -> PassiveMetrics:
    passive_heads = _passive_heads(doc)
    passive_sentences = _passive_sentences(doc, sentences, passive_heads)
    clause_heads = [
        token
        for token in doc
        if token.pos_ in {"VERB", "AUX"} and token.dep_ not in VERBAL_AUX_DEPS
    ]
    predicate_rate = (
        100.0 * len(passive_heads) / len(clause_heads) if clause_heads else None
    )
    if predicate_rate is None:
        notes.append("Passive predicate rate needs at least one verbal clause head.")
    return PassiveMetrics(
        passive_sentence_count=len(passive_sentences),
        passive_sentence_denominator=len(sentences),
        passive_sentence_pct=100.0 * len(passive_sentences) / len(sentences),
        passive_predicate_count=len(passive_heads),
        verbal_clause_head_denominator=len(clause_heads),
        passive_predicate_clause_pct=predicate_rate,
        passive_sentences=passive_sentences,
    )


def _parse(text: str) -> tuple[Doc, list[Span], list[Token]]:
    nlp = load(MODEL_NAME, exclude=["ner"])
    nlp.max_length = max(nlp.max_length, len(text) + 100)
    doc = nlp(text)
    sentences = list(doc.sents)
    tokens = [token for token in doc if not token.is_space and not token.is_punct]
    if not sentences or not tokens:
        raise ValueError("spaCy found no usable English text")
    return doc, sentences, tokens


def analyze_text(text: str, *, mode: Mode = Mode.EXACT) -> AnalysisResult:
    """Analyze text and return typed metrics."""
    analyzed_text = preprocess_text(text, mode)
    if not analyzed_text.strip():
        raise ValueError("analyzed text is empty after preprocessing")

    words, textstat_sentences, syllables, readability = _textstat_metrics(analyzed_text)
    lexical_tokens = [token for token in ld.tokenize(analyzed_text) if token]
    if not lexical_tokens:
        raise ValueError("lexical analysis found no tokens")
    lexical_diversity, notes = _lexical_metrics(lexical_tokens)
    doc, sentences, tokens = _parse(analyzed_text)

    return AnalysisResult(
        input=InputMetrics(
            mode=mode, raw_chars=len(text), analyzed_chars=len(analyzed_text)
        ),
        counts=CountMetrics(
            words_textstat=words,
            sentences_textstat=textstat_sentences,
            syllables_textstat=syllables,
            spacy_sentences=len(sentences),
            spacy_tokens_nonpunct=len(tokens),
            lexical_tokens=len(lexical_tokens),
            lexical_types=len(set(lexical_tokens)),
        ),
        readability=readability,
        lexical_diversity=lexical_diversity,
        syntax=_syntax_metrics(sentences, tokens),
        passive_voice=_passive_metrics(doc, sentences, notes),
        warnings=notes,
    )


def _read_input(path_arg: str) -> str:
    return (
        sys.stdin.read()
        if path_arg == "-"
        else Path(path_arg).read_text(encoding="utf-8")
    )


def cli(
    input_path: Annotated[
        str, typer.Argument(help="UTF-8 text file path, or '-' for stdin.")
    ],
    mode: Annotated[Mode, typer.Option(help="Text selection mode.")] = Mode.EXACT,
    output: Annotated[
        Path | None, typer.Option(help="Write JSON to this file.")
    ] = None,
    pretty: Annotated[bool, typer.Option(help="Indent the JSON output.")] = False,
) -> None:
    """Measure English readability, lexical diversity, syntax, and passive voice."""
    try:
        serialized = analyze_text(_read_input(input_path), mode=mode).render(
            pretty=pretty
        )
        if output:
            output.write_text(serialized, encoding="utf-8")
        else:
            typer.echo(serialized, nl=False)
    except (OSError, UnicodeError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=2) from exc


if __name__ == "__main__":
    typer.run(cli)
