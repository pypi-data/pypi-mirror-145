"""exceptions"""


class WorksheetWriteException(Exception):
    """if any xlsxwriter.worksheet.Worksheet write method failed"""

    def __init__(self, method_name, exit_code, *args, **kwargs):
        assert isinstance(method_name, str)
        assert isinstance(exit_code, int)

        msg = (
            f"Worksheet.{method_name} failed with code {exit_code}. "
            "This likely means that the column you tried to write to is "
            "out of the worksheet bounds, but can have other meanings "
            "depending on the method used. "
            "See https://xlsxwriter.readthedocs.io/worksheet.html for details."
        )

        if any(len(i) > 0 for i in [args, kwargs]):
            msg += "\n\nParams were:\n" + str(args) + str(kwargs)

        super().__init__(msg)
