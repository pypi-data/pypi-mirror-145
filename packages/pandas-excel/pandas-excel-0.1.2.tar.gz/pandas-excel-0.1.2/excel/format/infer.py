"""column format interence"""

from excel.format import type_checkers
from excel.format import formats, formatters


def get_column_formatter(series, custom_formats):
    """get the appropriate formatter for a given column

    Args:
        df (pandas.DataFrame): dataframe to find column in
        custom_formats (dict): custom formats

    Raises:
        TypeError, ValueError: if an invalid custom value was provided

    Returns:
        DtypeFormatter, str: formatter if one was found, else "General"
    """

    if not isinstance(custom_formats, dict):
        raise TypeError(
            "each custom format must be either a DtypeFormatter or a dict "
            "containing a DtypeFormatter and options. "
            f"{type(custom_formats)} was passed"
        )

    if series.name in custom_formats:

        custom_format = custom_formats[series.name]

        if isinstance(custom_format, formatters.DtypeFormatter):
            formatter = custom_format

        elif isinstance(custom_format, str):
            formatter = get_formatter_by_string(custom_format)

        elif isinstance(custom_format, dict):
            try:
                formatter = custom_format["formatter"]
            except KeyError as exc:
                raise ValueError(
                    "dictionary formatter must have a key named 'formatter'"
                ) from exc

            if isinstance(formatter, str):
                formatter = get_formatter_by_string(formatter)

            if not isinstance(formatter, formatters.DtypeFormatter):
                raise TypeError(
                    "formatter must be an instance of DtypeFormatter, "
                    f"not {type(formatter)}"
                )

    else:
        # defaults, must set manually to use others
        if type_checkers.number(series) is True:
            formatter = formats.NUMBER
        elif type_checkers.datetime(series):
            formatter = formats.SHORT_DATE
        else:
            formatter = formats.GENERAL

    return formatter


def get_formatter_by_string(string):
    """get a formatter object by its name as a string

    Args:
        string (str): name of formatter

    Raises:
        ValueError: if string is not the name of an existing formatter

    Returns:
        excel.format.formatters.DtypeFormatter: format with string as name
    """
    # convert string to constant format before searching
    string = string.upper().replace(" ", "_")
    try:
        formatter = getattr(formats, string)
    except AttributeError as exc:
        raise ValueError(
            f"'{string}' is not a valid format. See "
            "https://christopher-hacker.github.io/pandas-excel/excel/format/formats.html"
            "for a list of available formats. "
        ) from exc
    return formatter
