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
    functions_dir = Path(__file__).resolve().parent.parent / "functions"
    results = {}
    found_files = list(functions_dir.rglob("*.ipynb"))
    processed = 0
    for nb_file in found_files:
        # if processed >= 5:
        #     break
        # Read notebook and prepend actual external requirements to first code cell
        nb = nbformat.read(str(nb_file), as_version=4)
        first_cell = next((c for c in nb.cells if c.cell_type == 'code'), None)
        if first_cell:
            imports_set = get_imports_from_code(first_cell.source)
            external_pkgs = [mod for mod in sorted(imports_set) if categorize_module(mod) == 'external']
            if external_pkgs:
                first_cell.source = (
                    "# List required external packages, must be pyodide built-ins or pure python\n"
                    f"requirements = {external_pkgs}\n\n"
                    + first_cell.source
                )
                # only write back if there are external packages
                with open(nb_file, 'w', encoding='utf-8') as f:
                    nbformat.write(nb, f)
                processed += 1

        # Only analyze the first code cell for imports
        code_cells = extract_code_cells(nb_file)
        first_code = code_cells[0] if code_cells else ''
        imports_set = get_imports_from_code(first_code)

        categorized = {'built_in': [], 'external': [], 'unknown': []}
        for mod in sorted(imports_set):
            cat = categorize_module(mod)
            categorized[cat].append(mod)

        results[str(nb_file.relative_to(functions_dir))] = categorized

    out_path = Path(__file__).resolve().parent / "imports_summary.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Import summary written to {out_path}")


if __name__ == "__main__":
    main()