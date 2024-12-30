from checkpy import *
from shared import outputOfExactStdin, disallow
import ast

only("eratosthenes.py")

@test()
def noBreakAndImport():
    """Checking for disallowed code."""
    not_allowed = [ast.Break, ast.Import, ast.ImportFrom]
    disallow(not_allowed)


@test()
def test1():
    """Checking input 10"""
    output = outputOfExactStdin([10])
    numbers = static.getNumbersFrom(output)
    assert 4 in numbers

@test()
def test2():
    """Checking input 10.000.000"""
    output = outputOfExactStdin([10000000])
    numbers = static.getNumbersFrom(output)
    assert 664579 in numbers
