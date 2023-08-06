import struct
from enum import Enum, auto


class CompressionFormat(Enum):
    Unknown = auto()
    Zstandard = auto()


def detect_compression(file: str) -> CompressionFormat:
    with open(file, "rb") as f:
        try:
            h = struct.unpack("<I", f.read(4))[0]
        except struct.error:
            h = None
    if h == 0xFD2FB528:
        return CompressionFormat.Zstandard
    return CompressionFormat.Unknown
