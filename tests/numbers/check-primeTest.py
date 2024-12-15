from checkpy import *
from inputArgs import outputOfExactStdin

import ast

only("check-prime.py")


@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"

@passed(noBreakAndImport, timeout=90, hide=False)
@test()
def test1():
	"""Testing 9"""
	output = outputOfExactStdin([9])
	assert "9 is not a prime number." == output.strip()

@passed(noBreakAndImport, timeout=90, hide=False)
@test()
def test2():
	"""Testing 11"""
	output = outputOfExactStdin([11])
	assert "11 is a prime number!" == output.strip()

@passed(noBreakAndImport, timeout=90, hide=False)
@test()
def test3():
	"""Testing 2"""
	output = outputOfExactStdin([2])
	assert "2 is a prime number!" == output.strip()

@passed(noBreakAndImport, timeout=90, hide=False)
@test()
def test4():
	"""Testing 1"""
	output = outputOfExactStdin([1])
	assert "1 is not a prime number." == output.strip()
