from checkpy import *
from shared import outputOfExactStdin, noBreakAndImport

only("sum_until.py")

@test()
def test1():
    """Checking input: 9"""
    output = outputOf(stdinArgs=[9])
    assert "The sum of all numbers from 1 to 4 is 10 " + \
    "(which is bigger or equal to 9)." == output.strip()

@test()
def test2():
    """Checking input: 15"""
    output = outputOf(stdinArgs=[15])
    assert "The sum of all numbers from 1 to 5 is 15 " + \
    "(which is bigger or equal to 15)." == output.strip()
