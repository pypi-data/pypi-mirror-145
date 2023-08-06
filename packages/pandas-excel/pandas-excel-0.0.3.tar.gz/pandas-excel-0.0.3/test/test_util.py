"""utility function tests"""

import pytest
from excel.common import util


@pytest.mark.parametrize(
    ("fixture_name", "expected"),
    [
        ("test_range_index_single_column", True),
        ("test_rangeindex_string_columns", True),
        ("test_datetime_index_single_column", False),
        ("test_categorical_index_single_column", False),
        ("test_non_default_rangeindex", False),
    ],
)
def test_has_default_index(fixture_name, expected, request):
    """test has_default_index method"""
    assert util.has_default_index(request.getfixturevalue(fixture_name)) == expected


@pytest.mark.parametrize(
    ("col_name", "expected"),
    [
        ("foo", False),
        (("foo", "bar"), False),
        (("", "foo", "bar"), False),
        (("", "", "foo"), True),
    ],
)
def test_only_one_non_empty_column_level(col_name, expected):
    """test only_one_non_empty_column_level"""
    assert util.only_one_non_empty_column_level(col_name) == expected


@pytest.mark.parametrize(
    ("string", "exception"),
    [
        ("Sheet1", None),
        ("Sheet_1", None),
        ("".join("x" for _ in range(31)), None),
        (0, TypeError),
        ("", ValueError),
        ("".join("x" for _ in range(32)), ValueError),
        ("Sheet1*", ValueError),
    ],
)
def test_validate_sheet_name(string, exception):
    """test validate_sheet_name method"""
    if exception is not None:
        with pytest.raises(exception):
            util.validate_sheet_name(string)
    else:
        util.validate_sheet_name(string)
