# GEMINI.md

## Project Overview

This project is a Python-based command-line tool for converting Markdown files into LaTeX documents. It leverages the Gemini Large Language Model (LLM) to perform the conversion from Markdown syntax to LaTeX code.

The tool parses a Markdown file, extracts YAML frontmatter for metadata (like title and author), and then uses the Gemini API to convert the main content of the Markdown file into a `.tex` file. Finally, it generates a root `main.tex` file that includes the converted content and is ready for compilation into a PDF.

The project is structured into several modules:
- `src/main.py`: The main entry point for the command-line tool.
- `src/md_parser.py`: Handles parsing of Markdown files, including YAML frontmatter.
- `src/converter.py`: Orchestrates the conversion process, including prompting the LLM.
- `src/llm_client.py`: A client for interacting with the Gemini API.

## Building and Running

### 1. Installation

First, create and activate the conda environment:

```bash
conda create -n md2tex python=3.9 -y
conda activate md2tex
```

Then, install the necessary Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Set up API Key

This project uses the Gemini API, which requires an API key. You need to create a `.env` file in the root of the project and add your API key to it:

```
GEMINI_API_KEY="YOUR_API_KEY"
```

If you don't provide an API key, the `llm_client.py` module will run in a mock mode, which performs a basic, non-AI-powered conversion.

### 3. Running the Conversion

To convert one or more Markdown files, run the `main.py` script with the paths to your input files.

**Note for local development:** When running the script locally, you need to set the `PYTHONPATH` to the root of the project so that the script can find the `src` module.

```bash
PYTHONPATH=. python src/main.py path/to/your/file1.md path/to/your/file2.md
```

You can specify an output directory using the `--output_dir` flag. By default, the output is saved in the `output/` directory.

```bash
PYTHONPATH=. python src/main.py file1.md file2.md --output_dir my_latex_files
```

You can also provide a custom template for the main `.tex` file using the `--template` flag.

```bash
PYTHONPATH=. python src/main.py file1.md file2.md --template path/to/your/template.tex
```

Alternatively, you can specify the template in the YAML frontmatter of your Markdown file. This will override the `--template` argument.

```yaml
---
title: My Document
author: John Doe
template: path/to/your/template.tex
---
```




### 4. Compiling the LaTeX

After running the conversion, the `output/` directory will contain the generated `.tex` files. To compile them into a PDF, you can use a LaTeX compiler like `pdflatex`:

```bash
pdflatex -output-directory=output output/main.tex
```

## Development Conventions

- **Configuration:** Project configuration, such as the Gemini API key, is managed through environment variables using `python-dotenv`.
- **Modularity:** The code is organized into distinct modules with clear responsibilities (parsing, conversion, API client).
- **Templates:** A LaTeX template is used to generate the final `main.tex` file, allowing for easy modification of the document structure.
- **Error Handling:** The `llm_client.py` includes basic error handling for API calls and a fallback mock mode if the API key is not available.
