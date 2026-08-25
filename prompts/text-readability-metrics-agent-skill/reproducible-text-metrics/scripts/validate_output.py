#!/usr/bin/env python3
"""Validate JSON emitted by analyze_text.py."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

EXPECTED_SCHEMA = "1.0"
EXPECTED_VERSIONS = {
    "textstat": "0.7.13",
    "spacy": "3.8.15",
    "lexical-diversity": "0.1.1",
    "spacy-model": "3.8.0",
    "setuptools": "79.0.1",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _require(mapping: dict[str, Any], key: str, path: str) -> Any:
    if key not in mapping:
        raise ValueError(f"missing required field: {path}.{key}")
    return mapping[key]


def _require_mapping(mapping: dict[str, Any], key: str, path: str) -> dict[str, Any]:
    value = _require(mapping, key, path)
    if not isinstance(value, dict):
        raise ValueError(f"expected object at {path}.{key}")
    return value


def _check_finite_numbers(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _check_finite_numbers(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _check_finite_numbers(child, f"{path}[{index}]")
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"non-finite float at {path}: {value}")


def validate(payload: dict[str, Any], *, strict_versions: bool = True) -> list[str]:
    problems: list[str] = []

    try:
        if _require(payload, "schema_version", "root") != EXPECTED_SCHEMA:
            raise ValueError(f"schema_version must be {EXPECTED_SCHEMA}")

        input_info = _require_mapping(payload, "input", "root")
        for key in ("raw_sha256", "analyzed_sha256"):
            digest = _require(input_info, key, "root.input")
            if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                raise ValueError(f"root.input.{key} is not a lowercase SHA-256 hex digest")
        if _require(input_info, "mode", "root.input") not in {"exact", "prose"}:
            raise ValueError("root.input.mode must be 'exact' or 'prose'")

        versions = _require_mapping(payload, "versions", "root")
        python_version = str(_require(versions, "python", "root.versions"))
        if strict_versions and not python_version.startswith("3.11."):
            raise ValueError(
                f"Python version mismatch: expected CPython 3.11.x, received {python_version}"
            )
        if strict_versions:
            for key, expected in EXPECTED_VERSIONS.items():
                actual = _require(versions, key, "root.versions")
                if actual != expected:
                    raise ValueError(
                        f"version mismatch for {key}: expected {expected}, received {actual}"
                    )

        counts = _require_mapping(payload, "counts", "root")
        for key in ("words_textstat", "sentences_textstat", "spacy_sentences"):
            value = _require(counts, key, "root.counts")
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"root.counts.{key} must be a positive integer")

        readability = _require_mapping(payload, "readability", "root")
        fre = float(_require(readability, "flesch_reading_ease", "root.readability"))
        fre_manual = float(_require(readability, "flesch_reading_ease_manual", "root.readability"))
        fkgl = float(_require(readability, "flesch_kincaid_grade", "root.readability"))
        fkgl_manual = float(
            _require(readability, "flesch_kincaid_grade_manual", "root.readability")
        )
        if not math.isclose(fre, fre_manual, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(f"FRE cross-check failed: library={fre}, manual={fre_manual}")
        if not math.isclose(fkgl, fkgl_manual, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(f"FKGL cross-check failed: library={fkgl}, manual={fkgl_manual}")

        passive = _require_mapping(payload, "passive_voice", "root")
        passive_count = int(_require(passive, "passive_sentence_count", "root.passive_voice"))
        passive_den = int(_require(passive, "passive_sentence_denominator", "root.passive_voice"))
        passive_pct = float(_require(passive, "passive_sentence_pct", "root.passive_voice"))
        expected_passive_pct = 100.0 * passive_count / passive_den
        if not math.isclose(passive_pct, expected_passive_pct, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(
                "passive sentence percentage does not match its numerator and denominator"
            )
        if not 0.0 <= passive_pct <= 100.0:
            raise ValueError("passive sentence percentage must be between 0 and 100")

        _check_finite_numbers(payload)
    except (TypeError, ValueError) as exc:
        problems.append(str(exc))

    return problems


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate reproducible-text-metrics JSON output.")
    parser.add_argument("input", type=Path, help="JSON result from scripts/analyze_text.py")
    parser.add_argument(
        "--allow-version-drift",
        action="store_true",
        help="Validate schema/invariants without requiring the canonical pinned versions.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("top-level JSON value must be an object")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "fail", "problems": [str(exc)]}, sort_keys=True))
        return 2

    problems = validate(payload, strict_versions=not args.allow_version_drift)
    status = "pass" if not problems else "fail"
    print(json.dumps({"status": status, "problems": problems}, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
