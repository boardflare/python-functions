import os
from pathlib import Path
import json

# Root directory for functions
FUNCTIONS_DIR = Path(__file__).parent.parent / 'functions'
OUTPUT_MDX = FUNCTIONS_DIR / 'demos_gradio.mdx'

# Helper to escape triple backticks for MDX safety
def escape_backticks(code):
    return code.replace('```', '\u0060\u0060\u0060')

# Collect demos by section (folder)
demos_by_section = {}

for root, dirs, files in os.walk(FUNCTIONS_DIR):
    for file in files:
        if file.startswith('gradio_') and file.endswith('.py'):
            func_dir = Path(root)
            func_name = func_dir.name
            section = func_dir.parent.name.capitalize()  # e.g., 'text' -> 'Text'
            demo_files = []
            # Main gradio demo file
            py_demo = func_dir / file
            demo_files.append({
                "name": file,
                "content": escape_backticks(py_demo.read_text(encoding='utf-8')),
                "entrypoint": True
            })
            # Add ai_ask.py or similar implementation file if present
            impl_file = func_dir / f"{func_name}.py"
            if impl_file.exists():
                demo_files.append({
                    "name": f"{func_name}.py",
                    "content": escape_backticks(impl_file.read_text(encoding='utf-8'))
                })
            # Add test_cases.json if present
            test_cases = func_dir / "test_cases.json"
            if test_cases.exists():
                demo_files.append({
                    "name": "test_cases.json",
                    "content": escape_backticks(test_cases.read_text(encoding='utf-8'))
                })
            # Store by section and function
            demos_by_section.setdefault(section, []).append((func_name, demo_files))

# Compose MDX output to match the working demos_gradio.mdx exactly
header = (
    'import GradioLiteDemo from "../../../components/GradioLiteDemo.jsx"\n\n'
    '# Demos\n\n'
)

mdx_sections = [header]

for section in sorted(demos_by_section.keys()):
    mdx_sections.append(f"## {section}\n")
    for func_name, demo_files in sorted(demos_by_section[section]):
        files_json = json.dumps(demo_files, indent=2)
        mdx_sections.append(f"### {func_name.upper()}\n\n<GradioLiteDemo files={{ {files_json} }} />\n")

with open(OUTPUT_MDX, 'w', encoding='utf-8') as f:
    for sec in mdx_sections:
        f.write(sec)

print(f"Wrote Gradio Lite demos MDX to {OUTPUT_MDX}")
