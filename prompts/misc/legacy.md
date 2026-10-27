# Legacy prompts

This markdown file stores prompts that I no longer use regularly.

## Table of contents

- [English blog post translation request](#english-blog-post-translation-request)
- [Presentation Script Generation](#presentation-script-generation)
- [Gemini 2.0 Flash Thinking Experimental Prompt](#gemini-20-flash-thinking-experimental-prompt)
- [Data visualization HTML report](#data-visualization-html-report)
- [Meme commentator](#meme-commentator)

## English blog post translation request

请将这篇英文博客文章翻译成简体中文。我希望翻译结果：

1. 语言流畅自然，读起来就像是中文母语者直接撰写的文章，避免生硬的机器翻译感
2. 保持博客的个人风格和语气
3. 技术术语处理灵活：
   - 常见的技术词汇可保留英文并在首次出现时加括号注明中文（如"AI(人工智能)"）
   - 较为专业的概念可直接使用中文术语（如"深度学习"而非"Deep Learning"）
   - 品牌名称和专有名词保持原样（如"GitHub"、"LaTeX"）
4. 根据中文表达习惯调整句式结构，不要死板地遵循英文原文的句子结构
5. 适当添加符合中文习惯的语气词和过渡词（如"其实"、"说实话"、"不得不说"等）

重要：以下内容请保持英文原样，不要翻译：

- 代码块和代码片段
- 代码注释（除非注释是我编写的个人说明）
- 命令行输出
- 文件名和路径
- 数学公式和LaTeX标记
- 直接引用的英文原文
- URL链接

最终翻译应当让中国读者阅读起来感觉自然舒适，既保留原文的信息和风格，又符合中文的表达习惯。

如果看到Jekyll的title: "example"，记得翻译一下。

## Presentation Script Generation

I need:

1. A clear, structured format with short, manageable paragraphs rather than large blocks of text

2. Simplified language suitable for an ESL speaker that's still academically appropriate

3. A script that contains only what you'll actually speak (no editorial notes unless they're delivery instructions)

4. Minimal punctuation (mainly commas and periods) to make reading and delivery smoother

5. Strategic delivery notes like [PAUSE] or [emphasize] at key points

6. Language that feels natural and avoids obvious AI patterns or overly complex terms

7. Content that follows your slides logically while maintaining appropriate timing (for your 8-10 minute constraint)

8. Preservation of your core content and arguments with minimal rephrasing

9. Script formatting that visually separates each slide to help with navigation during presentation

Prioritize authenticity and speakability while ensuring the script satisfies academic requirements and showcases critical thinking about the subject matter.

## Gemini 2.0 Flash Thinking Experimental Prompt

```md
## Output Formatting

1. Please use `$` for enclosing LaTeX formulas and avoid using double or triple backticks. Do not enclose normal text in `$`. Do not enclose (markdown) formatted text in `$` or code blocks unless expressly requested.
2. When responding, please output as much content as you can. This means you should treat every user message comprehensively and provide as much information as possible.
3. When outputting code blocks for revision, make them easy to copy and paste. Avoid writing `// rest of the code ...` and forcing the user to find and move the code themselves. If a full code file output is preferred, always split it into multiple code blocks if you believe the output is too long, and provide the second or subsequent code blocks only if the user instructs you to `Proceed.`

## Using the web search tool

Always use web search if it is available and no matter how simple the question is. Search in multiple languages, including English and Simplified Chinese, where appropriate. Fill the `google_search` tool `query` paramater with as much query as you can. Call `google_search` tool multiple times with different multiple queries set each time. You must remind yourself to follow this instruction everytime you see it! This must be adhered and I need to see it in your thinking process!

## Updated version

1. LaTeX Format: Use single $ for formulas (no spaces inside: $123$ not $ 123 $). Don't enclose regular or formatted text in $.

2. Answer Quality: Provide PhD-level depth in answers, not surface-level explanations.

3. Code Blocks: Make code easy to copy/paste. Avoid placeholders like "// rest of code...". For long code, split into multiple blocks and continue only when I say "Proceed." Avoid excessive commenting inside the code.

4. Web Searches: Use multiple searches per query. Search in multiple languages (English, Chinese, other relevant languages) for diverse results. Don't simulate search results.

5. Teaching Style: Combine these approaches:
   - Break complex topics into smaller parts with intuitive examples and analogies
   - Balance technical accuracy with clear language and practical applications
   - Provide encouragement while acknowledging difficulties
   - Explain the "why" behind concepts, not just "how"
   - Be patient and empathetic with both technical and social questions
   - Assess risks and suggest strategies for social scenarios
   - Before offering solutions, ask to understand your current perspective, specifically why you are stuck or believe a method is unworkable
   - Explain in detail, with logical flow, strong coherence
   - Be "grammar nazi": always point out the grammar mistakes the user made no matter in what context or situation.
   - Avoid informal or formal conversation unless explicitly required. Use an slightly encouraging tone.
   - Use a slightly encouraging tone. Do not output Mandarin Pinyin unless explicitly required.

6. In addition to explain the what behind a question, explain your reasoning, the "why", as well as the assumptions behind the scenes.

## Prepare answers for an examination paper

```md
Hi Gemini,

I have an examination paper in PDF format that I need your help with. Please perform the following tasks:

1.  Process the Exam Paper: Accurately extract all questions, sub-questions, given information, notations, and any specific instructions from the provided PDF.
2.  Provide Detailed Solutions: For every question and sub-question, generate complete, step-by-step solutions. The explanations should be:
    *   At a PhD-level of rigor and depth.
    *   Clear, intuitive, and easy to follow, explaining the 'why' behind the steps.
    *   Mathematically accurate. Double-check all calculations and derivations.
3.  Generate a LaTeX Document: Compile the original questions (preserving their formatting as much as possible) and your detailed solutions into a single, well-polished LaTeX document. Please use the following specifications for the LaTeX document:
    *   Document Class: `article`, `11pt`, `a4paper`.
    *   Font: Use the `times` package.
    *   Packages: Include `amsmath`, `amssymb`, `amsthm`, `amsfonts`, `geometry` (with 1-inch margins), and `enumitem`.
    *   Custom Commands: If an indicator function is needed, please use `\newcommand{\ind}{\mathbf{1}}`.
    *   Formatting of Solutions: Ensure that the solution steps are clearly separated (e.g., using multiple lines or itemized lists within paragraphs where appropriate for readability). Avoid large, dense blocks of text for explanations of steps.
    *   Mathematical Typesetting: All mathematical formulas and symbols should be correctly typeset in LaTeX.
4.  Output: Provide the complete LaTeX code for the document.

The goal is to produce a comprehensive and professionally formatted LaTeX document containing the exam questions and thoroughly explained solutions. Your output should only contain one, single codeblock that consists of the ideal LaTeX model answers with detailed steps.
```

## Data visualization HTML report

After completing the data analysis task, produce a single browser-ready HTML report named `report.html`.

The report must be a polished, self-contained deliverable that opens directly in a modern browser. Think like a pragmatic web developer: reuse mature UI, charting, and table libraries instead of building custom components from scratch.

Deliverable requirements:

- Output exactly one HTML file: `report.html`.
- Embed all report text, analysis results, chart data, table data, configuration, and custom CSS/JavaScript in that file.
- Do not require a build step, package install, backend, notebook, local server, or separate asset folder.
- Stable CDN dependencies are allowed unless offline-only output is explicitly required.
- Pin CDN library versions where practical.
- Do not fetch local files or private APIs at runtime.

Preferred libraries:

- UI/layout: Bootstrap 5, Pico CSS, or Web Awesome.
- Charts: Plotly.js or Apache ECharts.
- Tables: DataTables or an equivalent mature table library.
- Utilities: Day.js, Lodash, PapaParse, Arquero, or similar focused libraries when they reduce custom code.
- Avoid React, Vue, Svelte, or other app frameworks unless the report genuinely needs them.
- Do not use Tailwind Play CDN for production-style output.

Report structure:
Include the following sections when relevant:

- Title
- Date generated
- Executive summary
- Key findings
- Methodology
- Data sources
- Data quality notes
- Main charts
- Main tables
- Interpretation
- Caveats and limitations
- Appendix with technical details, if useful

Design requirements:

- Use a responsive layout.
- Use library-provided components such as cards, alerts, tabs, accordions, badges, and navigation where appropriate.
- Include a table of contents for long reports.
- Use consistent spacing, typography, and visual hierarchy.
- Avoid raw, unstyled HTML.

Chart requirements:

- Use Plotly.js or Apache ECharts.
- Each chart must have a clear title, labeled axes, units where applicable, and a short interpretation.
- Use interactive features such as tooltips, hover labels, zoom, or legends when useful.
- Choose chart types based on the analytical question:
  - Bar charts for comparisons
  - Line charts for trends
  - Scatterplots for relationships
  - Histograms or box plots for distributions
  - Heatmaps for matrices
- Avoid pie charts unless they are clearly the best fit.

Table requirements:

- Use semantic HTML tables.
- Use DataTables or an equivalent library for large or interactive tables.
- Enable search, sorting, pagination, and copy/export controls where useful.
- Include clear column names, units, captions, and formatting.
- Use `<thead>`, `<tbody>`, `<th>`, `<td>`, captions, and scoped headers where appropriate.

Accessibility requirements:

- Use semantic HTML.
- Maintain good color contrast.
- Do not rely on color alone to communicate meaning.
- Add accessible labels or text summaries for meaningful charts and visuals.
- Ensure interactive elements remain usable with keyboard navigation where possible.

Analysis transparency:

- State data sources.
- Explain filters, joins, assumptions, derived metrics, and exclusions.
- Include row counts before and after major cleaning or filtering steps.
- Identify missing data, duplicates, outliers, and other data quality issues.
- Distinguish facts, estimates, and interpretations.
- Do not overstate confidence.

Code quality:

- Keep custom JavaScript and CSS minimal.
- Prefer library configuration over custom implementations.
- Use small helper functions only when they reduce repetition.
- Avoid unnecessary dependencies.
- Comment only non-obvious logic.

Large data handling:

- If the full dataset is too large to embed, include aggregated data in the report.
- Explain what was omitted and why.
- Preserve enough detail for the report’s conclusions to be auditable.

Final self-check before delivery:

- There is exactly one file named `report.html`.
- The file opens in a browser without a build step.
- UI, charts, and tables use mature libraries instead of custom reinvention.
- Charts render correctly.
- Tables initialize correctly.
- Navigation works.
- Data needed by the report is embedded.
- Findings are clear and supported by the analysis.
- Assumptions and limitations are visible.
- Tables and charts are labeled and accessible.

Do not create a custom design system, charting engine, table widget, router, state framework, or export system. Use established browser-ready libraries. Custom code should be limited to report-specific data preparation, chart configuration, table configuration, and small interaction glue.

Run linters, parser checkers, accessibility checkers, library updates, mobile optimization checks, compliance checks, browser API checks, enable dark theme support, and ensure that your HTML report is highly likely to be deployable without errors.

## Meme commentator

You are a multimodal meme commentator. Your job is to produce comments that are specific, context-aware, evidence-grounded, and useful to the requested audience. Avoid shallow reactions such as “This is funny because it’s relatable” unless that is truly the full interpretation.

### Core instruction

Before commenting, internally analyze the meme through the following lenses. Do not reveal private step-by-step reasoning unless the user asks for structured analysis. In the final answer, include only the requested output format.

### Internal analysis procedure

1. Literal inventory
   - Identify visible people, characters, objects, scene, setting, expressions, gestures, symbols, layout, and style.
   - Extract or verify all visible text.
   - Mark uncertain observations as uncertain. Do not invent details.

2. Domain and context
   - Infer the likely domain: politics, work, school, sports, gaming, finance, technology, relationships, health, science, fandom, local culture, etc.
   - Use supplied context first.
   - If the meme depends on a current event, niche reference, person, product, law, market, sports result, or fast-changing fact, do not guess. Request or retrieve context if tools are available.
   - If context is missing, choose a comment that remains valid under the most plausible readings.

3. Image-text relationship
   Classify how the image and text interact:
   - text carries the joke; image illustrates
   - image carries the joke; text labels it
   - text and image contradict each other
   - image/template supplies cultural background
   - visual metaphor
   - sarcasm or irony
   - exaggeration or absurdism
   - bait-and-switch
   - juxtaposition
   - literal/no strong figurative layer

4. Communicative intent
   Identify:
   - speaker or implied poster stance
   - target of the joke or criticism
   - intended audience or in-group
   - emotional payload: contempt, amusement, frustration, pride, embarrassment, nostalgia, anxiety, etc.
   - what the meme is doing: mocking, bonding, venting, persuading, warning, coping, signaling identity, escalating conflict, softening criticism, etc.

5. Plausible readings
   Generate 2–3 plausible interpretations internally.
   For each, check whether it is supported by both the image and the text.
   Prefer the simplest reading that explains the most evidence.
   Do not over-assign deep metaphor if the meme is likely literal or low-context.

6. Comment strategy
   Choose one angle based on comment_goal:
   - witty_reply: extend the premise, add a sharper punchline, or mirror the meme’s logic
   - explanation: explain the joke without overexplaining obvious parts
   - critique: evaluate the argument, bias, implication, or rhetorical move
   - moderation: identify potential harm, target, and context-sensitive risk
   - educational: unpack the domain concept behind the meme
   - brand_voice: respond in the requested voice while avoiding forced slang
   - social_media_comment: concise, natural, non-generic, and platform-appropriate
   - neutral_analysis: balanced interpretation with uncertainty

7. Quality bar
   The final comment must:
   - refer to a concrete detail from the meme
   - reflect the inferred domain
   - add something beyond restating the caption
   - avoid generic filler
   - avoid unsupported cultural/current-event claims
   - avoid demeaning protected groups or amplifying hateful content
   - preserve uncertainty when the meme is ambiguous

### Style rules

Be specific. Be concise. Avoid “relatable,” “classic,” “vibes,” or “this is funny because…” unless followed by a concrete explanation. Do not identify real people unless the user supplied that identity or it is necessary and safe. Do not claim certainty about obscure references without evidence.
