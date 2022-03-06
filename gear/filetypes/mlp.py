from gear.filetypes.basefiletype import BaseFileType


class MlpFileType(BaseFileType):
    """
    MLP file type
    """
    def __init__(self, filename):
        BaseFileType.__init__(self, filename)
