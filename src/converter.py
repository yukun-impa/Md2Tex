import os
from src.llm_client import LLMClient

class Converter:
    def __init__(self, output_dir="output"):
        self.client = LLMClient()
        self.output_dir = output_dir
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
            "**Conversion Rules & Guidelines:**\n\n"
            "1.  **Document Structure:**\n"
            "    *   Analyze the Markdown heading hierarchy (`#`, `##`, `###`, etc.) to infer the document structure.\n"
            "    *   Use appropriate LaTeX sectioning commands (`\\section`, `\\subsection`, `\\subsubsection`, `\\paragraph`).\n"
            "    *   If the structure is inconsistent (e.g., a `###` follows a `#`), make a logical choice to create a clean LaTeX structure. Do not blindly follow the Markdown.\n"
            "    *   The output should ONLY be the body content. Do NOT include `\\documentclass`, `\\begin{document}`, or `\\end{document}`.\n\n"
            "2.  **Text Formatting:**\n"
            "    *   Convert `**bold**` and `__bold__` to `\\textbf{bold}`.\n"
            "    *   Convert `*italic*` and `_italic_` to `\\textit{italic}`.\n"
            "    *   Convert `~~strikethrough~~` to `\\sout{strikethrough}`.\n"
            "    *   Convert inline `code` to `\\texttt{code}`.\n\n"
            "3.  **Lists:**\n"
            "    *   Convert unordered lists (`*`, `-`, `+`) to `itemize` environments.\n"
            "    *   Convert ordered lists (`1.`, `2.`) to `enumerate` environments.\n"
    		"    *   Handle nested lists correctly.\n\n"
            "4.  **Code Blocks:**\n"
            "    *   For fenced code blocks (e.g., ```python ... ```), use the `verbatim` environment. If a language is specified, you can optionally use the `minted` package syntax if you think it's appropriate, but `verbatim` is a safe default.\n\n"
            "5.  **Links & Images:**\n"
            "    *   Convert `[link text](url)` to `\\href{url}{link text}`.\n"
            "    *   Convert `![alt text](image_path)` to a `figure` environment with `\\includegraphics{image_path}` and `\\caption{alt text}`.\n\n"
            "6.  **Tables:**\n"
            "    *   Convert Markdown tables into LaTeX `tabular` environments within a `table` float if appropriate.\n\n"
            "7.  **Robustness:**\n"
            "    *   The input might be poorly formatted. Do your best to interpret the user's intent and produce clean LaTeX.\n"
            "    *   Handle mixed HTML and Markdown gracefully, converting simple tags like `<b>` or `<i>` if possible.\n"
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
        template_path = os.path.join("templates", "main.tex")
        with open(template_path, 'r') as f:
            template = f.read()

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
