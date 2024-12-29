from checkpy import *
from shared import outputOfExactStdin, noImportPow

only("newton.py")

@test()
def test1():
    """Checking input 25"""
    output = outputOfExactStdin([25])
    numbers = static.getNumbersFrom(output)
    assert approx(5.0, abs=0.0001) in numbers


@test()
def test2():
    """Checking input 9"""
    output = outputOfExactStdin([9])
    numbers = static.getNumbersFrom(output)
    assert approx(3.0, abs=0.0001) in numbers
