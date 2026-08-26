---
name: strict-minimal-edits
description: Use this skill when modifying existing code, scripts, configuration, or infrastructure and the user asks for the smallest possible diff, minimum edits, exact scope adherence, preservation of existing behavior, or no unrelated cleanup. Do not use for refactors, redesigns, modernization, broad reviews, or open-ended improvements.
---

# Strict Minimal Edits

## Goal

Implement exactly the requested behavior with the smallest practical diff. Treat the user's scope as a hard boundary.

## Workflow

1. Read the relevant existing files before editing.
2. Convert the request into a short internal allowlist of permitted changes.
3. Identify existing behavior that must remain unchanged.
4. Make only the changes required by the allowlist.
5. Reuse the current structure, naming, control flow, commands, and conventions.
6. Run only focused checks needed to verify the requested behavior.
7. Inspect the final diff and revert every unrelated hunk.

## Scope rules

- Do not fix unrelated bugs or warnings.
- Do not refactor, rename, reorganize, or reformat adjacent code.
- Do not add helpers, abstractions, dependencies, files, comments, validation, or configuration unless directly required.
- Do not change logging, tracing, timeouts, retries, defaults, security settings, error messages, or public interfaces unless requested.
- Do not replace the user's approach with a preferred architecture.
- Do not add speculative future-proofing, cleanup, hardening, or optional improvements.
- Do not create alternate implementations, extra patches, documentation, or other deliverables unless requested.

## Necessary supporting edits

A supporting edit is allowed only when all of these are true:

1. The requested behavior would otherwise fail or remain incomplete.
2. The edit is directly connected to that behavior.
3. No smaller viable alternative exists.
4. Unrelated behavior remains unchanged.

When uncertain whether an edit is necessary, leave it out.

## Adjacent issues

If an unrelated issue is discovered, do not modify it. Mention it only when it blocks the requested change or creates an immediate correctness risk in the changed path. Keep that note separate from the delivered diff.

## Diff audit

For every changed hunk, ask:

1. Which explicit user requirement requires this hunk?
2. Could the requirement be met with fewer changed lines?
3. Does the hunk alter unrelated behavior, output, formatting, or files?

Revert any hunk without a direct answer to the first question.

## Output

State what changed using the user's own scope. Provide only the requested file, patch, explanation, or validation result. Do not append unsolicited recommendations or describe unrelated opportunities.

## Boundary example

When asked to add existence checks and creation logic for one resource, add only the lookup, creation branch, and directly required wiring. Do not also change tracing, timeout handling, validation policy, command-line behavior, naming conventions, or nearby error handling.
