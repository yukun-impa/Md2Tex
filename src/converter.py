import os
from src.llm_client import LLMClient

class Converter:
    def __init__(self, output_dir="output", template_path=None):
        self.client = LLMClient()
        self.output_dir = output_dir
        self.template_path = template_path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def convert(self, metadata, content, filename="content.tex"):
        """
        Generates the prompt and calls the LLM.
        """
        
        # 1. Determine Structure Mapping from Metadata or Defaults
        structure_map = metadata.get('structure_map', {
            '#': 'section',
            '##': 'subsection',
            '###': 'subsubsection'
        })

        # 2. Build the System Prompt
        system_instruction = (
            "You are an expert LaTeX converter. Your task is to convert the given Markdown text into a high-quality, compilable LaTeX snippet.\n\n"
            "**Assumed Packages (do not include `\\usepackage` commands in your output):**\n"
            "*   `soul` for strikethrough (`\\sout{}`).\n"
            "*   `hyperref` for links (`\\href{}`).\n"
            "*   `graphicx` for images (`\\includegraphics{}`).\n"
            "*   `amsmath`, `amsfonts`, `amssymb` for mathematical typesetting.\n\n"
            "**Conversion Rules & Guidelines:**\n\n"
            "1.  **Document Structure:**\n"
            "    *   Analyze the Markdown heading hierarchy (`#`, `##`, `###`, etc.) to infer the document structure.\n"
            "    *   **Strictly adhere to the following mapping for Markdown headings to LaTeX sectioning commands:**\n"
            "        " + str(structure_map) + "\n"
            "    *   Use appropriate LaTeX sectioning commands (`\\section`, `\\subsection`, `\\subsubsection`, `\\paragraph`).\n"
            "    *   If the structure is inconsistent (e.g., a `###` follows a `#`), make a logical choice to create a clean LaTeX structure. Do not blindly follow the Markdown.\n"
            "    *   The output should ONLY be the body content. Do NOT include `\\documentclass`, `\\begin{document}`, or `\\end{document}`.\n\n"
            "2.  **Text Formatting:**\n"
            "    *   Convert `**bold**` and `__bold__` to `\\textbf{bold}`.\n"
            "    *   Convert `*italic*` and `_italic_` to `\\textit{italic}`.\n"
            "    *   Convert `~~strikethrough~~` to `\\sout{strikethrough}`.\n"
            "    *   Convert inline `code` to `\\texttt{code}`.\n\n"
            "3.  **Math:**\n"
            "    *   Convert inline math (e.g., `$E=mc^2$`) to `$...$` (e.g., `\\$E=mc^2\\$`).\n"
            "    *   Convert display math (e.g., `$$a^2 + b^2 = c^2$$` or `\\$\\$a^2 + b^2 = c^2\\$\\$`) to `\\[ ... \\]` environment.\n\n"
            "4.  **Lists:**\n"
            "    *   Convert unordered lists (`*`, `-`, `+`) to `itemize` environments.\n"
            "    *   Convert ordered lists (`1.`, `2.`) to `enumerate` environments.\n"
            "    *   Handle nested lists correctly.\n\n"
            "5.  **Code Blocks:**\n"
            "    *   For fenced code blocks (e.g., ```python ... ```), use the `verbatim` environment. If a language is specified, you can optionally use the `minted` package syntax if you think it's appropriate, but `verbatim` is a safe default. Assume `minted` is loaded if you use it.\n\n"
            "6.  **Links & Images:**\n"
            "    *   Convert `[link text](url)` to `\\href{url}{link text}`.\n"
            "    *   Convert `![alt text](image_path)` to a `figure` environment with `\\includegraphics{image_path}` and `\\caption{alt text}`. **Crucially, the `image_path` must be preserved exactly as provided in the Markdown.**\n\n"
            "7.  **Tables:**\n"
            "    *   Convert Markdown tables into LaTeX `tabular` environments within a `table` float if appropriate. Pay attention to column alignment (left, center, right) as indicated by Markdown syntax (e.g., `|:---|:---:|---:|`). Use `\\raggedright`, `\\centering`, `\\raggedleft` within `p{}` columns if needed, or simply `l`, `c`, `r` for fixed alignment.\n\n"
            "8.  **Blockquotes:**\n"
            "    *   Convert Markdown blockquotes (`> `) to the `quote` environment.\n\n"
            "9.  **Horizontal Rules:**\n"
            "    *   Convert Markdown horizontal rules (`---`, `***`, `___`) to `\\\\hrulefill`.\n\n"
            "10. **Robustness & HTML:**\n"
            "    *   The input might be poorly formatted. Do your best to interpret the user's intent and produce clean LaTeX.\n"
            "    *   Handle simple HTML tags: `<b>` to `\\textbf{}`, `<i>` to `\\textit{}`, `<u>` to `\\underline{}`. Other complex HTML should be ignored or converted to a reasonable LaTeX equivalent if possible.\n\n"
            "**Final Output Instruction:**\n"
            "Your response must ONLY contain the LaTeX code snippet, without any additional conversational text, explanations, or Markdown fences (e.g., ```latex). Do not wrap the LaTeX in any other characters or formatting."
        )

        # 3. Add extra user instructions if present
        if 'extra_instructions' in metadata:
            system_instruction += f"\nUSER SPECIAL INSTRUCTIONS:\n{metadata['extra_instructions']}\n"

        full_prompt = system_instruction + "\n\nMARKDOWN CONTENT:\n"

        # 4. Call LLM
        tex_content = self.client.generate_latex(full_prompt, content)

        # 5. Clean up the response
        tex_content = tex_content.strip()
        if tex_content.startswith("```latex"):
            tex_content = tex_content[8:].lstrip()
        if tex_content.endswith("```"):
            tex_content = tex_content[:-3].rstrip()

        # 6. Write Output
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w') as f:
            f.write(tex_content)
        
        return output_path

    def create_root_file(self, metadata, content_filenames):
        """
        Reads the template and fills in metadata title/author.
        """
        if self.template_path:
            template_path = self.template_path
        else:
            template_path = os.path.join("templates", "main.tex")

        try:
            with open(template_path, 'r') as f:
                template = f.read()
        except FileNotFoundError:
            print(f"Error: Template file not found at {template_path}")
            return None

        # Replace placeholders
        title = metadata.get('title', 'Untitled Document')
        author = metadata.get('author', 'Anonymous')
        
        # Generate the \input commands for each content file
        input_commands = ""
        for filename in content_filenames:
            input_commands += f"\\input{{{filename}}}\n"

        final_tex = template.replace('((TITLE))', title)
        final_tex = final_tex.replace('((AUTHOR))', author)
        final_tex = final_tex.replace('((CONTENT_FILES))', input_commands)

        root_filename = "main.tex"
        output_path = os.path.join(self.output_dir, root_filename)
        with open(output_path, 'w') as f:
            f.write(final_tex)
            
        return output_path
