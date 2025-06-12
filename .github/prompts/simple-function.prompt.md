# Function Notebook Guidelines

## Overview

These are guidelines for creating or editing the Jupyter notebook which contains a Python function to be used as a custom function in Excel. The notebook must serve as the single source of truth for documentation, implementation, testing, and Gradio demo. Carefully follow the instructions and coding guidelines below.

## Notebook Structure

The notebook must follow this structure and style, as shown in the psychrometrics.ipynb example:

### 1. Documentation (Markdown Cell)
- Title is the Excel function name in uppercase (e.g., `# TAX_EFFICIENT_REBALANCER`).
- Provide an `## Overview` section with the function’s purpose, background, and any relevant equations (use LaTeX math with `$...$` for inline and triple-backtick math blocks for display equations).  The following sentence should be included at the end of the overview: "This example function is provided as-is without any representation of accuracy."
- Include a `## Usage` section with a brief description of how to use the function in Excel and the function signature, where optional arguments are in square brackets. 
- List each argument in a bulleted list under Usage, with type and whether required/optional, description, and an example value.
- The function return type and behavior should be described in a short paragraph at the end of Usage.

For example:
  ```excel
  =BLACK_SCHOLES(S, K, T, r, sigma, [option_type])
  ```
   - `S` (float, required): Current stock price. Example: `100`
   - `K` (float, required): Strike price of the option. Example: `100`
   - `T` (float, required): Time to expiration in years. Example: `1`
   - `r` (float, required): Risk-free interest rate. Example: `0.05`
   - `sigma` (float, required): Volatility of the stock. Example: `0.2`
   - `option_type` (string, optional): Type of option ("call" or "put"). Example: `"call"`

   The function returns the Black-Scholes option price as a float.

- Ensure JSX or HTML characters outside code blocks are wrapped in backticks. E.g. `{2,3}` or `<=`.
- Include a `## Examples` section similar to the following format:

    ## Examples

    **Example 1: Resource Allocation (Minimize Cost)**

    This example minimizes the cost function $3x_1 + 5x_2$ subject to two inequality constraints:
    - $x_1 + 2x_2 \geq 8$
    - $2x_1 + x_2 \geq 8$

    In Excel:
    ```excel
    =LINEAR_PROG({3,5}, {-1,-2;-2,-1}, {-8;-8})
    ```
    Expected output:

    | x1  | x2  | Optimal Value |
    |-----|-----|---------------|
    | 2.0 | 3.0 | 21.0          |

    This means the minimum cost is 21.0 when $x_1 = 2.0$ and $x_2 = 3.0$.

    **Example 2: Diet Problem (Maximize Protein)**

    This example maximizes $x_1 + x_2$ (by minimizing $-x_1 - x_2$) subject to $x_1 + 2x_2 \leq 10$.

    In Excel:
    ```excel
    =LINEAR_PROG({-1,-1}, {1,2}, {10})
    ```
    Expected output:

    | x1   | x2   | Optimal Value |
    |------|------|---------------|
    | 10.0 | 0.0  | -10.0         |

    This means the maximum sum $x_1 + x_2$ is 10.0 (since the optimal value is the negative of the sum), achieved when $x_1 = 10.0$ and $x_2 = 0.0$.

### 2. Function Implementation (Python Cell)
- The function name must be a lowercase version of the Excel function name used in the documentation.
- Include a Google-style docstring with no examples.  Docstring description should have the following sentences at the end:  This example function is provided as-is without any representation of accuracy.
- Do not put imports in try/except blocks.
- For HTTP requests, use the `requests` library.
- For API calls, use api_key as arguments, not environment variables.
- Args and returns may be only list[list] or scalars, with types of float, bool, str, or None.
- Each arg should only accept a scalar or a 2D list of scalars, not both.
- Variable arguments (`*args`, `**kwargs`) are not allowed.
- Parameter names cannot contain numbers, use x_zero instead of x0, for example.
- Do not add comments before the function definition.
- Return error messages as str or list[list[str]] depending on output type instead of raising exceptions.
- Do not add any code for example usage.
- Where the function is wrapping an existing library function, do not use an alias import, and minimize the amount of pre and post processing of inputs and outputs.
- If a function generates a plot, return should only be a str with a data URL or error.  For example:
   ```python
   options = {"insert_only":True} # Add to top of the cell
   import matplotlib
   matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   import io
   import base64

   def example_chart():
      plt.plot([1], [2], 'ro')
      buf = io.BytesIO()
      plt.savefig(buf, format='png')
      plt.close()
      img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
      return f"data:image/png;base64,{img_b64}"
   ```
- If when the function is run, an error is thrown that an imported module is not found, install it using the following syntax:
   ```python
   import micropip
   await micropip.install('textdistance')
   ```

### 3. Unit Tests (Python Cell)
- Add a `demo_cases` variable with a list of parameterized test cases which will also be used for Gradio examples, so need to be in the Gradio examples format.  It must include all optional arguments and the last item in the array for each case should be the expected output.
- Use `demo_cases` in a parameterized test function to validate the function output types using the exact `is_valid_type()` function provided in the example below.
- Add additional test functions for invalid inputs.

For example:
```python
%pip install -q ipytest
import ipytest
ipytest.autoconfig()
import pytest

demo_cases = [
    ["x**2 + 3*x + 2", [[-1000, 1000]], "bounded", [[-1.5, -0.25]]],
    ["(x-5)**2 + 10", [[0, 10]], "bounded", [[5.0, 10.0]]],
    ["x**2 + 3*x + 2", [[-10, 10]], "bounded", [[-1.5, -0.25]]]
]

def approx_equal(a, b, rel=0.05, abs_tol=1e-4):
    # Scalar float only
    if isinstance(a, float) and isinstance(b, float):
        return a == pytest.approx(b, rel=rel, abs=abs_tol)
    # 2D list of floats only
    if (
        isinstance(a, list) and isinstance(b, list)
        and all(isinstance(x, list) for x in a)
        and all(isinstance(y, list) for y in b)
    ):
        return all(
            all(isinstance(x, float) and isinstance(y, float) and x == pytest.approx(y, rel=rel, abs=abs_tol) for x, y in zip(row_a, row_b))
            for row_a, row_b in zip(a, b)
        )
    return False

@pytest.mark.parametrize("func_expr, bounds, method, expected", demo_cases)
def test_demo_cases(func_expr, bounds, method, expected):
    result = minimize_scalar(func_expr, bounds, method)
    print(f"test_demo_cases output for {func_expr}: {result}")
    assert approx_equal(result, expected, rel=0.05), f"Output {result} not within 5% of expected {expected}"

def test_invalid_expression():
    result = minimize_scalar("x***2 + 3x + 2", None, None)
    assert isinstance(result, str) and ("error" in result.lower() or "must be" in result.lower())

def test_missing_x():
    result = minimize_scalar("5 + 7", None, None)
    assert isinstance(result, str) and ("function expression must contain" in result.lower())

ipytest.run('-s')
```

### 4. Gradio Demo (Python Cell)
- Use `gr.Interface()` to create a Gradio demo.
- Set `flagging_mode='never'` and `fill_width=True`.
- For 2D list inputs or outputs, use `gr.DataFrame()` with `type="array"`.  Use headers if the inputs or outputs have a consistent structure.
- Add a description to the Gradio interface that matches the documentation (without latex markup), but no title. Include the sentence "This demo is provided as-is without any representation of accuracy." at the end of the description.
- Set input values set to those of the first demo_case by referencing `demo_cases[0][0]`, etc..
- Use the demo_cases variable defined in the test cell, do not redefine it in the Gradio demo cell.
- Gradio wrapper functions should be used to handle dataframe inputs so that an empty dataframe is correctly passed as `None` to the function, and array elements are converted to floats where necessary.  If informative, the wrapper function should also generate a plot using `gr.HTML()` to display the chart image as a data URL.

For example:
```python
import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def gradio_minimize_scalar(func_expr, bounds, method):
    print(f"gradio_minimize_scalar args: func_expr={func_expr}, bounds={bounds}, method={method}")
    # Convert bounds to float if possible for both plotting and minimize_scalar
    bounds_float = None
    if bounds and isinstance(bounds, list) and len(bounds) == 1 and len(bounds[0]) == 2:
        try:
            min_b = float(bounds[0][0])
            max_b = float(bounds[0][1])
            bounds_float = [[min_b, max_b]]
        except Exception:
            bounds_float = None
    else:
        bounds_float = None

    result = minimize_scalar(func_expr, bounds_float, method)
    # Prepare plot
    x_vals = np.linspace(-10, 10, 400)
    if bounds_float:
        x_vals = np.linspace(bounds_float[0][0], bounds_float[0][1], 400)
    y_vals = []
    for x in x_vals:
        try:
            y = eval(func_expr, {"x": x, "math": __import__('math')})
        except Exception:
            y = np.nan
        y_vals.append(y)
    plt.figure(figsize=(6, 4))
    plt.plot(x_vals, y_vals, label="f(x)")
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list) and len(result[0]) == 2:
        min_x, min_y = result[0]
        plt.scatter([min_x], [min_y], color="red", label="Minimum")
        plt.annotate(f"min=({min_x:.3g}, {min_y:.3g})", (min_x, min_y), textcoords="offset points", xytext=(0,10), ha='center', color='red')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Function Minimization")
    plt.legend()
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    img_html = f'<img src="data:image/png;base64,{img_base64}" style="max-width:100%;height:auto;" />'
    # Prepare result table or error
    if isinstance(result, str):
        result_html = f'<div style="color:red;font-weight:bold;">{result}</div>'
    else:
        result_html = f'<table border="1" style="border-collapse:collapse;"><tr><th>x</th><th>f(x)</th></tr>'
        for row in result:
            result_html += f'<tr><td>{row[0]:.6g}</td><td>{row[1]:.6g}</td></tr>'
        result_html += '</table>'
    return img_html + result_html

demo = gr.Interface(
    fn=gradio_minimize_scalar,
    inputs=[
        gr.Textbox(label="Function Expression", value=demo_cases[0][0]),
        gr.DataFrame(headers=["min", "max"], label="Bounds (optional)", row_count=1, col_count=2, type="array", value=demo_cases[0][1]),
        gr.Dropdown(
            choices=["brent", "bounded", "golden"],
            label="Method (optional)",
            value=demo_cases[0][2],
            allow_custom_value=False,
        ),
    ],
    outputs=gr.HTML(label="Plot and Result"),
    examples=demo_cases,
    description="Find the minimum of a scalar function f(x), where x is a real number. Provide the function as a string in terms of x, with optional bounds and method. This demo is provided as-is without any representation of accuracy.",
    flagging_mode="never",
    fill_width=True,
)
demo.launch()
```

## Process

After creating the notebook, use the run the test notebook cell so that you can see the output, and either fix the function or update the expected result in demo_cases accordingly if the function appears to be working properly. 

If you make changes to the function implementation cell during debugging, ensure you update the documentation and gradio demo cells as needed.
