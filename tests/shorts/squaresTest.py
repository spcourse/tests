from checkpy import *
from shared import outputOfExactStdin, noBreakAndImport

only("squares.py")


@test()
def test1():
    """Checking input: 2, 3, 4, -1"""
    output = outputOfExactStdin([2, 3, 4, -1])
    assert "The squares of [2.0, 3.0, 4.0] are [4.0, 9.0, 16.0]." == output.strip()

@test()
def test2():
    """Checking input: 1.5, 2.5, 0"""
    output = outputOfExactStdin([1.5, 2.5, 0])
    assert "The squares of [1.5, 2.5] are [2.25, 6.25]." == output.strip()
