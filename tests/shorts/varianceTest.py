from checkpy import *
from shared import noImportSum

only("variance.py")


@test()
def test1():
    """Testing 2, 4, 4, 6, -1"""
    output = outputOf(stdinArgs=[2, 4, 4, 6, -1])
    assert "The variance of [2.0, 4.0, 4.0, 6.0] is 2.0." == output.strip()


@test()
def test2():
    """Testing 1, 3, 0"""
    output = outputOf(stdinArgs=[1, 3, 0])
    assert "The variance of [1.0, 3.0] is 1.0." == output.strip()


@test()
def test3():
    """Testing 5, 5, 5, -1"""
    output = outputOf(stdinArgs=[5, 5, 5, -1])
    assert "The variance of [5.0, 5.0, 5.0] is 0.0." == output.strip()
