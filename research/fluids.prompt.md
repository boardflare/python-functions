# Building Excel Functions Using the `fluids` Python Package

## Overview
You are creating a series of custom Excel functions that interface with the `fluids` Python package in the github repo `CalebBell/fluids`. You can use your github search tool to learn more about it.  The goal is to provide a user-friendly way for engineers and scientists to perform fluid dynamics calculations directly in Excel, while minimizing the number of functions needed by grouping related calculations together.

## Step 1: Enumerate the modules in the `fluids` package
Read the documentation for the `fluids` package at [fluids.readthedocs.io](https://fluids.readthedocs.io/modules.html) and enumerate the all the modules and the links to their documentation.

Write this list into #file`research/fluids.md` file.  Write the list as a checklist so you can check off each module as you implement it in Step 2.

## Step 2: Write documentation for each Excel function that implements a module in the `fluids` package
Read the documentation for each module in the `fluids` package, e.g. https://fluids.readthedocs.io/fluids.atmosphere.html using the list of links from step 1, starting with the first one that has not been completed yet. Write a brief description of what the Excel function would do that implements that module, including its parameters and return values. This documentation should be concise and user-friendly, suitable for inclusion in an Excel help sheet.  Ideally we'd like to implement all of the features of the module in a single Excel function, but we cannot use variable args so we may need to create multiple functions for a single module if there are too many parameters or if the parameters are not related.
- **Function Name:** `FLUIDS_ATMOSPHERE`
  - **Description:** Computes atmospheric properties based on the selected method.
  - **Parameters:**
    - `method`: The calculation type (e.g., `"ATMOSPHERE_1976"`, `"solar_position"`).
    - Additional parameters as required by the selected method.
  - **Returns:** Atmospheric properties such as pressure, temperature, and density.

Write the documentation into #file`research/fluids.md` file in a separeate section for each function, then check off the module in the checklist.  Stop when you have completed 3 modules so I may review your work.

