import argparse
import os
import sys
from dotenv import load_dotenv
from src.md_parser import parse_markdown
from src.converter import Converter

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Convert one or more Markdown files to a single LaTeX document.")
    parser.add_argument("input_files", nargs='+', help="Paths to the Markdown files to convert")
    parser.add_argument("--output_dir", default="output", help="Directory to save generated LaTeX files")
    parser.add_argument("--template", help="Path to a custom LaTeX template file")
    args = parser.parse_args()

    generated_tex_files = []
    root_metadata = {}

    converter = Converter(output_dir=args.output_dir, template_path=args.template)

    for input_file in args.input_files:
        if not os.path.isfile(input_file):
            print(f"Error: File {input_file} not found. Skipping.")
            continue

        print(f"--- Converting {input_file} ---")

        # 1. Parse input
        metadata, content = parse_markdown(input_file)
        if metadata and not root_metadata:
            root_metadata = metadata

        # 2. Convert content
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        content_tex_file = f"{base_name}.tex"
        
        converter.convert(metadata, content, filename=content_tex_file)
        generated_tex_files.append(content_tex_file)

    # 3. Generate Root File (main.tex)
    if generated_tex_files:
        root_file_path = converter.create_root_file(root_metadata, content_filenames=generated_tex_files)
        
        print("\nDone! All files converted.")
        print(f"Compile your document at: {root_file_path}")
        print(f"Example command: pdflatex -output-directory={args.output_dir} {root_file_path}")
    else:
        print("No files were converted.")


if __name__ == "__main__":
    main()
