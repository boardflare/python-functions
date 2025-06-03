import nbformat
from pathlib import Path

def process_notebook(nb_path):
    nb = nbformat.read(open(nb_path, encoding='utf-8'), as_version=4)
    code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
    if len(code_cells) < 2:
        print(f"{nb_path}: Notebook has fewer than 2 code cells.")
        return False
    cell = code_cells[1]
    lines = cell['source'].splitlines()
    try:
        idx = next(i for i, line in enumerate(lines) if 'import ipytest' in line)
    except StopIteration:
        print(f"{nb_path}: 'import ipytest' not found in 2nd code cell.")
        return False
    new_lines = lines[idx:]
    if not new_lines or not new_lines[0].startswith('%pip install'):
        new_lines.insert(0, '%pip install -q ipytest')
    cell['source'] = '\n'.join(new_lines)
    nbformat.write(nb, open(nb_path, 'w', encoding='utf-8'))
    print(f"Updated 2nd code cell in {nb_path}")
    return True


def main():
    notebooks_dir = Path(__file__).resolve().parent.parent / "notebooks"
    found_files = list(notebooks_dir.rglob("*.ipynb"))
    if not found_files:
        print("No notebooks found.")
        return
    for nb_file in found_files:
        process_notebook(nb_file)

if __name__ == "__main__":
    main()
