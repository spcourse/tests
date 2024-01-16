from checkpy import *

import ast

only("birthday.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"

@passed(noBreakAndImport, timeout=90, hide=False)
def outputsYears():
	"""The code outputs a line containing a number"""
	assert ast.Break not in static.AbstractSyntaxTree()

	result = outputOf(stdinArgs=[1])
	assert 1 == result.count("\n"), "Output should be on one line"

	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 0 < len(numbers), "No year found in the output"


@passed(outputsYears, timeout=90, hide=False)
def check1():
	"""Testing birthday number 1"""
	result = outputOf(stdinArgs=[1])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 2004 in numbers


@passed(outputsYears, timeout=90, hide=False)
def check2():
	"""Testing birthday number 2"""
	result = outputOf(stdinArgs=[2])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 2008 in numbers


@passed(outputsYears, timeout=90, hide=False)
def check3():
	"""Testing birthday number 3"""
	result = outputOf(stdinArgs=[3])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 2012 in numbers, "Hint: A year that is divisible by 4 but not by 100 should be a leap year."


@passed(outputsYears, timeout=90, hide=False)
def check10():
	"""Testing birthday number 10"""
	result = outputOf(stdinArgs=[10])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 2040 in numbers


@passed(outputsYears, timeout=90, hide=False)
def check97():
	"""Testing birthday number 97"""
	result = outputOf(stdinArgs=[97])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 2400 in numbers, "Hint: A year that is divisible by 400 should be a leap year."


@passed(outputsYears, timeout=90, hide=False)
def check500():
	"""Testing birthday number 500"""
	result = outputOf(stdinArgs=[500])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 4060 in numbers


@passed(outputsYears, timeout=90, hide=False)
def check1000():
	"""Testing birthday number 1000"""
	result = outputOf(stdinArgs=[1000])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 6124 in numbers
