# Markdown to LaTeX Converter

This project is a Python-based command-line tool for converting Markdown files into LaTeX documents. It leverages a Large Language Model (LLM) to perform the conversion from Markdown syntax to LaTeX code.

## Features

*   **Markdown to LaTeX Conversion**: Converts Markdown files to `.tex` files.
*   **LLM-Powered**: Uses a Large Language Model for smart conversion (with a mock mode for offline use).
*   **YAML Frontmatter Support**: Parses YAML frontmatter for metadata like title and author.
*   **Customizable LaTeX Templates**: Allows you to use your own LaTeX templates for the main document, specified via a command-line argument or in the Markdown frontmatter.
*   **LaTeX Template**: Generates a main `.tex` file that includes the converted content.

## Getting Started

### Prerequisites

*   Python 3.6+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yukun-impa/Md2Tex.git
    cd Md2Tex
    ```
2.  Create and activate the conda environment:
    ```bash
    conda create -n md2tex python=3.12 -y
    conda activate md2tex
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

This project uses the Gemini API by default, which requires an API key.

1.  Create a `.env` file in the root of the project:
    ```
    GEMINI_API_KEY="YOUR_API_KEY"
    ```
2.  If you don't provide an API key, the tool will run in a mock mode, which performs a basic, non-AI-powered conversion.

## Usage

To convert one or more Markdown files, run the `main.py` script with the paths to your input files.

```bash
python main.py path/to/your/file1.md path/to/your/file2.md
```

You can specify an output directory using the `--output_dir` flag. By default, the output is saved in the `output/` directory.

You can also provide a custom template for the main `.tex` file using the `--template` flag.

```bash
python main.py file1.md file2.md --template path/to/your/template.tex
```

Alternatively, you can specify the template in the YAML frontmatter of your Markdown file. This will override the `--template` argument.

```yaml
---
title: My Document
author: John Doe
template: path/to/your/template.tex
---
```

After running the conversion, the output directory will contain the generated `.tex` files. To compile them into a PDF, you can use a LaTeX compiler like `pdflatex`:

```bash
pdflatex -output-directory=output output/main.tex
```

## YAML Frontmatter Support

You can include YAML frontmatter at the beginning of your Markdown files to provide metadata for your LaTeX document. This metadata can be used by the LaTeX templates for fields like title, author, date, and even to specify a custom template for that specific Markdown file.

**Structure:**

The frontmatter must be at the very top of the file, enclosed by triple-dashed lines (`---`).

```yaml
---
title: Your Document Title
author: Your Name
date: "December 7, 2025" # Optional: Override the default date
template: path/to/your/custom_template.tex # Optional: Custom template for this file
document_class: article # Example of custom LaTeX options
---
```

**Supported Fields:**

*   `title`: The title of your document.
*   `author`: The author(s) of the document.
*   `date`: The publication date. If not provided, the current date might be used by the LaTeX template.
*   `template`: (Optional) Path to a specific LaTeX template file to use for this Markdown document. This overrides the `--template` command-line argument.
*   Any other custom fields you define can be accessed within your LaTeX templates.

## Development

The project is structured into several modules:

*   `src/main.py`: The main entry point for the command-line tool.
*   `src/md_parser.py`: Handles parsing of Markdown files, including YAML frontmatter.
*   `src/converter.py`: Orchestrates the conversion process.
*   `src/llm_client.py`: A client for interacting with the LLM API.
*   `templates/main.tex`: The LaTeX template for the main document.
