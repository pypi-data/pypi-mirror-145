import secrets
from base64 import b16encode
from struct import pack
from zlib import adler32


def checksum(to_hash: str) -> str:
    """
    Base 16 string of half the adler32 checksum
    """
    adler32_hash = adler32(bytes(to_hash, "utf-8"))
    return b16encode(pack("I", adler32_hash)).decode("utf-8").lower()[-4:]


def random_machine_id() -> str:
    """
    These used to be 64 hex characters. Now they have a new format.
    """
    to_hash = f"ss_m_{secrets.token_hex(11)}"
    return f"{to_hash}_{checksum(to_hash)}"


def random_token() -> str:
    """
    64 hex characters.
    """
    return secrets.token_hex(32)
