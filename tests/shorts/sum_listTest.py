from checkpy import *
from shared import noImportSum

only("sum_list.py")


@test()
def test1():
    """Testing 4, 7, 2, -1"""
    output = outputOf(stdinArgs=[4, 7, 2, -1])
    assert "The sum of [4.0, 7.0, 2.0] is 13.0." == output.strip()


@test()
def test2():
    """Testing 1.5, 2.5, 0"""
    output = outputOf(stdinArgs=[1.5, 2.5, 0])
    assert "The sum of [1.5, 2.5] is 4.0." == output.strip()


@test()
def test3():
    """Testing 10, 10, -1"""
    output = outputOf(stdinArgs=[10, 10, -1])
    assert "The sum of [10.0, 10.0] is 20.0." == output.strip()
