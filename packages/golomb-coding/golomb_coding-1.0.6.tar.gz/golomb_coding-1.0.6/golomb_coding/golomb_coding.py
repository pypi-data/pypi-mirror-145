"""Module providing didactical tools to show encoding and decoding of the Golomb format."""
from math import ceil, log2
from typing import List

from minimal_binary_coding import minimal_binary_coding, decode_minimal_binary
from unary_coding import inverted_unary, get_len_of_leading_inverted_unary, decode_leading_inverted_unary


def golomb_coding(n: int, b: int) -> str:
    """Return string representing given number in golomb coding.

    Parameters
    ------------------------
    n: int
        Number to convert to golomb coding.
    b: int
        Module.
    """
    return inverted_unary(n // b)+minimal_binary_coding(n % b, b)


def golomb_decoding(golomb_code: str, b: int) -> str:
    """Return integer represented in provided golomb code.

    Parameters
    ------------------------
    golomb_code: str
        Golomb encoding to be converted back.
    b: int
        Module.
    """
    inverted_unary_portion_len = get_len_of_leading_inverted_unary(golomb_code)
    decoded_inverted_unary_portion = decode_leading_inverted_unary(golomb_code)
    decoded_minimal_binary = decode_minimal_binary(
        golomb_code[inverted_unary_portion_len:],
        b
    )
    return decoded_inverted_unary_portion*b + decoded_minimal_binary


def optimal_golomb_coding(n: int, p: float) -> str:
    """Return string representing given number in optimal golomb coding.

    Parameters
    ------------------------
    n: int
        Number to convert to optimal golomb coding.
    p: float
        Probability for given number n.
    """
    return golomb_coding(n, ceil(-1 / log2(1-p)))


def bernoulli_golomb_coding(numbers: List[int]) -> List[str]:
    """Return list of strings representing given numbers in bernoulli golomb coding.

    Parameters
    ------------------------
    numbers: List[int]
        List of numbers to convert to bernoulli golomb coding.
    """
    frequencies = {}
    N = len(numbers)
    for n in numbers:
        frequencies[n] = frequencies.get(n, 0) + 1

    return [
        optimal_golomb_coding(n, frequencies[n]/N)
        for n in numbers
    ]
