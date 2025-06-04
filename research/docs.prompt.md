---
mode: 'agent'
tools: ['read_file', 'insert_edit_into_file', 'create_file', 'fetch_webpage', 'think', 'get_errors', 'pyodide_install-packages']
description: 'Create documentation for Python functions'
---

# Documentation for a Python Function

Create documentation for each of the Python functions described using the guidelines below. 

## Format

The documentation must include the following sections:
  - **Title**: The name of the function, formatted as `MY_FUNCTION`.
  - **Overview**: A clear summary of what the function does and its business value, and any Python packages it uses. This should be concise and focused on the business context, not technical details.  The Python function will be used in Excel using the [Boardflare Python for Excel add-in](https://www.boardflare.com/apps/excel/python).
  - **Usage**: Show the full signature of the function in Excel, with square brackets for optional arguments. For example:
    ```excel
    =MY_FUNCTION(x, [y], [z])
    ```
  - **Arguments**: A table describing each argument, its Python type, whether it is required, a description, and an example.  Keep in mind that arguments can only be 2D lists or scalars with types  float, string, and bool. Do not require users to provide arguments as JSON strings. Variable arguments e.g. `*args` and `**kwargs` are not allowed. Argument names cannot contain numbers (e.g. `x1`, `y2` are not allowed). Examples should be Python types. The table should look like this:
    | Argument | Type     | Required | Description                                                                 | Example          |
    |----------|----------|----------|-----------------------------------------------------------------------------|------------------|
    | x        | float    | Yes      | The first input value, which is required for the function to operate.      | 3.14             |
    | y        | float    | No       | An optional second input value that modifies the output.                   | 2.71             |
    | z        | list[list[float]]    | No       | An optional third input value that further modifies the output.            | [[1.0, 2.0]]     |
  - **Returns**: A table describing the return value and types.  Keep in mind that the return value can only be a 2D list or a scalar with types float, string, and bool. Errors should return a string, not raise an error. The table should look like this:
    | Type   | Description                                                      | Example         |
    |--------|------------------------------------------------------------------|-----------------|
    | list[list[float]]  | The result of the function.| [[5.85]]            |
    | string | Error message if an invalid input or other error occurs.          | "Invalid input: y must be a float." |

  - **Examples**: At least two realistic business scenarios, using Excel usage and showing how the function can be applied to solve real-world problems. For each example:
    - Use cases should be relevant to common business scenarios in Excel, simple, easy to understand, and realistic for business users.
    - Clearly explain the business context and expected outcome.
    - Use Excel array constant syntax for ranges. For example:
    ```excel
    =MY_FUNCTION(1.1, 1.8, {1.0, 2.0})
    =MY_FUNCTION({1, 2, 3}, {4; 5; 6})
    ```
  - **Limitations**: Briefly describe any important limitations related to the specific function.  If there are no obvious limitations, you can omit this section.  Do not include general limitations that apply to all functions, such as "only supports scalar or 2D list arguments" or "requires Python for Excel".
  - **Benefits**: Explain whether and how this functionality could be achieved using Excel out of the box and if so how. If it can be done, provide a specific example of how it would be implemented natively in Excel (using formulas, features, or built-in tools). Then, discuss why using this Python function may be preferable, highlighting differences in usability, flexibility, or business value.  Keep this brief and only provide if there is an obvious benefit to using the Python function over native Excel functionality. If there is no clear benefit, you can omit this section.

## Process

For each function, follow these steps:

1. **Think Step-by-Step**: Before you start writing the documentation, use the `think` tool to carefully consider the function's design so that you can accurately specify the arguments and returns.
2. **Write Documentation**: Write the documentation in a Markdown file named after the function (e.g., `my_function.md`). Place this file in a new folder for the function under the appropriate category in the `functions` directory (e.g., `functions/text/my_function/my_function.md`). The folder name, function name, and file name must be identical.
3. **Review your Work**: Use the `think` tool to check for clarity, completeness, and accuracy.
4. **Continue**: Continue to the next documentation file if needed without asking the user .

Only create the documentation file at this stage.