from gear.filetypes.basefiletype import BaseFileType


class PcapFileType(BaseFileType):
    """
    Pcap file type
    """
    def __init__(self, filename):
        BaseFileType.__init__(self, filename)
