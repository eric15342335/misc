# Legacy prompts

This markdown file stores prompts that I no longer use regularly.

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
