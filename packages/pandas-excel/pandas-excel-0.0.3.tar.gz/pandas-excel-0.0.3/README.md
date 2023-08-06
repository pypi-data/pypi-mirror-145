# pandas-excel

[![Status](https://github.com/christopher-hacker/pandas-excel/actions/workflows/test-status.yml/badge.svg)](https://github.com/christopher-hacker/pandas-excel/actions/workflows/test-status.yml)[![codecov](https://codecov.io/gh/christopher-hacker/pandas-excel/branch/main/graph/badge.svg?token=N9RLXFHVFG)](https://codecov.io/gh/christopher-hacker/pandas-excel)[![PyPI version](https://badge.fury.io/py/pandas-excel.svg)](https://badge.fury.io/py/pandas-excel)


Quickly turn pandas dataframes into shareable Excel reports.

## Overview

`pandas-excel` writes easy-to-read, ready-to-share multi-sheet Excel workbooks from pandas dataframes. It fixes some of the problems with `DataFrame.to_excel`, including its annoying habit of [writing an empty line below multiindex columns](https://github.com/pandas-dev/pandas/issues/27772), and implements several features not currently present in any existing excel writing libraries, including:
- Creation of multi-sheet report workbooks with a table of contents
- Commonly-used Excel number formats (e.g. Percentage, Accounting, etc.)
- Auto-fitting columns

## Basic Usage

Instead of writing using `DataFrame.to_excel`, create an `ExcelReport` object, either by instantiating directly or using `with`:

```python
import excel
import pandas as pd

df = pd.read_csv("input_file.csv")

report = excel.ExcelReport("output/basic-example.xlsx")

# do some analysis here

report.add_table(df, sheet_name="my-sheet")

# more analysis

report.add_table(some_other_df, sheet_name="other sheet")

report.write()
```

Or use `with`:

```python
import excel
import pandas as pd

df = pd.read_csv("input_file.csv")

# do some analysis here

with excel.ExcelReport("output/basic-example.xlsx") as report:
    report.add_table(df, sheet_name="my-sheet")
```


There are several examples of `pandas-excel`'s capabilities in [here](https://github.com/christopher-hacker/pandas-excel/tree/main/examples).

## Installation

`pandas-excel` is available on PyPi here: [https://pypi.org/project/pandas-excel](https://pypi.org/project/pandas-excel)

Install the latest release using `pip`:

```
pip install pandas-excel
```