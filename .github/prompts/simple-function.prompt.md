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
- Include a `## Examples` section with a few example inputs and expected outputs, formatted as code blocks.  Use the following format:
  ```excel
  =BLACK_SCHOLES(100, 100, 1, 0.05, 0.2, "call")
  ```
  Expected output: `10.450583572185565`
- If an example outputs a 2D list, format as a markdown table.

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
- Add a `demo_cases` variable with a list of parameterized test cases which will also be used for Gradio examples, so need to be in the Gradio examples format.  It must include all optional arguments with realistic values.
- Use `demo_cases` in a parameterized test function to validate the function output types using the exact `is_valid_type()` function provided in the example below.
- Add additional test functions for invalid inputs.

For example:
```python
%pip install -q ipytest
import ipytest
ipytest.autoconfig()

demo_cases = [
    ["a * x + b", [[1], [2], [3]], [[2], [4], [6]], [[1, 1]], [[0, 0]], [[10, 10]], "trf"],
    ["a * exp(b * x)", [[1], [2], [3]], [[2.7], [7.4], [20.1]], [[1, 1]], [[0, 0]], [[10, 10]], "trf"],
    ["a * x + b", [[1], [2], [3]], [[2], [4], [6]], [[1, 1]], [[0, 0]], [[10, 10]], "trf"]
]

def is_valid_type(val):
    if isinstance(val, (float, bool, str)):
        return True
    if isinstance(val, list):
        return all(isinstance(row, list) and all(isinstance(x, (float, bool, str)) for x in row) for row in val)
    return False

import pytest
@pytest.mark.parametrize("model, xdata, ydata, p_zero, bounds_lower, bounds_upper, method", demo_cases)
def test_demo_cases(model, xdata, ydata, p_zero, bounds_lower, bounds_upper, method):
    result = least_squares(model, xdata, ydata, p_zero, bounds_lower, bounds_upper, method)
    print(f"test_demo_cases output for {model}: {result}")
    assert is_valid_type(result), f"Output type is not valid. Got: {type(result)} Value: {result}"

def test_invalid_method():
    result = least_squares("a * x + b", [[1], [2], [3]], [[2], [4], [6]], [[1, 1]], [[0, 0]], [[10, 10]], "invalid")
    assert isinstance(result, str) and "method" in result

def test_param_mismatch():
    result = least_squares("a * x + b", [[1], [2], [3]], [[2], [4], [6]], [[1]])
    assert isinstance(result, str) and "initial guesses" in result

ipytest.run('-s')
```

### 4. Gradio Demo (Python Cell)
- Use `gr.Interface()` to create a Gradio demo.
- Set `flagging_mode='never'` and `fill_width=True`.
- For 2D list inputs or outputs, use `gr.DataFrame()` with `type="array"`.  Use headers if the inputs or outputs have a consistent structure.
- Add a description to the Gradio interface that matches the documentation, but no title. Include the sentence "This demo is provided as-is without any representation of accuracy." at the end of the description.
- Set input values set to those of the first demo_case by referencing `demo_cases[0][0]`, etc..
- Use the demo_cases variable defined in the test cell, do not redefine it in the Gradio demo cell.

For example:
```python
import gradio as gr

demo = gr.Interface(
    fn=psychrometrics, # Use function directly without wrapper
    inputs=[
        gr.Dropdown(["wetbulb", "dewpoint", "humidityratio", "enthalpy"], label="Calculation Type", value=demo_cases[0][0]),
        gr.Number(label="Dry Bulb Temperature (°C)", value=demo_cases[0][1]),
        gr.Number(label="Relative Humidity (%)", value=demo_cases[0][2]),
        gr.Number(label="Pressure (Pa)", value=demo_cases[0][3]),
    ],
    outputs=gr.Number(label="Result"),
    examples=demo_cases, # Use demo_cases defined in the test cell
    description="Calculate wet bulb, dew point, humidity ratio, or enthalpy using the psychrometrics function.",
    flagging_mode="never",
    fill_width=True,
)

demo.launch()
```

- Use the function defined without a wrapper, except in the case of a plot, which should use a wrapper similar to the following:
   ```python
   def render_html(data, chart_type, title, xlabel, ylabel):
    result = basic_chart(data, chart_type, title, xlabel, ylabel)
    if isinstance(result, str) and result.startswith("data:image/png;base64,"):
        # Return an HTML <img> tag with the data URL
        return f'<img src="{result}" alt="Chart Image" style="max-width:100%;height:auto;" />'
    return f'<div style="color:red;">{result}</div>'
   ```
- Plots should use `gr.HTML()` output to display the chart image.


## Process

After creating the notebook, use the run notebook cell tools to run all cells, validate unit tests, and review the documentation. If you make changes to the function implementation cell during debugging, ensure you update the documentation and gradio demo cells if needed.
