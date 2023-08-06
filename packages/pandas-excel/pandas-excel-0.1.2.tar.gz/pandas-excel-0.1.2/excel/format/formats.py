"""
Number and Date format options.
.. include:: ../../static/docs/excel/format/available-formats.md
---
"""

from excel.format.formatters import DtypeFormatter, NumberFormatter, DateTimeFormatter

GENERAL = DtypeFormatter(
    excel_format="General",
    python_format=None,
    convert_function=lambda val: val,
    type_checker=lambda _: True,
)
"""Default format for string values. Writes to Excel as the string version of a value"""

NUMBER = NumberFormatter(excel_format="0.00", python_format="{:.2f}")
"""
Default number format. Writes to Excel as a number with 0 decimals if an integer, or 2 if a float.
"""

CURRENCY = NumberFormatter(excel_format="$0.00", python_format="${:.2f}", decimals=2)
"""
Writes to Excel's Currency format: $0.00. Always prefixes with a '$' and has 2 decimal points
"""

PERCENTAGE = NumberFormatter(
    excel_format="0.00%",
    python_format="{:.2f}%",
    modifier_function=lambda val: val * 100,
)
"""
Similar to Excel's Percentage format, multiplies the value by 100 and appends a "%".
"""

SCIENTIFIC_NOTATION = NumberFormatter(excel_format="0.00E+0", python_format="{:.2e}")
"""Similar to Excel's Scientific Notation format."""

SHORT_DATE = DateTimeFormatter("yyyy-mm-dd", "%Y-%m-%d")
"""
Basic date format. Uses yyyy-mm-dd format rather than excel's default mm/dd/yyyy format
"""

COLUMN_FORMAT = {
    "bold": 1,
    "border": 1,
    "valign": "vcenter",
    "align": "center",
}
