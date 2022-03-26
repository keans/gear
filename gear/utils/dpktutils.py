import socket

import dpkt
from dpkt.compat import compat_ord


def mac_addr(address: bytes) -> str:
    """
    returns human-readable string of MAC address

    :param address: MAC address bytes
    :type address: bytes
    :return: human-readable string of MAC address
    :rtype: str
    """
    return ":".join([f"{b:02X}" for b in map(compat_ord, address)])


def inet_to_str(inet: bytes) -> str:
    """
    returns human-readable string of IP address

    :param inet: IP address bytes
    :type inet: bytes
    :return: human-readable string of IP address
    :rtype: str
    """
    try:
        # try IPv4 address
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        # try IPv6 address
        return socket.inet_ntop(socket.AF_INET6, inet)
