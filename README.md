Here is a structured, professional `README.md` derived from your `GEMINI.md` notes and our conversation. I have organized it to highlight the "Build System" philosophy and the robust error handling we discussed.

***

# Gemini Markdown to LaTeX Converter

A robust, LLM-powered build system that automates the conversion of multi-file Markdown projects into modular, compilable LaTeX documents.

Unlike simple "text replacement" scripts, this tool acts as a **Build Orchestrator**. It manages state, handles API failures gracefully, and sanitizes LLM outputs to ensure the final LaTeX compiles without manual intervention.

## 🚀 Key Features

*   **Modular Architecture:** Generates strictly formatted chapters designed for LaTeX's `\include` mechanism.
*   **Intelligent Sanitization:** Automatically strips Markdown code fences, preambles, and conversational text ("Sure, here is your code...") using a strict delimiter protocol.
*   **Fault Tolerance:** A single chapter failure does not crash the build. The system logs errors and continues processing.
*   **Incremental Builds:** Re-run the tool only on failed files without overwriting successful chapters.
*   **Observability:** Provides a detailed "Build Summary" at the end of execution.

## 🛠 Architecture

This system implements a **Root-and-Branch** architecture.

1.  **The Orchestrator (`main.tex`):** The tool dynamically generates a root file that manages the sequence of execution. It contains no content, only structure.
2.  **The Modules (Chapters):** Every Markdown file becomes a self-contained `.tex` file containing *only* body content (no `\documentclass`, no `\usepackage`).
3.  **Global Dependencies:** All packages are managed centrally in a preamble, ensuring styling consistency across 20+ generated chapters.

## 📦 Installation

1.  **Setup Environment:**
    ```bash
    conda create -n md2tex python=3.10
    conda activate md2tex
    pip install -r requirements.txt
    ```

2.  **Configuration:**
    Set your Google Gemini API key in a `.env` file or environment variable:
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```

## 🖥 Usage

### 1. Generate LaTeX
Run the CLI on your Markdown files. You can pass specific files or wildcards.

```bash
# Process specific files
python src/main.py data/chapter1.md data/chapter2.md

# Process a specific file to a custom output folder
python src/main.py data/intro.md --output_dir output/
```

### 2. The Build Summary (Feedback Loop)
At the end of the process, the tool prints a status report. If the LLM hallucinates or the API times out, you will see exactly where it failed.

**Example Output:**
```text
[SUCCESS] 01_intro.md      -> output/01_intro.tex
[SUCCESS] 02_methods.md    -> output/02_methods.tex
[FAILED]  03_results.md    (Reason: JSON Decode Error)

--------------------------------------------------
BUILD COMPLETE WITH ERRORS
To fix, run: python src/main.py 03_results.md
--------------------------------------------------
```

### 3. Compile PDF
Once the `.tex` files are generated, compile the `main.tex` using your preferred engine:

```bash
pdflatex -output-directory=output output/main.tex
```

## 🧩 System Components

| Module | Function |
| :--- | :--- |
| **`src/main.py`** | The CLI entry point and Build Orchestrator. Discovers files and manages the workflow. |
| **`src/md_parser.py`** | Reads and preprocesses raw Markdown content. |
| **`src/llm_client.py`** | Handles API authentication, retries, and communication with Gemini. |
| **`src/converter.py`** | **The Safety Layer.** Extracts pure LaTeX from the LLM response (using `<latex_content>` tags), strips fences, and ensures the output is safe for `\include`. |

## 🛡 Sanitization Protocol

To prevent compilation errors, this tool employs a **Deterministic Extraction Layer**:

1.  **Prompting:** The LLM is instructed to wrap code in `<latex_content>` tags.
2.  **Extraction:** Regex prioritizes content within these tags.
3.  **Fallback:** If tags are missing, it looks for standard ` ```latex ` blocks.
4.  **Cleaning:** It programmatically removes `\documentclass` or `\begin{document}` if the LLM accidentally includes them.
