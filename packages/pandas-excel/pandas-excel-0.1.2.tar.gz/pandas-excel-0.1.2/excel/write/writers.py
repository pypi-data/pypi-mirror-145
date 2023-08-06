"""excel writing functions"""

import itertools
import pandas as pd
from excel.common import util, exceptions
from excel.format import type_checkers, get_column_formatter
from excel.format.formats import COLUMN_FORMAT


def write_dataframe_to_sheet(
    df,
    writer,
    sheet_name="Sheet1",
    custom_formats=None,
    **kwargs,
):
    """
    write a dataframe to an excel sheet, auto-fitting columns and optionally
    implementing custom number formats

    Args:
        df (pandas.DataFrame): dataframe to save to Excel
        writer (pandas.ExcelWriter): writer to write to
        sheet_name (str, optional): name of sheet to write. Defaults to 'Sheet1'
        custom_formats (dict, optional): dictionary of custom formats for each column.
            Defaults to None.
        **sort (bool): whether to apply an auto-filter to the data, enabling
            sort and filter in Excel. Defaults to True.
        **merge_index (bool): whether to merge multiindex cells for dataframes that have
            more than one index level. Defaults to False. NOTE: This will disable sorting
            as enabling sort requires all cells to be unmerged.
    """
    util.validate_sheet_name(sheet_name)

    if custom_formats is None:
        custom_formats = {}

    merge_index = kwargs.get("merge_index", False)
    if merge_index is True:
        sort = False
    else:
        sort = kwargs.get("sort", True)

    # create worksheet
    workbook = writer.book
    worksheet = workbook.add_worksheet(sheet_name)

    # write merged multiindex cells before writing
    if isinstance(df.columns, pd.MultiIndex):
        _write_multiindex_columns(df, worksheet, workbook)

    # do autofilter before potentially resetting index
    if sort is True:
        _set_autofilter(worksheet, df)

    # reset index if not default so you can write it as a column
    # only do this if merge_index is False, otherwise use _write_multiindex_columns
    # and set offset in _write_column_to_sheet
    if merge_index is True and isinstance(df.index, pd.MultiIndex):
        _write_merged_multiindex(df, worksheet, workbook)
        col_offset = df.index.nlevels
    else:
        col_offset = 0
        if not util.has_default_index(df):
            df = df.reset_index(drop=False)
        else:
            df = df.reset_index(drop=True)

    for col_index in range(len(df.columns)):
        _write_column_to_sheet(
            df,
            col_index,
            worksheet,
            workbook,
            custom_formats=custom_formats,
            sort=sort,
            col_offset=col_offset,
        )


def _set_autofilter(worksheet, df):
    """apply an autofilter to a worksheet

    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): worksheet to set autofilter in
        df (pandas.DataFrame): dataframe to obtain autofilter range from
    """
    columns = df.columns.nlevels - 1
    indices = df.index.nlevels - 1
    autofilter_args = {
        "first_row": columns,
        "first_col": 0,
        "last_row": df.shape[0] + columns,
        "last_col": df.shape[1] + indices,
    }

    if util.has_default_index(df):
        autofilter_args["last_col"] = autofilter_args["last_col"] - 1

    worksheet.autofilter(**autofilter_args)


def _write_merged_multiindex(df, worksheet, workbook):
    """write and merge the cells of multiindex

    Args:
        df (pandas.DataFrame): dataframe containing multiindex
        worksheet (xlsxwriter.worksheet.Worksheet): worksheet to write to
        workbook (xlsxwriter.Workbook): workbook to create column format in
    """
    start_row = df.columns.nlevels
    first_col = 0
    first_row = start_row
    column_format = workbook.add_format(COLUMN_FORMAT)
    for level in range(df.index.nlevels):
        level_values = df.index.get_level_values(level)

        _xlsxwriter_write(
            worksheet,
            "write_string",
            row=df.columns.nlevels - 1,
            col=level,
            string=str(level_values.name),
            cell_format=column_format,
        )

        for value, group in itertools.groupby(level_values):
            n_cells = sum(1 for _ in group)
            last_row = n_cells + first_row - 1
            if first_row == last_row:
                _xlsxwriter_write(
                    worksheet,
                    "write_string",
                    row=first_row,
                    col=first_col,
                    string=str(value),
                    cell_format=column_format,
                )
            else:
                _xlsxwriter_write(
                    worksheet,
                    "merge_range",
                    first_row=first_row,
                    first_col=first_col,
                    last_row=last_row,
                    last_col=first_col,
                    data=value,
                    cell_format=column_format,
                )
            first_row = n_cells + first_row

        first_row = start_row
        first_col = level + 1

        _xlsxwriter_write(
            worksheet,
            "set_column",
            level,
            level,
            _get_column_width(
                values=level_values,
                names=level_values.name,
                sort_padding=False,
            ),
        )
        if df.columns.nlevels > 2:
            _merge_empty_header_cells(df, worksheet, level, column_format)


def _write_multiindex_columns(df, worksheet, workbook):
    """write and merge the cells of multiindex columns

    Args:
        df (pandas.DataFrame): dataframe contain multiindex columns
        worksheet (xlsxwriter.worksheet.Worksheet): worksheet to write to
        workbook (xlsxwriter.Workbook): workbook to create column format in
    """
    start_col = df.index.nlevels
    first_row = 0
    first_col = start_col
    column_format = workbook.add_format(COLUMN_FORMAT)
    # -1 because lowest level of columns is written in _write_column_to_sheet
    for level in range(df.columns.nlevels - 1):
        level_values = df.columns.get_level_values(level)

        for value, group in itertools.groupby(level_values):
            n_cells = sum(1 for _ in group)
            last_col = n_cells + first_col - 1
            if first_col == last_col:
                _xlsxwriter_write(
                    worksheet,
                    "write_string",
                    row=first_row,
                    col=first_col,
                    string=str(value),
                    cell_format=column_format,
                )
            else:
                _xlsxwriter_write(
                    worksheet,
                    "merge_range",
                    first_row=first_row,
                    first_col=first_col,
                    last_row=first_row,
                    last_col=last_col,
                    data=value,
                    cell_format=column_format,
                )

            first_col = n_cells + first_col
        first_col = start_col
        first_row = level + 1


def _write_column_to_sheet(df, column_index, worksheet, workbook, **kwargs):
    """write a column to worksheet by index

    Args:
        df (pandas.DataFrame): dataframe containing column to write
        column_index (int): index of column to write
        worksheet (xlsxwriter.worksheet.Worksheet): worksheet to write to
        workbook (xlsxwriter.Workbook): workbook passed to
            formatter.get_xlsxwriter_format
        **custom_formats (dict): dictionary of custom formats
        **sort (bool): whether the column will be sorted, to adjust padding
            to accomodate sort button
        **column_format (xlsxwriter.workbook.Format, optional): format object
            for column headers. One is created if not provided.
        **col_offset (int): number of columns to offset, if merging index
    """

    column_format = workbook.add_format(COLUMN_FORMAT)
    # use iloc rather than column name to prevent breaking
    # on multiindex with duplicate names
    column_values = df.iloc[:, column_index]
    # get formatter for column data type
    formatter = get_column_formatter(column_values, kwargs.get("custom_formats", {}))
    # store name for later use before losing it when converting to list
    column_names = column_values.name
    # convert to list, from which we'll write values
    column_values = column_values.tolist()

    # convert column names to list so they can be reversed
    if isinstance(column_names, tuple):
        column_names = list(column_names)
    elif isinstance(column_names, str):
        column_names = [column_names]

    column_index += kwargs.get("col_offset", 0)

    # if all but one column name is an empty string, reverse the list of column names
    # so the non-empty string is selected
    if util.only_one_non_empty_column_level(column_names):
        # reverse the list so the value written is at the bottom
        column_names.reverse()
        # merge the cells above this column with an empty value if more than 2 levels
        if df.columns.nlevels > 2:
            _merge_empty_header_cells(df, worksheet, column_index, column_format)

    # write only the last column name. any additional levels of columns are
    # written in _merge_multiindex_columns
    _xlsxwriter_write(
        worksheet,
        "write_string",
        row=df.columns.nlevels - 1,
        col=column_index,
        string=str(column_names[-1]),
        cell_format=column_format,
    )

    # store number of column levels before writing
    row_offset = len(column_names)

    # write values
    for row_index, val in enumerate(column_values):
        row_index = row_index + row_offset
        # setup formatter for value if formatter takes modifications
        if hasattr(formatter, "for_value"):
            formatter.for_value(val)
        # write cell data to worksheet
        _xlsxwriter_write(
            worksheet,
            formatter.xlsx_writer_write_method_name,
            row_index,
            column_index,
            _pre_write(val),
            formatter.get_xlsxwriter_format(workbook),
        )

    _xlsxwriter_write(
        worksheet,
        "set_column",
        first_col=column_index,
        last_col=column_index,
        width=_get_column_width(
            value_formatter=formatter,
            values=column_values,
            names=column_names,
            sort_padding=kwargs.get("sort", True),
        ),
    )


def _merge_empty_header_cells(df, worksheet, column_index, column_format):
    """merge the cells above the lowest level of multiindex columns

    Args:
        df (pandas.DataFrame): dataframe containing multiindex columns
        worksheet (xlsxwriter.worksheet.Worksheet): worksheet to write to
        column_format (xlsxwriter.workbook.Format): format object to apply to cells
    """
    _xlsxwriter_write(
        worksheet,
        "merge_range",
        first_row=0,
        first_col=column_index,
        last_row=df.columns.nlevels - 2,
        last_col=column_index,
        data="",
        cell_format=column_format,
    )


def _get_column_width(values, names, sort_padding, value_formatter=None):
    """get the column width, in characters, of the values and names of a column

    Args:
        values (list | pandas.Index): a list or pandas index containing values
        names (str | pandas.Index): a single column name or index of column names
        sort_padding (bool): whether to use padding to accomodate a sort button
        value_formatter (excel.format.DtypeFormatter, optional): formatter to
            apply to value before measuring. Defaults to None.

    Returns:
        int: longest value, in characters
    """
    assert isinstance(
        values, (list, pd.Index)
    ), f"values expects a list or a pandas.Index, not {type(values)}"

    if not isinstance(names, (list, pd.Index)):
        names = [names]
    else:
        # only measure based on last name so merged levels don't interfere
        names = [list(names)[-1]]

    if value_formatter is not None:
        values = [value_formatter.convert_value(val) for val in values]

    max_len = lambda iterable: max(map(lambda val: len(str(val)), iterable))
    # +5 if sort to accommodate the sort button, +1 if not to prevent cutoff
    if sort_padding is True:
        padding = 5
    else:
        padding = 1
    column_width = max([max_len(values), max_len(names)]) + padding

    return column_width


def _xlsxwriter_write(worksheet, method_name, *args, **kwargs):
    """
    write a value or range in a worksheet by method. allows for better error
    handling for xlsxwriter's exit codes

    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): worksheet to write to
        method_name (str): name of xlsxwriter.worksheet.Worksheet method

    Raises:
        TypeError: if anything other than Worksheet is passed as worksheet
        ValueError: if both args and kwargs were passed
        ValueError: if the method name doesn't exist
        exceptions.WorksheetWriteException: if write method failed
    """
    if len(args) > 0 and len(kwargs) > 0:
        raise ValueError(
            "attempted to write with both positional and keyword arguments. "
            "this can cause unexpected results"
        )

    try:
        xlsxwriter_method = getattr(worksheet, method_name)
    except AttributeError as exc:
        raise ValueError(
            f"invalid method name '{method_name}' for xlsxwriter.worksheet.Worksheet"
        ) from exc

    out = xlsxwriter_method(*args, **kwargs)
    if out is not None and out < 0:
        raise exceptions.WorksheetWriteException(method_name, out, args, kwargs)

    if len(args) > 0:
        return {
            "start_row": args[0],
            "start_col": args[1],
            "end_row": args[0],
            "end_col": args[1],
        }
    return kwargs


def _pre_write(val):
    """final transformations that need to take place before writing"""
    if type_checkers.pandas_timestamp(val):
        val = val.to_pydatetime()
    return val
