from checkpy import *
from shared import noImportSum

only("geometric_series.py")


@test()
def test_n0():
    """Testing n=0"""
    output = outputOf(stdinArgs=[0])
    numbers = static.getNumbersFrom(output)
    assert approx(1.0, abs=1e-4) in numbers


@test()
def test_n4():
    """Testing n=4"""
    output = outputOf(stdinArgs=[4])
    numbers = static.getNumbersFrom(output)
    assert approx(1.9375, abs=1e-3) in numbers


@test()
def test_n10():
    """Testing n=10"""
    output = outputOf(stdinArgs=[10])
    numbers = static.getNumbersFrom(output)
    assert approx(1.9990234375, abs=1e-6) in numbers
