from checkpy import *
from shared import outputOfExactStdin, noImportSum

only("sum.py")

@test()
def test1():
    """Checking input: 3, 7"""
    output = outputOfExactStdin([3, 7])
    assert "The sum of all numbers from 3 to 7 is 25." == output.strip()

@test()
def test2():
    """Checking input: -1, 1"""
    output = outputOfExactStdin([-1, 1])
    assert "The sum of all numbers from -1 to 1 is 0." == output.strip()
