import os
import json
import shutil
from pathlib import Path
import nbformat
import ast
import subprocess

def extract_code_cells(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    return [cell['source'] for cell in nb.cells if cell.cell_type == 'code']

def extract_function_metadata(nb_path):
    code_cells = extract_code_cells(nb_path)
    if not code_cells:
        return None
    try:
        tree = ast.parse(code_cells[0])
        func_node = next((n for n in tree.body if isinstance(n, ast.FunctionDef)), None)
        if not func_node:
            return None
        func_name = func_node.name
        docstring = ast.get_docstring(func_node) or ""
        arg_names = [arg.arg for arg in func_node.args.args]
        description = docstring.split('\n')[0].strip() if docstring else ""
    except Exception:
        return None
    # Try to extract demo_cases from any cell
    demo_examples = None
    for code in code_cells:
        try:
            tree = ast.parse(code)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "demo_cases":
                            if isinstance(node.value, ast.List):
                                demo_examples = ast.literal_eval(node.value)
                                break
            if demo_examples:
                break
        except Exception:
            continue
    test_cases = []
    if demo_examples:
        # Only use the first demo_case element
        example = demo_examples[0] if len(demo_examples) > 0 else None
        if example and isinstance(example, (list, tuple)) and len(example) >= 2:
            *inputs, expected_output = example
            arguments = dict(zip(arg_names, inputs if len(inputs) > 1 else inputs[0] if isinstance(inputs[0], (list, tuple)) else inputs))
            test_cases.append({
                "id": f"test_{func_name}_1",
                "description": f"Demo example 1",
                "arguments": arguments,
                "expected_output": expected_output,
                "demo": True
            })
    return {
        "name": func_name,
        "description": description,
        "docstring": docstring,
        "code": code_cells[0],
        "test_cases": test_cases
    }

def clean_dir(path):
    if path.exists() and path.is_dir():
        shutil.rmtree(path)

def copy_first_two_cells(src, dest):
    with open(src, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    nb.cells = nb.cells[:2]
    with open(dest, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

def main():
    root = Path(__file__).resolve().parent.parent
    files_dir = root / "files"
    notebooks_dir = root / "notebooks"
    public_dir = root / "public"
    # 1. Clean files dir
    clean_dir(files_dir)
    # 2. Extract metadata
    functions = []
    index = 1
    for nb_file in notebooks_dir.rglob("*.ipynb"):
        rel_parts = nb_file.relative_to(notebooks_dir).parts
        if any(part.startswith("_") for part in rel_parts[:-1]) or nb_file.parent == notebooks_dir or nb_file.name.startswith("test_"):
            continue
        meta = extract_function_metadata(nb_file)
        if meta:
            meta["fileId"] = str(index)
            index += 1
            rel_path = nb_file.relative_to(notebooks_dir).parent
            parent_name = rel_path.name
            file_stem = nb_file.stem
            if rel_path == Path('.'):
                link_path = meta['name']
            elif parent_name == file_stem:
                link_path = str(rel_path).replace('\\', '/')
            else:
                link_path = f"{str(rel_path).replace('\\', '/')}/{meta['name']}"
            meta["link"] = f"https://www.boardflare.com/python-functions/{link_path}"
            meta["folder"] = rel_path.parts[-2] if parent_name == file_stem and len(rel_path.parts) > 1 else rel_path.parts[-1] if len(rel_path.parts) > 0 else ''
            functions.append(meta)
    functions.sort(key=lambda x: x["name"])
    public_dir.mkdir(exist_ok=True)
    with open(public_dir / "example_functions.json", 'w', encoding='utf-8') as f:
        json.dump(functions, f, indent=2)
    # 3. Copy first two cells of each notebook
    files_dir.mkdir(parents=True, exist_ok=True)
    for item in notebooks_dir.iterdir():
        dest = files_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
            for nb_file in dest.rglob("*.ipynb"):
                src_nb_file = item / nb_file.relative_to(dest)
                copy_first_two_cells(src_nb_file, nb_file)
        elif item.is_file() and item.suffix == ".ipynb":
            copy_first_two_cells(item, dest)
    # 4. Remove .pytest_cache folders
    for cache_dir in files_dir.rglob(".pytest_cache"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir)
    # 5. Clean public dir except example_functions.json
    for item in public_dir.iterdir():
        if item.name != "example_functions.json":
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    # 6. Build jupyter lite
    result = subprocess.run(["jupyter", "lite", "build"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("jupyter lite build failed")

if __name__ == "__main__":
    main()