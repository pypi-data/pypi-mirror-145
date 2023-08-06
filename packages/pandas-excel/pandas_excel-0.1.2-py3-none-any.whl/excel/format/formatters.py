"""excel number format classes"""

import re
from excel.format import type_checkers


class DtypeFormatter:
    """
    converts a value of provided type to python format using a provided conversion
    function in order to predict how much space will be needed to auto-fit column

    Args:
        excel_format (str): string provided to Excel formatter
        python_format (str): python format to be passed to convert_function
        convert_function (function): a function that accepts one argument and returns a
            formatted string.
        type_checker (function): a function that accepts a value and returns a boolean
            to evaluate whether a value is of the desired type to format
        **modifier_function: a function that accepts and returns one value,
            called before self.convert_value
    """

    def __init__(
        self,
        excel_format,
        python_format,
        convert_function,
        type_checker,
        **kwargs,
    ):
        self.excel_format = excel_format
        self.python_format = python_format
        self.convert_function = convert_function
        self.type_checker = type_checker
        self.xlsx_writer_write_method_name = kwargs.pop(
            "xlsx_writer_write_method_name", "write_string"
        )
        self.modifier_function = kwargs.pop("modifier_function", lambda val: val)
        self._defaults = {
            "excel_format": self.excel_format,
            "python_format": self.python_format,
        }

    def _reset(self):
        for attr_name, default_value in self._defaults.items():
            self.__setattr__(attr_name, default_value)

    def convert_value(self, value, **kwargs):
        """
        convert a python value into its corresponding string format as it
        would appear in Excel

        Args:
            value (any): value to convert
            **kwargs (any): values passed to self.for_value, if it exists

        Returns:
            str: string-formatted value
        """
        # if any subclass has a "for_value" method, run that first to update
        # format strings for the value
        if hasattr(self, "for_value"):
            self.for_value(value, **kwargs)
        if self.type_checker(value) is True:
            return self.convert_function(self.modifier_function(value))
        return str(value)

    def get_xlsxwriter_format(self, workbook):
        """get an xlsxwriter Format object for self.excel_format

        Args:
            workbook (xlsxwriter.Workbook): workbook to create format in

        Returns:
            xlsxwriter.workbook.Format: Format object for given excel format
        """
        fmt = workbook.add_format({"num_format": self.excel_format})
        return fmt


class NumberFormatter(DtypeFormatter):
    """base class for number format conversion

    Args:
        excel_format (str): string provided to Excel formatter
        python_format (str): python format to be passed to convert_function
        **decimals (int): number of decimals to display
    """

    def __init__(self, excel_format, python_format, **kwargs):
        # if "decimals" in kwargs, always use that value
        self.default_decimals = kwargs.pop("decimals", None)
        super().__init__(
            excel_format=excel_format,
            python_format=python_format,
            convert_function=python_format.format,
            type_checker=type_checkers.number,
            xlsx_writer_write_method_name="write_number",
            **kwargs,
        )
        # regex for parsing decimal numbers
        self.excel_format_pat = r"((?<=\.)(?:0+)|^0$)"
        self.python_format_pat = r"(?<={:\.)(\d)(?=[fe]})"
        # run this on init so it fails on invalid patterns
        try:
            self.format_string_decimals
        except ValueError as exc:
            raise ValueError(
                "One or more format strings is invalid. For more info see "
                "https://support.microsoft.com/en-us/office/number-format-codes-"
                "5026bbd6-04bc-48cd-bf33-80f18b4eae68"
            ) from exc

    @staticmethod
    def _get_n_decimal_points(value):
        if type_checkers.number(value):
            match = re.match(r"^[0-9]*\.([1-9]([0-9]*[1-9])?)0*$", str(value))
            n_decimals = len(match.group(1)) if match is not None else 0
        else:
            n_decimals = 0
        return n_decimals

    @property
    def format_string_decimals(self):
        """get number of decimals in format strings"""

        def extract_or_fail(pat, val):
            match = re.search(pat, val)
            if match is None:
                raise ValueError(f"invalid format: '{val}'. Unable to locate decimals.")
            return match.group(1)

        python_decimals = int(
            extract_or_fail(self.python_format_pat, self.python_format)
        )
        excel_decimals = (
            len(extract_or_fail(self.excel_format_pat, self.excel_format))
            # explicitly allow "0" format for no decimals
            if self.excel_format != "0"
            else 0
        )
        assert (
            python_decimals == excel_decimals
        ), "python and excel formats must have the same number of decimals"
        return python_decimals

    def _set_decimals(self, decimals=None):
        """set the number of decimals in format strings"""

        assert isinstance(decimals, int)
        self.excel_format = re.sub(
            r"(?<=\.)(0+)",
            "".join(["0" for _ in range(decimals)]),
            self.excel_format,
        )
        # drop trailing point
        self.excel_format = re.sub(r"(?<=\d)(\.)(?=%?$|E+)", "", self.excel_format)
        self.python_format = re.sub(
            r"(?<={:\.)(\d)(?=[fe]})", str(decimals), self.python_format
        )
        self.convert_function = self.python_format.format

    def for_value(self, value, decimals=None):
        """make adjustments for value

        Args:
            value (any): value to convert
            decimals (int, optional): if provided, use this number of decimals
                for all values.

        Returns:
            str: string-formatted value
        """
        self._reset()
        if self.type_checker(value) is True:
            value = self.modifier_function(value)
        if decimals is not None:
            self._set_decimals(decimals)
        else:
            if self.default_decimals is not None:
                self._set_decimals(self.default_decimals)
            else:
                # otherwise only use default decimal value if there are actual decimals
                # in the value
                try:
                    if float(value).is_integer():
                        # if it's an integer, no decimals
                        self._set_decimals(0)
                    else:
                        # if not, use the initial number of decimals
                        self._set_decimals(self._get_n_decimal_points(value))
                except ValueError as exc:
                    if "could not convert string to float" not in str(exc):
                        # catch and ignore string to float, raise any other exception
                        raise exc  # pragma: nocover
        return self


class DateTimeFormatter(DtypeFormatter):
    """base class for number format conversion

    Args:
        excel_format (str): string provided to Excel formatter
        python_format (str): python format to be passed to convert_function
        **auto_times (int): drop time formatting when time values are zero
            or datetime.date object is provided, and add time values to formats
            that have none. Defaults to True.
    """

    def __init__(self, excel_format, python_format, **kwargs):
        self.excel_format = excel_format
        self.python_format = python_format
        self.type_checker = type_checkers.datetime
        self.auto_times = kwargs.pop("auto_times", True)
        super().__init__(
            excel_format=excel_format,
            python_format=python_format,
            convert_function=self._convert_function,
            type_checker=self.type_checker,
            xlsx_writer_write_method_name="write_datetime",
            **kwargs,
        )
        self._initial_python_format = python_format
        self._initial_excel_format = excel_format
        self._time_regex = {
            "python": r"%(H|-H|I|-I|p|M|-M|S|-S|f|z|Z)",
            "excel": r"h+:mm(?::ss)?(?:\.0)?(?:\sAM\/PM)?",
        }
        # enforce matching formats in __init__. this will fail on mismatch
        self._has_time()

    def _has_time(self):
        tests = [
            re.search(self._time_regex["python"], self.python_format) is not None,
            re.search(self._time_regex["excel"], self.excel_format) is not None,
        ]
        if all(tests):
            return True
        if any(tests):
            raise ValueError("format mismatch. must have consistent times.")
        return False

    def _convert_function(self, value):
        return value.strftime(self.python_format)

    def _strip_time(self):
        # strip all time values from python format
        self.python_format = re.sub(
            r"\:{2,}|\:$",
            "",
            re.sub(self._time_regex["python"], "", self.python_format),
        ).strip()
        # strip all time values from excel format
        self.excel_format = re.sub(
            self._time_regex["excel"], "", self.excel_format
        ).strip()

    def _add_time(self, seconds=False):
        # if there are already times, don't change them
        if self._has_time():
            return
        self.python_format += " %H:%M"
        self.excel_format += " h:mm"
        if seconds is True:
            self.python_format += ":%S"
            self.excel_format += ":ss"

    def for_value(self, value):
        """configure attributes to value

        Args:
            value (any): value to adjust attributes to
        """
        self._reset()
        # always use default formats if auto_times is disabled
        if self.auto_times is True:
            if type_checkers.date_no_time(value):
                # if no time, make sure there are no time in format
                self._strip_time()
            else:
                # if there are time, add them to the pattern
                self._add_time(hasattr(value, "second"))
