#!/usr/bin/env python3
"""Compute a reproducible panel of English readability and stylometric metrics."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

import spacy
import textstat
from lexical_diversity import lex_div as ld
from spacy.tokens import Doc, Span, Token

SCHEMA_VERSION = "1.0"
DEFAULT_MODEL = "en_core_web_sm"
CONTENT_POS = frozenset({"NOUN", "PROPN", "VERB", "ADJ", "ADV"})
PASSIVE_DEPS = frozenset({"auxpass", "nsubjpass", "csubjpass"})
VERBAL_AUX_DEPS = frozenset({"aux", "auxpass", "cop"})
BE_GET_LEMMAS = frozenset({"be", "get"})


def sha256_text(text: str) -> str:
    """Return the SHA-256 hex digest of UTF-8 encoded text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def preprocess_text(text: str, mode: str) -> str:
    """Apply the skill's deterministic preprocessing policy."""
    if mode == "exact":
        return text
    if mode != "prose":
        raise ValueError(f"unsupported mode: {mode!r}; expected 'exact' or 'prose'")

    output: list[str] = []
    in_fence = False
    fence_marker: str | None = None

    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        fence_match = re.match(r"^(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        if re.match(r"^#{1,6}\s+", stripped):
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            continue

        newline = "\n" if line.endswith("\n") else ""
        body = line[:-1] if newline else line
        body = re.sub(r"^(\s*)[-*+]\s+", r"\1", body)
        output.append(body + newline)

    return "".join(output)


def distribution_version(distribution: str) -> str:
    """Return a distribution version, or a clear sentinel if metadata is missing."""
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "not-installed"


def runtime_versions(model_name: str) -> dict[str, str]:
    """Return versions that materially affect metric output."""
    return {
        "python": ".".join(map(str, sys.version_info[:3])),
        "textstat": distribution_version("textstat"),
        "spacy": distribution_version("spacy"),
        "lexical-diversity": distribution_version("lexical-diversity"),
        "setuptools": distribution_version("setuptools"),
        "spacy-model": distribution_version(model_name.replace("_", "-")),
        "spacy-model-name": model_name,
    }


def _nonpunct_tokens(doc: Doc) -> list[Token]:
    return [token for token in doc if not token.is_space and not token.is_punct]


def _passive_heads(doc: Doc) -> set[int]:
    heads: set[int] = set()
    for token in doc:
        passive_signal = token.dep_ in PASSIVE_DEPS or "Pass" in token.morph.to_dict().get(
            "Voice", ""
        )
        if passive_signal:
            head = token.head if token.dep_ in PASSIVE_DEPS else token
            heads.add(head.i)

    for token in doc:
        if token.tag_ != "VBN" or token.pos_ not in {"VERB", "AUX"}:
            continue
        has_passive_aux = any(
            child.pos_ == "AUX" and child.lemma_.lower() in BE_GET_LEMMAS
            for child in token.children
        )
        if has_passive_aux:
            heads.add(token.i)
    return heads


def _passive_sentence_records(
    doc: Doc, sentences: list[Span], passive_heads: set[int]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for sentence_index, sentence in enumerate(sentences, start=1):
        heads = [doc[index] for index in passive_heads if sentence.start <= index < sentence.end]
        if not heads:
            continue
        records.append(
            {
                "sentence_index": sentence_index,
                "predicate_indices": sorted({token.i for token in heads}),
                "predicates": sorted({token.text for token in heads}),
                "text": sentence.text.strip().replace("\n", " "),
            }
        )
    return records


def _sentence_lengths(sentences: list[Span]) -> list[int]:
    lengths: list[int] = []
    for sentence in sentences:
        length = sum(1 for token in sentence if not token.is_space and not token.is_punct)
        if length:
            lengths.append(length)
    return lengths


def _dependency_distances(doc: Doc) -> list[int]:
    distances: list[int] = []
    for token in doc:
        if token.is_space or token.is_punct or token.dep_ == "ROOT" or token.head == token:
            continue
        if token.head.is_space or token.head.is_punct:
            continue
        distances.append(abs(token.i - token.head.i))
    return distances


def analyze_text(
    text: str, *, mode: str = "exact", model_name: str = DEFAULT_MODEL
) -> dict[str, Any]:
    """Analyze text and return the complete metrics payload."""
    analyzed_text = preprocess_text(text, mode)
    if not analyzed_text.strip():
        raise ValueError("analyzed text is empty after preprocessing")

    textstat.set_lang("en_US")
    words = textstat.lexicon_count(analyzed_text, removepunct=True)
    sentences_textstat = textstat.sentence_count(analyzed_text)
    syllables = textstat.syllable_count(analyzed_text)
    if words <= 0 or sentences_textstat <= 0:
        raise ValueError("textstat did not detect at least one word and one sentence")

    asl = words / sentences_textstat
    asw = syllables / words
    fre_manual = 206.835 - (1.015 * asl) - (84.6 * asw)
    fkgl_manual = (0.39 * asl) + (11.8 * asw) - 15.59

    lexical_tokens = ld.tokenize(analyzed_text)
    if not lexical_tokens:
        raise ValueError("lexical-diversity tokenizer produced no tokens")

    try:
        nlp = spacy.load(model_name)
    except OSError as exc:
        raise RuntimeError(
            f"spaCy model {model_name!r} is unavailable; run scripts/bootstrap.py first"
        ) from exc
    nlp.max_length = max(nlp.max_length, len(analyzed_text) + 100)
    doc = nlp(analyzed_text)
    spacy_sentences = list(doc.sents)
    if not spacy_sentences:
        raise ValueError("spaCy produced no sentences")

    eligible_tokens = _nonpunct_tokens(doc)
    if not eligible_tokens:
        raise ValueError("spaCy produced no non-punctuation tokens")

    pos_counts: dict[str, int] = {}
    for token in eligible_tokens:
        pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
    pos_percent = {
        pos: (100.0 * count / len(eligible_tokens)) for pos, count in sorted(pos_counts.items())
    }
    content_count = sum(1 for token in eligible_tokens if token.pos_ in CONTENT_POS)

    dependency_distances = _dependency_distances(doc)
    sentence_lengths = _sentence_lengths(spacy_sentences)
    if not dependency_distances or not sentence_lengths:
        raise ValueError("parser output is insufficient for syntactic metrics")

    passive_heads = _passive_heads(doc)
    passive_sentences = _passive_sentence_records(doc, spacy_sentences, passive_heads)
    verbal_clause_heads = [
        token
        for token in doc
        if token.pos_ in {"VERB", "AUX"} and token.dep_ not in VERBAL_AUX_DEPS
    ]

    passive_sentence_pct = 100.0 * len(passive_sentences) / len(spacy_sentences)
    passive_clause_pct = (
        100.0 * len(passive_heads) / len(verbal_clause_heads) if verbal_clause_heads else 0.0
    )
    sentence_mean = statistics.mean(sentence_lengths)
    sentence_sd = statistics.pstdev(sentence_lengths)

    return {
        "schema_version": SCHEMA_VERSION,
        "input": {
            "mode": mode,
            "raw_chars": len(text),
            "analyzed_chars": len(analyzed_text),
            "raw_sha256": sha256_text(text),
            "analyzed_sha256": sha256_text(analyzed_text),
        },
        "versions": runtime_versions(model_name),
        "counts": {
            "words_textstat": words,
            "sentences_textstat": sentences_textstat,
            "syllables_textstat": syllables,
            "spacy_sentences": len(spacy_sentences),
            "spacy_tokens_nonpunct": len(eligible_tokens),
            "lexical_tokens": len(lexical_tokens),
            "lexical_types": len(set(lexical_tokens)),
        },
        "readability": {
            "average_sentence_length_textstat": asl,
            "average_syllables_per_word_textstat": asw,
            "flesch_reading_ease": textstat.flesch_reading_ease(analyzed_text),
            "flesch_reading_ease_manual": fre_manual,
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(analyzed_text),
            "flesch_kincaid_grade_manual": fkgl_manual,
            "gunning_fog": textstat.gunning_fog(analyzed_text),
            "smog_index": textstat.smog_index(analyzed_text),
            "automated_readability_index": textstat.automated_readability_index(analyzed_text),
            "coleman_liau_index": textstat.coleman_liau_index(analyzed_text),
            "dale_chall_readability": textstat.dale_chall_readability_score(analyzed_text),
            "linsear_write": textstat.linsear_write_formula(analyzed_text),
        },
        "lexical_diversity": {
            "ttr": ld.ttr(lexical_tokens),
            "mattr_50": ld.mattr(lexical_tokens, window_length=50),
            "msttr_50": ld.msttr(lexical_tokens, window_length=50),
            "hdd": ld.hdd(lexical_tokens),
            "mtld": ld.mtld(lexical_tokens),
        },
        "syntax": {
            "pos_percent_nonpunct": pos_percent,
            "lexical_density_content_pos_pct": 100.0 * content_count / len(eligible_tokens),
            "lexical_density_content_pos": sorted(CONTENT_POS),
            "mean_dependency_distance": statistics.mean(dependency_distances),
            "dependency_arc_count": len(dependency_distances),
            "sentence_length_mean_spacy_nonpunct": sentence_mean,
            "sentence_length_population_sd_spacy_nonpunct": sentence_sd,
            "sentence_length_cv_spacy_nonpunct": sentence_sd / sentence_mean,
        },
        "passive_voice": {
            "passive_sentence_count": len(passive_sentences),
            "passive_sentence_denominator": len(spacy_sentences),
            "passive_sentence_pct": passive_sentence_pct,
            "passive_predicate_count": len(passive_heads),
            "verbal_clause_head_denominator": len(verbal_clause_heads),
            "passive_predicate_clause_pct": passive_clause_pct,
            "passive_sentences": passive_sentences,
        },
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute reproducible English readability, lexical, syntax, and passive-voice metrics."
        )
    )
    parser.add_argument(
        "input",
        help="UTF-8 text file path, or '-' to read UTF-8 text from stdin.",
    )
    parser.add_argument(
        "--mode",
        choices=("exact", "prose"),
        default="exact",
        help="Preprocessing mode (default: exact).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"spaCy model name (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument("--output", type=Path, help="Write JSON to this file instead of stdout.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON with indentation.")
    return parser.parse_args(argv)


def read_input(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()
    path = Path(path_arg)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"input file not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise UnicodeError(f"input is not valid UTF-8: {path}") from exc


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload = analyze_text(read_input(args.input), mode=args.mode, model_name=args.model)
    except (OSError, RuntimeError, UnicodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    indent = 2 if args.pretty else None
    serialized = json.dumps(payload, indent=indent, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    else:
        sys.stdout.write(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
