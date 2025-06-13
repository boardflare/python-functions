import nbformat
from pathlib import Path

def process_notebook(nb_path):
    nb = nbformat.read(open(nb_path, encoding='utf-8'), as_version=4)
    code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
    if len(code_cells) < 2:
        print(f"{nb_path}: Notebook has fewer than 2 code cells.")
        return False
    # Remove %pip install -q ipytest from 2nd code cell if present
    cell = code_cells[1]
    lines = cell['source'].splitlines()
    filtered_lines = [l for l in lines if l.strip() != '%pip install -q ipytest']
    if len(filtered_lines) != len(lines):
        cell['source'] = '\n'.join(filtered_lines)
        print(f"Removed '%pip install -q ipytest' from 2nd code cell in {nb_path}")
    # Update 2nd code cell for ipytest install
    try:
        idx = next(i for i, line in enumerate(filtered_lines) if 'import ipytest' in line)
    except StopIteration:
        print(f"{nb_path}: 'import ipytest' not found in 2nd code cell.")
        return False
    new_lines = filtered_lines[idx:]
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
