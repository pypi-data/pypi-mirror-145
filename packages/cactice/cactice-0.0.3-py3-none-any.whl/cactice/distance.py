from typing import List, Tuple, Any


def hamming_distance(a: List[Any], b: List[Any]) -> int:
    """
    Computes the Hamming distance between the lists (first casting their elements to strings).
    Lists must be the same length. Adapted from https://stackoverflow.com/a/54174768/6514033.

    :param a: The first list
    :param b: The second list
    :return: The Hamming distance between the lists interpreted as strings
    """

    # make sure lists are the same length
    if len(a) != len(b):
        raise ValueError(f"Lists must be the same length")

    # count pairs of elements which aren't equal
    return sum(ac != bc for ac, bc in zip(a, b))


def frechet_distance(a: List[Tuple[float, float]], b: List[Tuple[float, float]]) -> float:
    # TODO
    # reference impl: https://gist.github.com/MaxBareiss/ba2f9441d9455b56fbc9
    pass
