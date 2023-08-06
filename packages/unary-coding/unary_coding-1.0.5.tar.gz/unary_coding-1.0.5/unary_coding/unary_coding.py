def _unary(n: int, zero: str, one: str) -> str:
    return one*n + zero


def unary(n: int) -> str:
    """Return string representing given number in unary.
        n:int, number to convert to unary.
    """
    return _unary(n, "0", "1")


def inverted_unary(n: int) -> str:
    """Return string representing given number in inverted unary.
        n:int, number to convert to unary.
    """
    return _unary(n, "1", "0")


def decode_leading_unary(string_starting_with_unary: str) -> int:
    """Returns decoded unary value."""
    return string_starting_with_unary.index("0")


def decode_leading_inverted_unary(string_starting_with_inverted_unary: str) -> int:
    """Returns decoded unary value."""
    return string_starting_with_inverted_unary.index("1")


def get_len_of_leading_unary(string_starting_with_unary: str) -> int:
    """Returns length of leading unary portion in string."""
    return decode_leading_unary(string_starting_with_unary) + 1


def get_len_of_leading_inverted_unary(string_starting_with_inverted_unary: str) -> int:
    """Returns length of leading inverted unary portion in string."""
    return decode_leading_inverted_unary(string_starting_with_inverted_unary) + 1
