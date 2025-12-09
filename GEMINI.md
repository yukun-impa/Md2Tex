# GEMINI.md

## Project Overview

This tool automates the conversion of Markdown files into LaTeX using the LLM. It is designed to handle multi-file projects by converting individual Markdown files into LaTeX fragments and stitching them together into a single, compilable PDF.

## Architecture

- **`src/main.py`**: The CLI entry point. It discovers input files and orchestrates the workflow.
- **`src/md_parser.py`**: Extracts content from Markdown files.
- **`src/converter.py`**: Interfaces with Gemini. **Crucially, this module is responsible for stripping Markdown formatting and ensuring output is valid LaTeX body content.**
- **`src/llm_client.py`**: Manages API authentication and requests.

## Setup and Usage

### 1. Installation
Activate the environment:
```bash
conda activate md2tex
```

### 2. Conversion
Run the tool on specific files. This generates individual `.tex` files and updates the root `main.tex`.

```bash
# Basic usage
python src/main.py chapter1.md chapter2.md

# Specify output directory
python src/main.py file.md --output_dir my_tex_output
```

### 3. Compilation
Compile the generated `main.tex` using your preferred LaTeX engine:

```bash
pdflatex -output-directory=output output/main.tex
```

Compilation Strategy (Modular Chapter Architecture)
To support large-scale document generation, this system implements a Root-and-Branch architecture using LaTeX's \include mechanism. This treats every source Markdown file as a distinct, self-contained Chapter.

1. The "Chapter Module" Constraint
The system does not merely generate text fragments; it generates Structural Modules.

The Contract: Every generated .tex file must function as a valid target for \include{}.
Correct Output: Must start with \chapter{...} and contain strictly body content.
Strict Prohibitions: No Preambles (\documentclass, \usepackage) and no nested includes.
2. The Main Orchestrator (main.tex)
The main.tex file acts as the Build Orchestrator. It does not contain content; it contains the sequence of execution.

LATEX
% main.tex
\input{preamble}
\begin{document}
    \include{output/01_intro}
    \include{output/02_analysis} 
\end{document}
Error Isolation: By using \include, LaTeX generates separate .aux files. If one chapter breaks, it is isolated from the others' internal states.
3. Observability & Recovery (The Feedback Loop)
In distributed generation (generating 20+ chapters), failures are inevitable (API timeouts, hallucinated syntax). The system must handle this gracefully.

Atomic Failure Handling:
The CLI does not crash on a single file failure. Instead, it catches the exception, logs the error, and proceeds to the next file.

The "Build Summary" Standard:
At the end of execution, the CLI must print a Status Report distinguishing between success and failure.

Design Requirement:
TEXT
[SUCCESS] 01_intro.md -> output/01_intro.tex
[SUCCESS] 02_analysis.md -> output/02_analysis.tex
[FAILED]  03_conclusion.md (Reason: JSON Decode Error)

--------------------------------------------------
BUILD COMPLETE WITH ERRORS
To fix, run: python src/main.py 03_conclusion.md
--------------------------------------------------
Incremental Build Capability:
The system design allows running the tool on a subset of files without destroying the work done on previous files. This allows the user to regenerate only the failed chapters.

4. Dependency Management
Since individual chapters cannot load packages, dependencies must be declared Globally.

Strategy: Maintain a strict "Standard Library" of packages in your main template (e.g., amsmath, graphicx, listings).
Prompt Engineering: The System Prompt must explicitly instruct the LLM: "Assume standard packages are already loaded. Do not add \usepackage commands."
Development Guidelines
Prompt Engineering: Explicitly forbid Markdown fences and preambles.
Sanitization: Programmatically strip ```latex fences and \documentclass tags before saving.
State Management: The tool dynamically generates main.tex based on the files present in the output/ directory, ensuring the build structure is always up to date.
