import nbformat
import os
from pathlib import Path
import re

def remove_comments_from_demo_cases(cell_source):
    lines = cell_source.splitlines()
    new_lines = []
    in_demo_cases = False
    bracket_level = 0
    for line in lines:
        if not in_demo_cases and re.match(r"\s*demo_cases\s*=", line):
            in_demo_cases = True
        if in_demo_cases:
            # Remove comments from this line
            code_part = line.split('#', 1)[0].rstrip()
            # Track bracket level to know when demo_cases ends
            bracket_level += code_part.count('[') - code_part.count(']')
            if code_part.strip():
                new_lines.append(code_part)
            if in_demo_cases and bracket_level <= 0:
                in_demo_cases = False
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def process_notebook(nb_path):
    changed = False
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'demo_cases' in cell.source:
            new_source = remove_comments_from_demo_cases(cell.source)
            if new_source != cell.source:
                cell.source = new_source
                changed = True
    if changed:
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Updated: {nb_path}")

def main():
    root = Path("notebooks")
    for nb_file in root.rglob("*.ipynb"):
        process_notebook(nb_file)

if __name__ == "__main__":
    main()
