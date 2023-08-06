import os
import time
import base64
import datetime
from typing import List
from functools import cached_property

# int(datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc).timestamp())
epoch = 1640995200

# 8 bytes
raw_len = 8


def timestamp() -> int:
    """Seconds from epoch"""
    now = int(time.time())
    cid_epoch = now - epoch
    return cid_epoch


def right_timestamp(ts: int) -> int:
    """Seconds from epoch"""
    return ts + epoch


def random_bits(n: int) -> List[int]:
    return list(os.urandom(n))


def generate_eightid() -> List[int]:
    id = [0] * raw_len
    now = timestamp()

    id[0] = (now >> 24) & 0xFF
    id[1] = (now >> 16) & 0xFF
    id[2] = (now >> 8) & 0xFF
    id[3] = (now) & 0xFF

    randb = random_bits(4)

    id[4] = randb[0]
    id[5] = randb[1]
    id[6] = randb[2]
    id[7] = randb[3]

    return id


class InvalidEightID(Exception):
    pass


class EightID(object):
    """
    A short id based on 8 bytes (it fits in a PostgreSQL BigInt).

    32 bites bytes are taken from the timestamp.
    32 bites bytes are random generated (4.294.967.296 of unique numbers).

    The string representation is based on urlsafe_b64, with the padding stripped.

    So it's quite compact, it fits in less than 22 chars.

    """

    __slots__ = ("value", "__dict__")

    def __init__(self, id=None):
        if id is None:
            id = generate_eightid()
        self.value = id

    def __str__(self) -> str:
        return self.string

    def __int__(self) -> int:
        return self.integer

    def __repr__(self) -> str:
        return "<EightID '%s'>" % self.__str__()

    @cached_property
    def string(self) -> str:
        byte_value = self.bytes
        return packing(byte_value)

    @cached_property
    def integer(self):
        """Return the EightID as int."""
        return int.from_bytes(self.value, "big")

    @cached_property
    def random(self) -> int:
        """Return the random part of the EightID."""
        return (
            self.value[4] << 24
            | self.value[5] << 16
            | self.value[6] << 8
            | self.value[7]
        )

    @cached_property
    def datetime(self) -> datetime.datetime:
        """Return the timestamp as datetime."""
        return datetime.datetime.fromtimestamp(self.time)

    @cached_property
    def time(self) -> int:
        """Return the timestamp of the EightID."""
        return right_timestamp(
            self.value[0] << 24
            | self.value[1] << 16
            | self.value[2] << 8
            | self.value[3]
        )

    @cached_property
    def bytes(self) -> bytes:
        """Return the EightID as bytes."""
        return "".join(map(chr, self.value)).encode("utf-8")

    @classmethod
    def from_string(cls, s: str) -> "EightID":
        value = list(map(ord, unpacking(s)))
        return cls(value)

    @classmethod
    def from_int(cls, i: int) -> "EightID":
        value = list(i.to_bytes(8, "big"))
        return cls(value)


def packing(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def unpacking(s: str) -> str:
    padded_s = s + "=="
    try:
        return base64.urlsafe_b64decode(padded_s.encode("utf-8")).decode(
            "utf-8"
        )
    except UnicodeDecodeError:
        raise InvalidEightID("Invalid EightID format.")
