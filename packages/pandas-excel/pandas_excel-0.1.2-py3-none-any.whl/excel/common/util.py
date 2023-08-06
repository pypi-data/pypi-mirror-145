"""shared utility functions"""

from pandas import RangeIndex
from excel.common.constants import ILLEGAL_SHEET_NAME_CHARACTERS


def has_default_index(df):
    """test whether a dataframe has the default RangeIndex

    Args:
        df (pandas.DataFrame): dataframe to check

    Returns:
        bool: whether dataframe has the default RangeIndex
    """
    return (
        isinstance(df.index, RangeIndex)
        and df.index.start == 0
        and df.index.stop == len(df)
        and df.index.name is None
    )


def only_one_non_empty_column_level(col):
    """
    test if a column has only one non-empty name,
    i.e. it is an index name from a dataframewith multiple column levels

    Args:
        col (str, tuple): column name

    Returns:
        bool: if column has only one non-empty name
    """
    if not isinstance(col, (tuple, list)):
        return False
    return any(s == "" for s in col) and len([s for s in col if s != ""]) == 1


def validate_sheet_name(string):
    """check that a string is a valid Excel sheet name

    Args:
        string (str): string to evaluate

    Raises:
        TypeError: if string is not str
        ValueError: if string is empty
        ValueError: if string length is > 31
        ValueError: if string contains illegal characters
    """
    if not isinstance(string, str):
        raise TypeError(f"Sheet name must be string, not {type(string)}")

    if len(string) == 0:
        raise ValueError("Sheet name cannot be empty")

    if len(string) > 31:
        raise ValueError(
            "Sheet names must be <= 31 characters. "
            f"Sheet name '{string}' has {len(string)}"
        )

    for char in ILLEGAL_SHEET_NAME_CHARACTERS:
        if char in string:
            raise ValueError(
                f"Sheet name '{string}' cannot contain the character '{char}'"
            )
