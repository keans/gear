import logging
from pathlib import Path
from typing import Union, Any

import xlrd
import openpyxl

from gear.filetypes.base.basereader import BaseReader
from gear.filetypes.xls.xlsschema import xls_schema
from gear.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class XlsReader(BaseReader):
    """
    XLS reader
    """
    def __init__(
        self,
        filename: Union[str, Path],
        **kwargs
    ):
        BaseReader.__init__(
            self,
            argconfig_schema=xls_schema,
            filename=filename,
            **kwargs
        )

    def __enter__(self):
        """
        enter context manager
        """
        # ensure that filename is set for loading and that it does exist
        self.ensure_filename_set(must_exist=True)

        if self.filename.suffix == ".xls":
            self._f = xlrd.open_workbook(self.filename, on_demand=True)

        elif self.filename.suffix == ".xlsx":
            self._f = openpyxl.load_workbook(self.filename, read_only=True)

        else:
            raise NotImplemented(
                f"Unknown file extention '{self.filename.suffix}' for "
                f"XlsReader!"
            )

        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        """
        exit context manager

        :param exc_type: executable type
        :type exc_type: Any
        :param exc_value: executable value
        :type exc_value: Any
        :param traceback: traceback
        :type traceback: Any
        """

        if self.filename.suffix == ".xls":
            self._f.release_resources()

        elif self.filename.suffix == ".xlsx":
            self._f.close()

    def __iter__(self):
        """
        iterate over row of pandas dataframe obtained from csv file

        :return: generator that iterates over rows
        :rtype: Generator
        """
        self.ensure_file_is_opened()

        if self.filename.suffix == ".xls":
            # select sheet
            sheet = self._f.sheet_by_index(self.argconfig["sheet_index"] or 0)

            # return generator of rows
            return (
                sheet.row_values(row, start_colx=0, end_colx=None)
                for row in range(sheet.nrows)
            )

        elif self.filename.suffix == ".xlsx":
            # select sheet
            sheet = self._f.worksheets[self.argconfig["sheet_index"] or 0]

            # return generator of rows
            return (
                [col.value for col in row]
                for row in sheet.rows
            )

        else:
            raise NotImplemented(
                f"Unknown file extention '{self.filename.suffix}' for "
                f"XlsReader!"
            )
