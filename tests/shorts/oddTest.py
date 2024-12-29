from checkpy import *
from shared import outputOfExactStdin, noImportSum

only("odd.py")


@test()
def test1():
    """Checking input: 1, 2, 0"""
    output = outputOfExactStdin([1, 2, 0])
    assert "The list [1, 2] contains these odd numbers [1]." == output.strip()


@test()
def test2():
    """Checking input: 8, 15, 23, 42, -1"""
    output = outputOfExactStdin([8, 15, 23, 42, -1])
    assert "The list [8, 15, 23, 42] contains these odd numbers [15, 23]." == output.strip()
