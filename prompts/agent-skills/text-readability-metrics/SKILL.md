---
name: text-readability-metrics
description: Check how easy English text is to read. Also count word mix, word types, sentence size, links between words, and passive voice. Use this skill to check or compare English text or files.
compatibility: Needs uv, shell, files, and the web for the first run.
---

# Text Readability Metrics

Use the script for each score.

Run it in this skill folder:

```bash
uv run --script scripts/analyze_text.py input.txt --pretty
```

The default `exact` mode reads all input. Use `--mode prose` to skip Markdown code blocks, headings, table rows, and list marks. Use `-` for stdin. Use `--output FILE` to save JSON.

Check the `warnings` field before you report scores. Use the same mode and script when you compare texts.

Keep each reading score on its own unless the user asks for an average. TTR changes with text length. Use the same parser when you compare parser scores. Keep passive sentence rate and passive predicate rate separate. For each passive rate, show the count and total.
