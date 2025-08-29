from checkpy import *
from shared import outputOfExactStdin, noBreakAndImport

only("positive.py")


@test()
def test1():
    """Checking input: -1, -2, 0, 18"""
    output = outputOf(stdinArgs=[-1, -2, 0, 18])
    assert "Great, 18 is a positive number!" == output.strip()

@test()
def test2():
    """Checking input: 5"""
    output = outputOf(stdinArgs=[5])
    assert "Great, 5 is a positive number!" == output.strip()
