from pathlib import Path

from luigi import Parameter

from gear.utils.typing import PathOrString
from gear.utils.utils import ensure_path


class PathParameter(Parameter):
    """
    path parameter
    """
    def parse(self, s: PathOrString):
        """
        parse string to Path
        """
        return ensure_path(s)
