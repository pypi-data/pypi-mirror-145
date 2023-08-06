"""type checking functions for format inference"""

from pandas.api.types import is_number, is_numeric_dtype


def number(obj):
    """is number or pandas numeric dtype"""
    return any(
        check(obj) is True
        for check in [
            is_number,
            is_numeric_dtype,
            lambda obj: str(obj).isnumeric(),
        ]
    )


def datetime(obj):
    """is any object with a strftime method"""
    return hasattr(obj, "strftime") or hasattr(obj, "dt")


def date_no_time(obj):
    """if a date object has no time objue"""

    if not datetime(obj):
        return False
    if hasattr(obj, "time"):
        # if all time objues are null, return True
        return all(
            getattr(obj.time(), attr) == 0 for attr in ["hour", "minute", "second"]
        )
    return True


def pandas_timestamp(obj):
    """test if is pandas Timestamp

    Args:
        obj (any): objue to test

    Returns:
        bool: if obj is pandas Timestamp
    """
    return hasattr(obj, "to_pydatetime")
