from checkpy import *
from shared import outputOfExactStdin, noBreakAndImport

only("positive_list.py")


@test()
def test1():
    """Checking input: 1, 2, 0"""
    output = outputOfExactStdin([1, 2, 0])
    assert "My positive number list: [1, 2]" == output.strip()

@test()
def test2():
    """Checking input: 18, 5, -1"""
    output = outputOfExactStdin([18, 5, -1])
    assert "My positive number list: [18, 5]" == output.strip()
