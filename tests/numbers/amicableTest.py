from checkpy import *
from shared import outputOfExactStdin, disallow
import ast

only("amicable.py")

@test()
def noBreakAndImport():
    """Checking for disallowed code."""
    not_allowed = [ast.Break, ast.Import, ast.ImportFrom]
    disallow(not_allowed)


@test()
def test1():
    """Checking input 300"""
    output = outputOfExactStdin([300])
    numbers = static.getNumbersFrom(output)
    assert {220, 284} == set(numbers), \
    "expected the amicable numbers 220 and 284\n" +\
    f"you gave: {sorted(list(set(numbers)))}"


@test()
def test2():
    """Checking input 5000"""
    output = outputOfExactStdin([5000])
    numbers = static.getNumbersFrom(output)
    assert {220, 284, 1210, 1184, 2620, 2924} == set(numbers),\
        "expected the amicable numbers 220, 284, 1210, 1184, 2620, and 2924\n" + \
        f"you gave: {sorted(list(set(numbers)))}"
