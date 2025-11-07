from checkpy import *
from shared import outputOfExactStdin, disallow
import ast

only("eratosthenes.py")

@test()
def noBreakAndImport():
    """Checking for disallowed code."""
    imports = static.getAstNodes(ast.Import)
    for node in imports:
        for alias in node.names:
            if alias.name != "math":
                raise AssertionError("you cannot use import statements (only 'import math' is allowed)")

    if static.getAstNodes(ast.ImportFrom):
        raise AssertionError("you cannot use import statements (only 'import math' is allowed)")

    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"

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
