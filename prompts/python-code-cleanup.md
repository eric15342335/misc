Python 3.12+ only.

Requirements

* Support Python 3.12+ exclusively.
* Remove all legacy compatibility code, version checks, shims, and deprecated APIs.
* Prefer modern, actively maintained libraries that maximize:

  * Performance
  * Reliability
  * Edge-case handling
  * Maintainability
  * Scalability
* Do not reinvent functionality already provided by the Python standard library or mature third-party libraries.
* Minimize comments.
* Keep comments only when they explain non-obvious business logic or architectural decisions.
* Do not use section-banner comments such as:
  * `# CONFIG`
  * `# Constants`
  * `# Helpers`
  * `# Main`
* Use ASCII-only source code unless Unicode is required by the problem domain.
* Avoid decorative output formatting.
* Do not use patterns such as:
  * `"=" * 80`
  * `"-" * 80`
  * manual indentation padding
  * handcrafted table rendering
  * custom alignment logic
* Prefer existing standard-library facilities where applicable:
  * pathlib
  * logging
  * pprint
  * textwrap
  * argparse
  * json
  * csv
  * string.Template
  * dataclasses
  * enum
  * contextlib
  * itertools
  * functools
  * collections
* Prefer:
  * pathlib over os.path
  * collections.abc over legacy typing aliases where appropriate
  * dataclasses or pydantic models where appropriate
  * context managers for resource management
  * structured logging over print debugging
  * exception chaining via `raise ... from ...`
* Remove dead code immediately.
* Avoid speculative abstractions.
* Favor readability, explicitness, and maintainability.

Quality Gates

All code must pass:

* ruff check
* ruff format
* pylint
* mypy
* pyscn

Additional Requirements

* Ruff line length: 120.
* Ruff import-sorting rules enabled.
* Review actual pyscn findings.
* Successful pyscn execution does not imply acceptable code quality.
* Address or explicitly justify significant pyscn findings.
* Fact-check technical assumptions before implementation.
* Verify library capabilities against current documentation before introducing dependencies.
* Do not rely on memory when current documentation can be consulted.

Tooling Notes

Recommended execution order:

```bash
ruff check --fix
ruff format
mypy
pylint
pyscn
```

Ruff import sorting is derived from isort and is intended to be near-equivalent to isort's Black profile. Running standalone isort is unnecessary unless project-specific behavior requires it.

Ruff formatting does not perform import sorting. Import sorting is handled by Ruff's linting phase.
