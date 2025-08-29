from checkpy import *
from shared import outputOfExactStdin, noBreakAndImport

only("max_until.py")


@test()
def test1():
    """Checking input: 4, 5, 9, 1, 2, 0"""
    output = outputOf(stdinArgs=[4, 5, 9, 1, 2, 0])
    assert "The biggest number you entered was 9." == output.strip()

@test()
def test2():
    """Checking input: -11"""
    output = outputOf(stdinArgs=[-11])
    assert "The biggest number you entered was -11." == output.strip()
