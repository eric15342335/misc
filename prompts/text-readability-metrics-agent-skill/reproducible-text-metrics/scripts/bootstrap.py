#!/usr/bin/env python3
"""Create or verify the pinned runtime environment for this skill."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import venv
from pathlib import Path
from typing import Any

EXPECTED = {
    "textstat": "0.7.13",
    "spacy": "3.8.15",
    "lexical-diversity": "0.1.1",
    "en-core-web-sm": "3.8.0",
    "setuptools": "79.0.1",
}
SKILL_ROOT = Path(__file__).resolve().parent.parent
LOCK_FILE = SKILL_ROOT / "requirements.lock"


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run_checked(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() or "no stderr"
        raise RuntimeError(
            f"command failed ({exc.returncode}): {' '.join(command)}\n{stderr}"
        ) from exc
    return completed.stdout.strip()


def inspect_versions(interpreter: Path) -> dict[str, str]:
    code = (
        "import importlib.metadata as m, json; "
        "names=['textstat','spacy','lexical-diversity','en-core-web-sm','setuptools']; "
        "print(json.dumps({n:m.version(n) for n in names}, sort_keys=True))"
    )
    output = run_checked([str(interpreter), "-c", code])
    parsed = json.loads(output)
    if not isinstance(parsed, dict):
        raise RuntimeError("version probe did not return a JSON object")
    return {str(key): str(value) for key, value in parsed.items()}


def verify_versions(interpreter: Path) -> dict[str, str]:
    actual = inspect_versions(interpreter)
    mismatches = {
        key: {"expected": expected, "actual": actual.get(key, "missing")}
        for key, expected in EXPECTED.items()
        if actual.get(key) != expected
    }
    if mismatches:
        raise RuntimeError(f"runtime version mismatch: {json.dumps(mismatches, sort_keys=True)}")
    run_checked([str(interpreter), "-m", "pip", "check"])
    return actual


def create_environment(venv_dir: Path) -> dict[str, Any]:
    if not LOCK_FILE.is_file():
        raise RuntimeError(f"lock file is missing: {LOCK_FILE}")
    if not venv_python(venv_dir).exists():
        venv.EnvBuilder(with_pip=True, clear=False).create(venv_dir)
    interpreter = venv_python(venv_dir)
    run_checked(
        [
            str(interpreter),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--requirement",
            str(LOCK_FILE),
        ]
    )
    versions = verify_versions(interpreter)
    return {"python": str(interpreter.resolve()), "versions": versions}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or verify the pinned virtual environment for reproducible-text-metrics."
    )
    parser.add_argument(
        "--venv",
        type=Path,
        default=SKILL_ROOT / ".venv",
        help="Virtual-environment directory (default: <skill>/.venv).",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Verify an existing environment without installing packages.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if sys.version_info[:2] != (3, 11):
        print(
            json.dumps(
                {
                    "status": "fail",
                    "error": (
                        "canonical runtime requires CPython 3.11; "
                        f"received {sys.version_info.major}.{sys.version_info.minor}"
                    ),
                },
                sort_keys=True,
            )
        )
        return 2
    interpreter = venv_python(args.venv)
    try:
        if args.check_only:
            if not interpreter.exists():
                raise RuntimeError(f"virtual environment does not exist: {args.venv}")
            result: dict[str, Any] = {
                "python": str(interpreter.resolve()),
                "versions": verify_versions(interpreter),
            }
        else:
            result = create_environment(args.venv)
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, sort_keys=True))
        return 2

    print(json.dumps({"status": "pass", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
