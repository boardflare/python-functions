For each class init in this document, create a notebook with a function named exactly the same as the class, e.g. class fluids.atmosphere.ATMOSPHERE_1976 would be named ATMOSPHERE_1976 in the notebook, and the class should be imported from fluids.atmosphere.  The notebook should be placed in notebooks/engineering/fluids folder with a lowercase name, e.g. `atmosphere_1976.ipynb`.

## Step 1: Create a checklist document
Create a checklist document in the same folder as the notebook, named after the module being worked on, e.g. `atmosphere-checklist.md`, which keeps track of which notebooks have been created, and which ones are still to be created. 

## Step 2: Create the notebook
For the next item in the checklist, create a Jupyter notebook.  These notebooks contains a Python function to be used as a custom function in Excel. The notebook must serve as the single source of truth for documentation, implementation, testing, and Gradio demo.  Each notebook should follow the following structure:

### Documentation (Markdown Cell)
- Title is the Excel function name in uppercase (e.g., `# TAX_EFFICIENT_REBALANCER`).
- Provide an `## Overview` section with the function’s purpose and why it is useful.  This should include a detailed background of any algorithms used, if relevant, using equations where appropriate.
- Equations should be formatted with latex using `$...$` delimiters for inline, and ```math ``` for equation blocks.  Use exactly the same equations as in the documentation for the class.
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

- Include a `## Examples` section with realistic, business-focused examples of how to use the function in Excel.
  - Provide at least two examples with sample input, function call, and expected output.
  - Where args or returns are lists, provide each arg in a table format and reference ranges in the Excel formula examples.
  - Ensure examples are clear and demonstrate practical use cases.
  - Headings of examples should not include `Example 1`, `Example 2`, etc., but should be descriptive of the example content, such as `### Calculating Option Price` or `### Using with Different Volatilities`.

- Include a `## References` section which repeats the references in the documentation and adds a link to the documentation for the module, e.g. https://fluids.readthedocs.io/fluids.atmosphere.html

- Use 2D list syntax `[[1, 2, 3], [4, 5, 6]]` for examples in arg and returns tables, not Excel array constants.
- Ensure JSX or HTML characters outside code blocks are wrapped in backticks. E.g. `{2,3}` or `<=`

### Function Implementation (Python Cell)
- The function name must be a lowercase of the Excel function name used in the documentation.
- Include a Google-style docstring with no examples.
- Do not put imports in try except blocks or use an import alias. Always import classes directly, e.g. `from fluids.atmosphere import ATMOSPHERE_1976` (not `as` anything).
- Do not add unused helper functions to any cell, including Gradio demo cells. Only include code that is required for the function, tests, or demo to work as specified.
- For HTTP requests, use the `requests` library.
- For API calls, use api_key as arguments, not environment variables.
- Args may only be list[list[]] or scalars, with types of float, bool, str, None.
- Returns may be list[] or list[list[]] or scalars, with types of float, bool, str, None.
- Where a function returns a series of attributes, return a list[].
- Variable arguments (`*args`, `**kwargs`) are not allowed.
- Function parameter names cannot contain numbers, use x_zero instead of x0, for example.
- Do not add comments before the function definition.
- Return error messages as str or list[list[str]] depending on output type instead of raising exceptions.
- Do not add any code for example usage.
- Import the package using the following syntax at the top of the cell:
   ```python
   import micropip
   await micropip.install('fluids')
   ```

### Unit Tests (Python Cell)
- Use `ipytest` for in-notebook testing as follows:
   ```python
   %pip install -q ipytest
   import ipytest
   ipytest.autoconfig()
   ..test functions here..
   ipytest.run()
   ```
- Write separate test functions for each test case.
- If the attached documentation includes example inputs and outputs, use those as test cases.
- Cover both success and failure paths.
- Use only generic assertions (type checks, non-emptiness, structure, approximate value checks).
- Avoid content-specific assertions, especially with stochastic outputs (e.g. LLM, optimization).
- Do not mock external APIs. 
- Demo test cases must be realistic and business-focused.

### Gradio Demo (Python Cell)
- Use `gr.Interface()` for the demo.
- Examples shoud be the same as those in the documentation.
- Set `flagging_mode='never'` to disable flagging.
- Use a separate output for each of the attributes returned by the function.
- For 2D list inputs or outputs, use `gr.DataFrame()` with `type="array"`.
- Set default values for all inputs to match the first example in the documentation.
- Add a description to the Gradio interface that matches the documentation.
- Do not add a title to the Gradio interface.
- Call `demo.launch()` at the end of the cell.

## Gradio Input Conversion
- Use `gr.Textbox(placeholder='Optional')` for optional numeric inputs in the Gradio interface. This allows users to leave the field blank, which will be passed as None.  For required numeric inputs, use `gr.Number()`.
- In the converter function, check for None or blank values and only pass non-empty values to the main function, casting to float if provided.  2D list inputs should also be checked for empty lists and not passed to the main function.
- This approach ensures that only explicitly provided values are passed, and the main function's default values are used for any omitted arguments.

## Step 3: Run and Validate

After creating the notebook, use the run notebook cell tools to run all cells, validate unit tests, and review the documentation. If you make changes to the function implementation cell during debugging, ensure you update the documentation and gradio demo cells if needed.

When done, stop here and do not proceed to the next notebook until you have received confirmation from the user to proceed.
