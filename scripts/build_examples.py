import os
import json
import re
from pathlib import Path
import ast
import nbformat
import shutil
import subprocess

def extract_code_cells(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    code_cells = [cell['source'] for cell in nb.cells if cell.cell_type == 'code']
    return code_cells

def extract_function_info(code):
    """Extract function name, docstring, and argument names from code string."""
    try:
        tree = ast.parse(code)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                docstring = ast.get_docstring(node) or ""
                arg_names = [arg.arg for arg in node.args.args]
                return func_name, docstring, arg_names
    except Exception as e:
        print(f"AST parse error: {e}")
    return None, None, []

def extract_gradio_example(gradio_code):
    """Extract the first 'examples' item from gradio code cell as a Python object using AST parsing."""
    try:
        tree = ast.parse(gradio_code)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "examples":
                        examples = ast.literal_eval(node.value)
                        print(f"Extracted examples from gradio code cell: {examples}")
                        if isinstance(examples, list) and examples:
                            return examples[0]
                        elif isinstance(examples, tuple) and examples:
                            return examples[0]
                        elif examples:
                            return examples
    except Exception as e:
        print(f"Error extracting gradio example with AST: {e}")
    print("No examples found in gradio code cell.")
    return None

def build_test_case_from_example(example, arg_names, func_name=None):
    if example is None:
        return []
    if isinstance(example, (list, tuple)):
        arguments = dict(zip(arg_names, example))
    elif isinstance(example, dict):
        arguments = example
    else:
        return []
    test_case = {
        "id": f"test_{func_name or 'function'}_1",
        "description": "Demo example 1",
        "arguments": arguments,
        "demo": True
    }
    return [test_case]

def get_function_metadata(nb_path):
    try:
        code_cells = extract_code_cells(nb_path)
        if len(code_cells) < 1:
            print(f"No code cells found in {nb_path}")
            return None
        main_code = code_cells[0]
        func_name, docstring, arg_names = extract_function_info(main_code)
        description = docstring.split('\n')[0].strip() if docstring else ""
        gradio_code = code_cells[2] if len(code_cells) > 2 else None
        gradio_example = extract_gradio_example(gradio_code) if gradio_code else None
        test_cases = build_test_case_from_example(gradio_example, arg_names, func_name)
        return {
            "name": func_name or Path(nb_path).stem,
            "description": description,
            "docstring": docstring or "",
            "code": main_code,
            "test_cases": test_cases
        }
    except Exception as e:
        print(f"Error processing {nb_path}: {str(e)}")
        return None

def remove_last_code_cell(nb_path):
    """Remove the last code cell from a notebook file."""
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        # Find the last code cell
        for i in range(len(nb.cells) - 1, -1, -1):
            if nb.cells[i].cell_type == 'code':
                del nb.cells[i]
                break
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
    except Exception as e:
        print(f"Error removing last code cell from {nb_path}: {e}")

def main():
    # Step -1: Delete the files folder if it exists
    files_dir = Path(__file__).resolve().parent.parent / "files"
    if files_dir.exists() and files_dir.is_dir():
        print(f"Deleting {files_dir}...")
        shutil.rmtree(files_dir)
    else:
        print(f"{files_dir} does not exist, skipping delete.")

    # Step 0: Copy all contents of notebooks directory into public/files directory
    notebooks_dir = Path(__file__).resolve().parent.parent / "notebooks"
    files_dir.mkdir(parents=True, exist_ok=True)
    print(f"Copying contents from {notebooks_dir} to {files_dir}...")
    for item in notebooks_dir.iterdir():
        dest = files_dir / item.name
        try:
            print(f"Copying {item} to {dest}...")
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            if item.is_dir():
                shutil.copytree(item, dest)
            elif item.is_file():
                shutil.copy2(item, dest)
            else:
                print(f"Skipping non-file, non-directory: {item}")
        except FileNotFoundError as e:
            print(f"File not found, skipping: {item} ({e})")
        except Exception as e:
            print(f"Error copying {item} to {dest}: {e}")

    # Step 1: Remove all .pytest_cache folders in files directory
    print(f"Searching for .pytest_cache folders in: {files_dir.absolute()}")
    for cache_dir in files_dir.rglob(".pytest_cache"):
        if cache_dir.is_dir():
            print(f"Deleting {cache_dir}...")
            shutil.rmtree(cache_dir)

    # Step 2: Delete the public folder if it exists
    public_dir = Path(__file__).resolve().parent.parent / "public"
    if public_dir.exists() and public_dir.is_dir():
        print(f"Deleting {public_dir}...")
        shutil.rmtree(public_dir)
    else:
        print(f"{public_dir} does not exist, skipping delete.")

    functions_dir = files_dir
    print(f"Searching for Jupyter notebooks in: {functions_dir.absolute()}")
    functions = []
    index = 1
    for nb_file in functions_dir.rglob("*.ipynb"):
        # Skip files in directories starting with underscore
        relative_parts = nb_file.relative_to(functions_dir).parts
        if any(part.startswith("_") for part in relative_parts[:-1]):
            print(f"Skipping file in underscore folder: {nb_file}")
            continue
        # Skip files at the root of functions directory
        if nb_file.parent == functions_dir:
            print(f"Skipping root file: {nb_file.name}")
            continue
        # Skip test notebooks
        if nb_file.name.startswith("test_"):
            continue
        file_path = str(nb_file)
        print(f"Processing {file_path}...")
        metadata = get_function_metadata(file_path)
        if metadata:
            metadata["fileId"] = str(index)
            index += 1
            relative_path = nb_file.relative_to(functions_dir).parent
            parent_name = relative_path.name
            file_stem = nb_file.stem
            if relative_path == Path('.'):
                link_path = metadata['name']
            elif parent_name == file_stem:
                link_path = str(relative_path).replace('\\', '/')
            else:
                replaced_path = str(relative_path).replace('\\', '/')
                link_path = f"{replaced_path}/{metadata['name']}"
            metadata["link"] = f"https://www.boardflare.com/python-functions/{link_path}"
            if parent_name == file_stem and len(relative_path.parts) > 1:
                metadata["folder"] = relative_path.parts[-2]
            elif len(relative_path.parts) > 0:
                metadata["folder"] = relative_path.parts[-1]
            else:
                metadata["folder"] = ''
            functions.append(metadata)
    functions.sort(key=lambda x: x["name"])
    public_dir.mkdir(exist_ok=True)
    output_path = public_dir / "example_functions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(functions, f, indent=2)
    print(f"Generated {output_path} with {len(functions)} functions")

    # Remove the last code cell from each notebook in files_dir (after JSON build)
    print(f"Removing last code cell from notebooks in: {files_dir.absolute()}")
    for nb_file in files_dir.rglob("*.ipynb"):
        try:
            remove_last_code_cell(nb_file)
        except Exception as e:
            print(f"Error processing {nb_file}: {e}")

    # Step 3: Run jupyter lite build (now last)
    print("Running 'jupyter lite build'...")
    result = subprocess.run(["jupyter", "lite", "build"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("jupyter lite build failed")

if __name__ == "__main__":
    main()