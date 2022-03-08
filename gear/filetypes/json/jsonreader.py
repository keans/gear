import logging
from pathlib import Path
from typing import Union, Any

import json
from gear.filetypes.base.basereader import BaseReader
from gear.filetypes.json.jsonschema import json_schema
from gear.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class JsonReader(BaseReader):
    """
    JSON reader
    """
    def __init__(
        self,
        filename: Union[str, Path],
        **kwargs
    ):
        BaseReader.__init__(
            self,
            argconfig_schema=json_schema,
            filename=filename,
            **kwargs
        )

    def __iter__(self):
        """
        iterate

        :return: generator that iterates over rows
        :rtype: Generator
        """
        self.ensure_file_is_opened()

        return (j for j in [json.load(self._f)])
