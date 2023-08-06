"""Module providing methods to encode and decode unary coding."""
from .unary_coding import unary, inverted_unary, get_len_of_leading_inverted_unary, get_len_of_leading_unary, decode_leading_inverted_unary, decode_leading_unary

__all__ = [
    "unary",
    "inverted_unary",
    "get_len_of_leading_inverted_unary",
    "get_len_of_leading_unary",
    "decode_leading_inverted_unary",
    "decode_leading_unary"
]
