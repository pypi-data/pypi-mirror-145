import numpy as np
import pytest

from cactice.distance import hamming_distance, frechet_distance


def test_hamming_distance_ints():
    a = [1, 1, 3, 4, 6, 6]
    b = [1, 2, 3, 4, 5, 6]
    d = hamming_distance(a, b)
    assert d == 2


def test_hamming_distance_strings():
    a = ['hello', 'world', '!']
    b = ['hello', ',', 'world']
    d = hamming_distance(a, b)
    assert d == 2

    a = ['hello', 'world', '!']
    b = ['hello', 'world', '.']
    d = hamming_distance(a, b)
    assert d == 1


def test_hamming_distance_throws_error_when_unequal_lengths():
    a = [1, 1, 3, 4, 6, 6]
    b = [1, 2, 3, 4, 5]
    with pytest.raises(ValueError, match='same length'):
        hamming_distance(a, b)


def test_frechet_distance():
    pass