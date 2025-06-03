# List imports in function notebooks and categorize imports as built-in, external, or unknown.
import sys
import json
import importlib.util
from pathlib import Path
import nbformat
import ast

def extract_code_cells(nb_path):
    """Extract code cell sources from a notebook."""
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    return [cell['source'] for cell in nb.cells if cell.cell_type == 'code']


def get_imports_from_code(code):
    """Parse code and return a set of top-level imported module names."""
    imports = set()
    try:
        tree = ast.parse(code)
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception:
        pass
    return imports


def categorize_module(mod_name):
    """Categorize a module as built_in, external, or unknown using Python 3.10+ stdlib names."""
    # Preferred Python 3.10+ approach: stdlib and builtins
    if mod_name in sys.stdlib_module_names or mod_name in sys.builtin_module_names:
        return 'built_in'
    # Fallback: check if it's importable
    spec = importlib.util.find_spec(mod_name)
    if spec is None:
        return 'unknown'
    return 'external'


def main():
    functions_dir = Path(__file__).resolve().parent.parent / "notebooks"
    all_imports = set()
    found_files = list(functions_dir.rglob("*.ipynb"))
    for nb_file in found_files:
        code_cells = extract_code_cells(nb_file)
        for code in code_cells:
            imports_set = get_imports_from_code(code)
            all_imports.update(imports_set)

    out_path = Path(__file__).resolve().parent / "requirements.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        for pkg in sorted(all_imports):
            f.write(f"{pkg}\n")
    print(f"All imports written to {out_path}")


if __name__ == "__main__":
    main()