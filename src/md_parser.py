import yaml
import re

def parse_markdown(file_path):
    """
    Reads a markdown file and extracts YAML frontmatter and the main content.
    Returns: (metadata_dict, content_string)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex to find YAML frontmatter delimited by ---
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, text, re.DOTALL)

    metadata = {}
    content = text

    if match:
        yaml_text = match.group(1)
        try:
            metadata = yaml.safe_load(yaml_text)
            # Remove the frontmatter from the content
            content = text[match.end():]
        except yaml.YAMLError as e:
            print(f"Warning: Error parsing YAML frontmatter: {e}")

    return metadata, content
