import os
import re
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
            '###': 'subsubsection',
            '####': 'paragraph*'
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
            "1.  **Document Structure & Numbering:**\n"
            "    *   Analyze the Markdown heading hierarchy (`#`, `##`, `###`) to infer the structure.\n"
            "    *   **Strictly adhere to the following mapping:**\n"
            "        " + str(structure_map) + "\n"
            "    *   **CRITICAL: Avoid Double Numbering.** LaTeX automatically numbers sections. If the Markdown header text starts with a number, label, or index (e.g., '1. Introduction', '2.3 Methodology', 'Part 1: Abstract'), **you must remove the leading number/label** from the title text inside the LaTeX command.\n"
            "    *   **CRITICAL RULE:** If a list item content starts with a square bracket `[` (e.g., `* [Draft]`), you MUST output it as `\\item {[Draft]...}` or `\\item {[}Draft]...`. If you output `\\item [Draft]`, LaTeX will treat it as a label, not text.\n" 
            "        *   *Bad:* `## 2. Methods` -> `\\subsection{2. Methods}` (Result: 2. 2. Methods)\n"
            "        *   *Good:* `## 2. Methods` -> `\\subsection{Methods}` (Result: 2. Methods)\n"
            "    *   The output should ONLY be the body content. Do NOT include `\\documentclass`, `\\begin{document}`, or `\\end{document}`.\n\n"
            "2.  **Text Formatting:**\n"
            "    *   Convert `**bold**` and `__bold__` to `\\textbf{bold}`.\n"
            "    *   Convert `*italic*` and `_italic_` to `\\textit{italic}`.\n"
            "    *   Convert `~~strikethrough~~` to `\\sout{strikethrough}`.\n"
            "    *   Convert inline `code` to `\\texttt{code}`.\n\n"
            "3.  **Math:**\n"
            "    *   Convert inline math (e.g., `$E=mc^2$`) to `$...$`.\n"
            "    *   Convert display math to `\\[ ... \\]` environment.\n\n"
            "4.  **Lists:**\n"
            "    *   Convert `*`, `-` to `itemize`.\n"
            "    *   Convert `1.` to `enumerate`.\n"
            "    *   **CRITICAL: Use correct LaTeX environment closing syntax.** For example, always use `\\end{itemize}` and `\\end{enumerate}`, avoiding `\\end{{itemize}` or `\\end{{enumerate}` typos.\n\n"
            "5.  **Code Blocks:**\n"
            "    *   Use `verbatim` environment for code blocks.\n\n"
            "6.  **Links & Images:**\n"
            "    *   Convert `[text](url)` to `\\href{url}{text}`.\n"
            "    *   Convert `![alt](path)` to `figure` with `\\includegraphics{path}` and `\\caption{alt}`. Preserve `path` exactly.\n\n"
            "7.  **Tables:**\n"
            "    *   Convert to `tabular` inside `table` float if appropriate. Respect alignment.\n\n"
            "8.  **Blockquotes & Rules:**\n"
            "    *   `> ` to `quote` environment.\n"
            "    *   `---` to `\\hrulefill`.\n\n"
            "9.  **Robustness:**\n"
            "    *   Handle poor formatting gracefully. Interpret user intent.\n"
            "    *   ONLY return the LaTeX code. No Markdown fences.\n"
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
        
        # Fix common LLM typo: \end{{itemize} -> \end{itemize}
        tex_content = re.sub(r'\\end\{\{itemize\}', r'\\end{itemize}', tex_content)
        tex_content = re.sub(r'\\end\{\{enumerate\}', r'\\end{enumerate}', tex_content)

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
            # Fallback template if file is missing
            template = (
                "\\documentclass{article}\n"
                "\\usepackage{graphicx}\n"
                "\\usepackage{hyperref}\n"
                "\\usepackage{soul}\n"
                "\\usepackage{amsmath}\n"
                "\\title{((TITLE))}\n"
                "\\author{((AUTHOR))}\n"
                "\\begin{document}\n"
                "\\maketitle\n"
                "((CONTENT_FILES))\n"
                "\\end{document}"
            )

        # Replace placeholders
        title = metadata.get('title', 'Untitled Document')
        author = metadata.get('author', 'Anonymous')
        
        # Generate the \input commands for each content file
        input_commands = ""
        for filename in content_filenames:
            # Ensure we only input the filename, not the full path if it's in the same dir
            # But usually input uses relative paths. Assuming flat structure here.
            fname_only = os.path.basename(filename) 
            input_commands += f"\\input{{{fname_only}}}\n"

        final_tex = template.replace('((TITLE))', title)
        final_tex = final_tex.replace('((AUTHOR))', author)
        final_tex = final_tex.replace('((CONTENT_FILES))', input_commands)

        root_filename = "main.tex"
        output_path = os.path.join(self.output_dir, root_filename)
        with open(output_path, 'w') as f:
            f.write(final_tex)
            
        return output_path
