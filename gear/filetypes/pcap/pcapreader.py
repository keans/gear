from pathlib import Path
from typing import Union

import dpkt

from gear.filetypes.base.basereader import BaseReader
from gear.filetypes.pcap.pcapschema import pcap_schema


class PcapReader(BaseReader):
    """
    Pcap reader (.pcap and .pcapng)
    """
    def __init__(
        self,
        filename: Union[str, Path],
        **kwargs
    ):
        BaseReader.__init__(
            self,
            argconfig_schema=pcap_schema,
            filename=filename,
            is_binary=True,
            **kwargs
        )

    def __iter__(self):
        """
        iterate over row of frames of pcap file

        :return: generator that iterates over rows
        :rtype: Generator
        """
        if self.filename.suffix == ".pcap":
            pcap = dpkt.pcap.Reader(self._f)

        elif self.filename.suffix == ".pcapng":
            pcap = dpkt.pcapng.Reader(self._f)

        else:
            raise NotImplemented(
                f"Unknown file extention '{self.filename.suffix}' for "
                f"PcapReader!"
            )

        return ((ts, dpkt.ethernet.Ethernet(buf)) for ts, buf in pcap)
