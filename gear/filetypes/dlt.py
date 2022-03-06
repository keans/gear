from gear.filetypes.basefiletype import BaseFileType


class DltFileType(BaseFileType):
    """
    DLT file type
    """
    def __init__(self, filename):
        BaseFileType.__init__(self, filename)
