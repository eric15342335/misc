---
name: text-readability-metrics
description: Set up a pinned Python analysis environment and calculate reproducible English text metrics, including Flesch/FKGL, Fog, SMOG, ARI, Coleman-Liau, Dale-Chall, Linsear Write, lexical diversity, POS rates, dependency distance, sentence variation, and passive voice. Use when a user asks to calculate, audit, reproduce, compare, or standardize readability, stylometry, syntax, passive voice, or text-complexity measurements on text or text files.
compatibility: Requires CPython 3.11 and filesystem/shell execution. First-time environment bootstrap requires package-network access; analysis itself is offline. Parser metrics use spaCy en_core_web_sm 3.8.0.
---

# Text Readability Metrics

Use this skill for deterministic, auditable measurement of English text. Prefer the bundled scripts over reimplementing formulas or parser logic in an ad hoc command.

## Workflow

1. Preserve the user's input exactly unless they explicitly request preprocessing.
2. Work in an isolated environment when one is available. Do not rely on unknown global package versions.
3. From this skill directory, verify or create the pinned runtime:

   ```bash
   python3 scripts/bootstrap.py --venv .venv
   ```

   The command is non-interactive. It prints JSON containing the interpreter path and installed versions. If the active environment is already pinned, use `--check-only` instead of reinstalling.

4. Analyze the input with the interpreter reported by the bootstrap script:

   ```bash
   .venv/bin/python scripts/analyze_text.py input.txt --output metrics.json --pretty
   ```

   On Windows, use `.venv\\Scripts\\python.exe`.

5. Validate the result before reporting it:

   ```bash
   .venv/bin/python scripts/validate_output.py metrics.json
   ```

6. If validation fails, fix the environment or input handling and rerun the analysis. Do not report an unvalidated result as reproducible.
7. Report the metric value together with its denominator or operational definition when the metric is not self-explanatory. In particular, distinguish passive-sentence percentage from passive-predicate/clause percentage.
8. Record the input SHA-256, preprocessing mode, parser/model version, package versions, and sentence counts with the result when reproducibility matters.

## Input modes

- `--mode exact` is the default and analyzes every character in the supplied text. Use it for verbatim or forensic requests.
- `--mode prose` applies the deterministic rules documented in `references/reproducibility.md`. Use it only when the user asks to exclude document-format artifacts such as Markdown headings, tables, or fenced code.
- For comparative work, use the same mode and software versions for every document.

## Core outputs

The analyzer emits JSON and includes:

- raw counts and SHA-256 hashes;
- Flesch Reading Ease and Flesch-Kincaid Grade Level, plus manual formula cross-checks;
- Gunning Fog, SMOG, Automated Readability Index, Coleman-Liau, Dale-Chall, and Linsear Write;
- TTR, MATTR-50, MSTTR-50, HD-D, and MTLD;
- spaCy sentence/token counts and normalized POS frequencies;
- lexical density under the explicitly stated content-POS definition;
- mean dependency distance and dependency-arc count;
- sentence-length mean, population SD, and coefficient of variation;
- passive-bearing sentence count/percentage and passive predicate/clause percentage;
- passive predicates and matching sentences for auditability;
- exact library/model versions used.

Read `references/metrics.md` when interpreting definitions, denominators, or limitations. Read `references/reproducibility.md` when designing comparisons, publishing methods, or explaining why two tools disagree.

## Gotchas

- Readability formulas are not interchangeable. Do not average grade estimates unless the user explicitly asks for a defined aggregation method.
- `textstat` and spaCy can segment the same input into different sentence counts. Keep both counts and use the denominator named by each metric.
- Raw TTR is length-sensitive. Prefer MATTR-50, MTLD, and HD-D for cross-document lexical-diversity comparisons.
- Passive voice has no universal percentage denominator. This skill reports both sentence-based and predicate/clause-based forms.
- Tables, formulas, headings, abbreviations, decimal points, and bullets can affect tokenization and sentence segmentation. Do not silently remove them.
- Parser-derived metrics are reproducible only under the same parser and model version; they are not mathematically parser-independent.
- A readability score estimates surface text difficulty, not comprehension, truth, writing quality, or authorship.

## Quality gate

Before finalizing a metric result:

- [ ] Input mode is explicit.
- [ ] Input SHA-256 is present.
- [ ] Runtime versions match the lock file.
- [ ] Manual FRE/FKGL cross-checks match the library values.
- [ ] Parser/model identity is recorded for parser-derived metrics.
- [ ] Passive voice denominator is named.
- [ ] `scripts/validate_output.py` passes.

