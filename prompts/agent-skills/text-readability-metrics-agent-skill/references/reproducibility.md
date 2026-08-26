# Reproducibility protocol

## Input identity

The analyzer records SHA-256 for both the raw UTF-8 input and the text actually analyzed. Preserve the source file unchanged when the user asks for verbatim measurement.

## Preprocessing modes

### exact

No text transformation. UTF-8 text is analyzed exactly as read.

### prose

The transformation is deterministic and line-oriented:

1. Remove fenced Markdown code blocks, including fence lines.
2. Remove ATX Markdown heading lines beginning with one to six `#` characters followed by whitespace.
3. Remove Markdown table rows whose stripped line begins and ends with `|`.
4. On remaining lines, remove a leading Markdown unordered-list marker (`- `, `* `, or `+ `) but keep the list-item text.
5. Preserve blank lines and all remaining characters.

The analyzer records both raw and analyzed hashes so preprocessing is auditable.

## Frozen runtime

The canonical runtime uses CPython 3.11 with every transitive dependency pinned in `requirements.lock`. The key application versions are:

- textstat 0.7.13
- spaCy 3.8.15
- en_core_web_sm 3.8.0
- lexical-diversity 0.1.1
- setuptools 79.0.1 (needed by lexical-diversity 0.1.1 at import time)

Run `scripts/bootstrap.py` to create an isolated virtual environment from the lock file. It runs `pip check` and verifies the key versions after installation.

## Sentence denominators

`textstat` and spaCy do not have to produce the same sentence segmentation. Readability formulas use the textstat sentence count because that is the library's defined input. Parser-derived metrics use the spaCy sentence count. Both are stored.

## Numeric output

JSON contains Python double-precision floating-point values without display rounding. Round only when presenting results to a human; preserve the raw JSON for audit or regression tests.

## Cross-document comparisons

Use the same:

- preprocessing mode;
- exact lock file;
- Python major/minor version where feasible;
- parser model;
- metric definitions and denominators.

If any of these change, treat the comparison as a new measurement protocol and record the change.
