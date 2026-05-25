# Collection of Prompts

## Side note

2026 Update: I heard <https://clawhub.ai/> has a collection of good prompts that might be useful for many different use cases.

### Fix grammar

Please fix the grammar for the following enclosed text. No rephrasing, change of word usage, change of sentence structure, or alteration of the original sentence meaning is allowed. You are only allowed to make minor, aesthetic, non-content-meaning-altering changes, such as fixing typos, adding pronouns, connectives, punctuation, and other filler changes. You must preserve the original text format and structure.

### State assumptions

state:

1. any assumptions you made
2. any edge cases you haven't considered
3. any implicit theories you used, but did not explain (And if you don't want to explain them)
4. be detailed rather than concise

### what

Please use $ for enclosing mathematical or LaTeX formulas and avoid using double or triple ticks. Do: $\LaTeX$. Don't: $ \LaTeX $ (do not leave space). Do not enclose your $formulas$ with `, otherwise the LaTeX would render as a code, not formulas. In other words, your LaTeX formulas should not be placed inside as a inline code.

When responding, please output as much as you can. This means you should treat every user message comprehensively and provide as much information as possible. When you receive a question from the user, do not provide the answer directly or indirectly in the context of helping the student think for himself, instead of just blindly reading the explanation.

Only answer only when your confidence in the answer is greater than 90%.
A correct answer earns +1 point; an incorrect answer loses 9 points; answering "I don't know" gets 0 points.

### Coding

- Think very hard.
- You are an senior software engineer at google.
- You are an expert in machine learning, data science, software refactoring and maintenance.
- You are tasked to refactor this data science script.
- Your aim is mainly identify the code in the script that violates the Don't Repeat Yourself (DRY) principle, and propose reusable strategies (functions, shared variable declarations, object oriented programming).
- Your aim is to preserve the order of the code.
- Your aim is to propose a method without significant "rewriting".
- "Rewriting" is defined as the number of times of copying, pasting, deleting, adding, and replacing existing codes with new one.
- You are encouraged to use advanced features in Python that helps maintainability. E.g. @dataclass, ABC @abstractmethod, etc.
- The minimum version you should support is Python 3.11. For example, you cannot use @override for an overridden function by an inherited class, because that syntax does not exist before Python 3.12.
- Try your best.
- You do not need to output code that remains unchanged.
- Variable names' length should be at least longer or equal to 3 characters. No exceptions allowed.

### Web search

Do not rely on your pretrained prior facts and always reference online information for reference.

You must search online extensively for every terms and details, even if you are fully confident in it, or it was a simple term. Do not trust your pretrained prior knowledge and always search online for fact checking and confirmation.

can you help me on problem X? before answering, please think about strategies of how a teacher can answer student's question and help him learn without spoiling or letting him get the answer without conscious effort or hard work.

### Data science

Analyze and visualize the results by writing python data science code (do not write any comments, do not reinvent the wheel, always web search to use the latest functions).

If at any step you are unsure about something and cannot find a solution online, do not attempt to guess the answer using "common sense" or logical reasoning. If you do not know, simply say you do not know, stop, and wait for further instructions.

Requirements

- Python 3.12+. All legacy code support should be removed entirely.
- Rich for progress bar and ETA
- Modern libraries, e.g. FastAPI, pydantic, dataclass, for best in class performance, reliability, edge case handling, maintainability and scalability
- Omit all unnecessary comments in code
- Omit "# --- CONFIG ---" (hyphen) comments in code
- Avoid using unicode characters in code. Focus on ASCII. This means no emojis.
- fact check everything after you make a plan
- all ruff check
- all ruff format line length 120
- isort
- pylint
- pyscn from ludo-technologies, run check and observe the produced analysis output. successful tool usage does not mean free of errors.
- and one python linter of your choice
- and remove all manual reinventing the wheel output formatting, e.g. "="*60, manual space indent. replace them with existing wheels

## Git commit message generation

Generate a git commit message in the form of type(scope): description for this git diff.

## Studying

I am doing Assignment 3. I am brainstorming whether my idea is okay and correct. Whenever I say something, if you know it is workable and correct, do not give me the answer. Instead, tell me which page of the slides I should look at. If it is not correct, try to either point to slides that contain the same statement (e.g. “this is not workable, as we know ...”), if they exist, or simply respond with nothing. Do not give me a direct answer (although I can infer it from your response anyway). In all scenarios, if you can find a better way to teach me, you can ignore my instructions and do it your way instead. Use Google to find the best way to teach without offloading the assignment’s mental effort to AI.

## AI Studio to WhatsApp

Reformat your previous output verbatim but apply Whatsapp-compatible markdown formatting as they use different number of asterisks for bold/italic.

## Explanation

Can you explain it from first principles?

## Web development

Fact-check your build/website against best practices using various linters, formatters, and code complexity checkers in the JavaScript ecosystem, and fix all issues. Before you start, research available tools. After you complete your fact-check and fix all issues arising in your codebase, create a production-optimized build again and deliver the website in a zipped distribution/build folder so that the browser can open `index.html` and instantly view your output.

Research the topic, what, why, when, where, how, and who, prior works, derivative works, ecosystem trends and technologies, etc.

Research the best tech stack for building a website showcasing your research results on the topic. Then build the website using your researched and modernized tech stack.

I want the technical, in-depth details. We already know there could be positive or negative implications. I need only certain answers. Do not guess. If you don't know, just say, "I cannot determine from the source," after you believe you have researched a substantial amount of material and found no clues.
