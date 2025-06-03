# Function Notebook Creation Guidelines

## Overview

You are creating a Jupyter notebook for a Python function used as a custom function in Excel. The notebook must serve as the single source of truth for documentation, implementation, testing, and Gradio demo. Carefully follow the instructions and coding guidelines below.

## Notebook Structure

Load this [example notebook template](../../functions/financial/tax_rebalancer.ipynb) as a reference.
The notebook should contain the following cells in this order:

### Documentation (Markdown Cell)
- Title is the Excel function name in uppercase (e.g., `# TAX_EFFICIENT_REBALANCER`).
- Provide an `## Overview` section with the function’s purpose and why it is useful.  This should include a detailed background of any algorithms used, if relevant, using equations where appropriate with inline latex math formatting only with $...$ delimiters..
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

- Include a `## Notes` section with any limitations or important notes about the function.
- Include a `## Examples` section with realistic, business-focused examples of how to use the function in Excel.
  - Provide at least two examples with sample input, function call, and expected output.
  - Where args or returns are lists, provide example values in a table format and reference ranges in the Excel formula examples.
  - Ensure examples are clear and demonstrate practical use cases.

### Function Implementation (Python Cell)
- The function name must be a lowercase of the Excel function name used in the documentation.
- Include a Google-style docstring with no examples.
- Do not put imports in try except blocks.
- For HTTP requests, use the `requests` library.
- Args and returns may be only list[list[]] or scalars, with types of float, bool, str, None.
- Variable arguments (`*args`, `**kwargs`) are not allowed.
- Function parameter names cannot contain numbers.
- Do not add comments before the function definition.
- Return error messages as strings instead of raising exceptions.
- If a function generates a plot, return it as a data URL.  For example:
   ```python
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

### Unit Tests (Python Cell)
- Use `ipytest` for in-notebook testing.
- Write separate test functions for each test case.
- Cover both success and failure paths.
- Use only generic assertions (type checks, non-emptiness, structure, approximate value checks).
- Avoid content-specific assertions.
- Do not mock external APIs; use live calls with placeholder/test keys.
- Demo test cases must be realistic and business-focused.

### Gradio Demo (Python Cell)
- Use `gr.Interface()` for the demo.
- Use the function defined in the implementation cell, do not wrap it in another function.
- Examples shoud be the same as those in the documentation.
- Set `flagging_mode='never'` to disable flagging.
- Call `demo.launch()` at the end of the cell.

## Process

After creating the notebook, follow these steps to ensure correctness and usability:

1. **Run All Cells**
   - Execute each cell in the notebook sequentially to ensure there are no errors and all outputs are as expected.

2. **Validate Unit Tests**
   - Confirm that all unit tests pass successfully. If any test fails, debug and update the implementation or tests as needed, then rerun the tests.

3. **Review Documentation**
   - Ensure the documentation cell is clear, complete, and matches the function implementation and test cases.

4. **Final Review**
   - Review the entire notebook for logical flow, formatting, and adherence to all coding guidelines.
   - Make any necessary corrections to ensure the notebook is ready for use in Excel and as a standalone reference.

## Other

Guidelines:
- Markdown cell: Use the same headings and content formatting as the example notebook. When there is a conflict between the formatting of the markdown file and the example notebook provided, use the formatting from the example notebook. Omit any content that does not fit the format provided in the example notebook.
- Test cell: Use ipytest with separate test functions as shown in the notebook. Do not import the old test_cases.json or use parameterized tests.  Make sure to inject the token as shown in the example notebook.
- Gradio cell: Examples should exactly match those provided in the markdown cell.  Use the function directly, do not wrap. Set default values for inputs to same as the first example.  Ensure all arguments in the examples and defaults have a value set - do not leave any as `None` or empty.
- Do NOT add a code cell for example usage.
- Do NOT add comments to the top of the code cells

DO NOT use any tools that run terminal commands.
