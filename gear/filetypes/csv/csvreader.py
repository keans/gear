import csv
import logging
from pathlib import Path
from typing import Union, Any

from gear.filetypes.base.basereader import BaseReader
from gear.filetypes.csv.csvschema import csv_schema
from gear.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class CsvReader(BaseReader):
    """
    CSV reader
    """
    def __init__(
        self,
        filename: Union[str, Path],
        **kwargs
    ):
        BaseReader.__init__(
            self,
            argconfig_schema=csv_schema,
            filename=filename,
            **kwargs
        )

    def __iter__(self):
        """
        iterate over row of pandas dataframe obtained from csv file

        :return: generator that iterates over rows
        :rtype: Generator
        """
        self.ensure_file_is_opened()

        return csv.DictReader(self._f, delimiter=self.argconfig["delimiter"])
