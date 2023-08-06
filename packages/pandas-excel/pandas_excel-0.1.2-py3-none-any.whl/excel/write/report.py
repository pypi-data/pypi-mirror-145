"""
.. include:: ../../static/docs/excel/write/report.md
"""

import pandas as pd
from excel.write.writers import write_dataframe_to_sheet


class ExcelReport:
    """generates an excel file with a table of contents

    Args:
        filename (str): path to excel file
        **contents (bool): whether to write table of contents sheet with links
            to other sheets. Defaults to True, unless there is only one sheet, in which
            case it will always be False.
    """

    def __init__(self, filename, **kwargs):
        self.tables = {}
        self.default_figsize = (15, 10)
        self.filename = filename
        self.contents = kwargs.get("contents", True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.write()

    def _build_contents_df(self):
        """build the table containing table names and descriptions from self.tables"""
        data = {"Table Name": [], "Description": []}
        for sheet_name, table_info in self.tables.items():
            data["Table Name"].append(sheet_name)
            description = table_info["description"]
            data["Description"].append(description if description is not None else "")
        return pd.DataFrame(data, index=list(range(len(data["Table Name"]))))

    def _build_contents_sheet(self, writer):
        """create the table of contents sheet"""
        contents_df = self._build_contents_df()

        # setup word wrap
        word_wrap_format = writer.book.add_format()
        word_wrap_format.set_text_wrap()

        # write contents df to writer and get sheet object
        contents_sheet_name = "Contents"
        contents_df.to_excel(writer, sheet_name=contents_sheet_name, index=False)
        contents_sheet = writer.sheets[contents_sheet_name]
        contents_sheet.set_column("A:A", 30)

        # ensure second column wraps
        contents_sheet.set_column("B:B", 120, word_wrap_format)
        for sheet_index, sheet_name in enumerate(self.tables):
            contents_sheet.write_url(
                f"A{sheet_index + 2}",
                f"internal:'{sheet_name}'!A1",
                string=sheet_name,
                tip="jump to sheet",
            )

    def add_table(
        self,
        df,
        sheet_name,
        description=None,
        column_formats=None,
        **kwargs,
    ):
        """add a table to the report

        Args:
            df (pandas.DataFrame): table to add
            sheet_name (str): name of table for contents
            description (str, optional): description for table. Defaults to None.
            column_formats (str | dict, optional): a string containing an excel number format or
                a dictionary of column names and number formats. Defaults to None.
            **merge_index (bool): whether to merge multiindex cells for dataframes that have
                more than one index level. Defaults to False. NOTE: This will disable sorting
                as enabling sort requires all cells to be unmerged.
        """
        table_dict = {
            "df": df,
            "description": description,
            "column_formats": column_formats,
            "merge_index": kwargs.get("merge_index", False),
        }
        self.tables[sheet_name] = table_dict
        return df

    def write(self):
        """write the report to excel

        Args:
            output_excel_file (str): path to output file
        """
        with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            self.filename, engine="xlsxwriter"
        ) as writer:

            # table of contents must be written first
            if self.contents is True and len(self.tables) > 1:
                self._build_contents_sheet(writer)

            for sheet_name, df_info in self.tables.items():
                df = df_info["df"]
                write_dataframe_to_sheet(
                    df,
                    writer,
                    sheet_name,
                    df_info["column_formats"],
                    merge_index=df_info["merge_index"],
                )
