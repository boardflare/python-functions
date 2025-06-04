# Function Notebook Guidelines

## Overview

These are guidelines for creating or editing the Jupyter notebook which contains a Python function to be used as a custom function in Excel. The notebook must serve as the single source of truth for documentation, implementation, testing, and Gradio demo. Carefully follow the instructions and coding guidelines below.

## Notebook Structure

Load this [example notebook template](../../notebooks/optimization/basin_hopping.ipynb) as a reference.
The notebook should contain the following cells in this order:

### Documentation (Markdown Cell)
- Title is the Excel function name in uppercase (e.g., `# TAX_EFFICIENT_REBALANCER`).
- Provide an `## Overview` section with the function’s purpose and why it is useful.  This should include a detailed background of any algorithms used, if relevant, using equations where appropriate.
- Equations should be formatted with latex using `$...$` delimiters for inline, and ```math ``` for equation blocks, not `$$...$$`.
- Include a `## Usage` section with a brief description of how to use the function in Excel and the function signature, where optional arguments are in square brackets. For example:
   ```excel
   =BLACK_SCHOLES(S, K, T, r, sigma, [option_type])
   ```
- Include an `## Arguments` section which lists arguments in a table, including type, required, description, and an example value.  For example:

| Argument | Type | Required | Description | Example |
|:---|:---|:---|:---|:---|
| S | float | Required | Current stock price | 100 |
| K | float | Required | Option strike price | 105 |
| T | float | Required | Time to expiration (in years) | 0.5 |
| r | float | Required | Risk-free interest rate | 0.03 |
| sigma | float | Required | Volatility of the underlying asset | 0.2 |
| option_type | string | Optional | Type of option ("call" or "put") | "call" |

- Include a `## Returns` section with a table describing the return value, including type, description, and an example value. For example:
| Returns | Type | Description | Example |
|:---|:---|:---|:---|
| Price | float | The calculated option price | 4.1783 |
| Error | string | Error message if calculation fails | "Error: Invalid input" |

- Description columns should not include an example value.
- Include a `## Examples` section with realistic, business-focused examples of how to use the function in Excel.
  - Provide at least two examples with sample input, function call, and expected output.
  - Where args or returns are lists, provide example values in a table format and reference ranges in the Excel formula examples.
  - Ensure examples are clear and demonstrate practical use cases.
  - Headings of examples should not include `Example 1`, `Example 2`, etc., but should be descriptive of the example content, such as `### Calculating Option Price` or `### Using with Different Volatilities`.
- Use 2D list syntax `[[1, 2, 3], [4, 5, 6]]` for examples in arg and returns tables, not Excel array constants.
- Ensure JSX or HTML characters outside code blocks are wrapped in backticks. E.g. `{2,3}` or `<=`

### Function Implementation (Python Cell)
- The function name must be a lowercase of the Excel function name used in the documentation.
- Include a Google-style docstring with no examples.
- Do not put imports in try except blocks.
- For HTTP requests, use the `requests` library.
- For API calls, use api_key as arguments, not environment variables.
- Args and returns may be only list[list[]] or scalars, with types of float, bool, str, None.
- Variable arguments (`*args`, `**kwargs`) are not allowed.
- Function parameter names cannot contain numbers, use x_zero instead of x0, for example.
- Do not add comments before the function definition.
- Return error messages as str or list[list[str]] depending on output type instead of raising exceptions.
- Do not add any code for example usage.
- If a function generates a plot, return it as a data URL.  For example:
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

### Unit Tests (Python Cell)
- Use `ipytest` for in-notebook testing.  Install it with `%pip install -q ipytest` at the top of the cell.
- Write separate test functions for each test case.
- Cover both success and failure paths.
- Use only generic assertions (type checks, non-emptiness, structure, approximate value checks).
- Avoid content-specific assertions, especially with stochastic outputs (e.g. LLM, optimization).
- Do not mock external APIs. 
- Demo test cases must be realistic and business-focused.

### Gradio Demo (Python Cell)
- Use `gr.Interface()` for the demo.
- Use the function defined in the implementation cell, do not wrap it in another function, except in the case of a plot, which should use a wrapper similar to the following:
   ```python
   def render_html(data, chart_type, title, xlabel, ylabel):
    result = basic_chart(data, chart_type, title, xlabel, ylabel)
    if isinstance(result, str) and result.startswith("data:image/png;base64,"):
        # Return an HTML <img> tag with the data URL
        return f'<img src="{result}" alt="Chart Image" style="max-width:100%;height:auto;" />'
    return f'<div style="color:red;">{result}</div>'
   ```
- Plots should use `gr.HTML()` to display the chart image.
- Examples shoud be the same as those in the documentation.
- Set `flagging_mode='never'` to disable flagging.
- For 2D list inputs or outputs, use `gr.DataFrame()` with `type="array"`.
- Set default values for all inputs to match the first example in the documentation.
- Add a description to the Gradio interface that matches the documentation.
- Do not add a title to the Gradio interface.
- Call `demo.launch()` at the end of the cell.

## Process

After creating the notebook, use the run notebook cell tools to run all cells, validate unit tests, and review the documentation. If you make changes to the function implementation cell during debugging, ensure you update the documentation and gradio demo cells if needed.
