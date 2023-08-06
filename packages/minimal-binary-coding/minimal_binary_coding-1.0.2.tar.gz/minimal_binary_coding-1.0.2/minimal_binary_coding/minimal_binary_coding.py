"""Module providing implementation of encoding and decoding of minimal binary code."""
from math import log2, ceil


def get_maximal_code_length(b: int) -> int:
    """Return the maximal length of the code."""
    return ceil(log2(b))


def minimal_binary_coding(n: int, b: int) -> str:
    """Return string representing given number in minimal binary coding.

    Parameters
    -------------------------
    n: int
        Number to convert to minimal binary encoding.
    b: int
        Maximal size.
    """
    if n == 0 and b == 1:
        return ""
    code_maximal_len = get_maximal_code_length(b)
    if n < 2**code_maximal_len - b:
        return f"{{0:0{code_maximal_len-1}b}}".format(n)
    return f"{{0:0{code_maximal_len}b}}".format(n-b+2**code_maximal_len)


def decode_minimal_binary(minimal_binary_code: str, b: int) -> int:
    """Return integer obtained decoding provided minimal binary string.

    Parameters
    -------------------------
    minimal_binary_code: str
        The minimal binary code to convert back to integer
    b: int
        Maximal size.
    """
    code_maximal_len = get_maximal_code_length(b)

    if len(minimal_binary_code) != code_maximal_len:
        return int(minimal_binary_code, 2)

    return int(minimal_binary_code, 2) + b - 2**code_maximal_len
