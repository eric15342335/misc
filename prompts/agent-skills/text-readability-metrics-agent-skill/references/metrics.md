# Metric definitions

These definitions are normative for this skill version.

## Readability and counts

`textstat==0.7.13` supplies word, sentence, and syllable counts for its readability formulas. The analyzer also recomputes FRE and FKGL directly from those counts and requires agreement with `textstat`.

- Average sentence length (ASL) = textstat words / textstat sentences.
- Average syllables per word (ASW) = textstat syllables / textstat words.
- Flesch Reading Ease = `206.835 - 1.015*ASL - 84.6*ASW`.
- Flesch-Kincaid Grade Level = `0.39*ASL + 11.8*ASW - 15.59`.
- Gunning Fog, SMOG, ARI, Coleman-Liau, Dale-Chall, and Linsear Write use the implementation in the pinned textstat release.

Do not claim that a grade score is a precise educational prerequisite. It is an index derived from surface features.

## Lexical diversity

The skill tokenizes lexical-diversity inputs with `lexical_diversity.lex_div.tokenize`.

- TTR = unique token types / token count. It is strongly length-sensitive.
- MATTR-50 = moving-average TTR with a fixed 50-token window.
- MSTTR-50 = mean TTR over non-overlapping 50-token segments.
- HD-D = hypergeometric-distribution lexical diversity from the pinned library.
- MTLD = Measure of Textual Lexical Diversity from the pinned library.

Do not assign school-grade labels to these metrics. They describe lexical variety, not educational level.

## POS and lexical density

spaCy `en_core_web_sm==3.8.0` provides tokenization, POS tags, dependency labels, morphology, and sentence boundaries.

POS percentages use all non-space, non-punctuation spaCy tokens as the denominator.

Lexical density is defined here as:

`(NOUN + PROPN + VERB + ADJ + ADV tokens) / all non-space, non-punctuation tokens * 100`.

Different lexical-density traditions use different content-word sets, so always state this definition when comparing against external work.

## Mean dependency distance

For every spaCy token that is not a root, punctuation, or whitespace token, and whose syntactic head is not punctuation/whitespace, dependency distance is `abs(token.i - token.head.i)`. Mean dependency distance is the arithmetic mean of those distances.

This is parser/model-dependent. Do not present a universal school-grade cutoff for it.

## Sentence variation

Sentence length is the number of non-space, non-punctuation spaCy tokens in each non-empty spaCy sentence.

- mean = arithmetic mean;
- SD = population standard deviation (`statistics.pstdev`);
- CV = population SD / mean.

CV is dimensionless and is useful when comparing variation across texts with different mean sentence lengths.

## Passive voice

The primary parser signals are spaCy dependencies `auxpass`, `nsubjpass`, `csubjpass`, or a morphology feature containing `Voice=Pass`. A secondary deterministic rule adds a VBN VERB/AUX predicate with a `be` or `get` auxiliary child. Detected predicate token indices are deduplicated.

The skill reports two percentages:

1. Passive-sentence percentage = spaCy sentences containing at least one passive predicate / all spaCy sentences * 100.
2. Passive predicate/clause percentage = detected passive predicate heads / verbal clause heads * 100, where verbal clause heads are VERB/AUX tokens excluding dependency labels `aux`, `auxpass`, and `cop`.

These are operational definitions for this skill, not universal definitions of passive-voice percentage.
