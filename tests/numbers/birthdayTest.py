import ast
from checkpy import *

only("birthday.py")


@test(timeout=90)
def outputsYears():
	"""The code outputs a line containing a number"""
	assert ast.Break not in static.AbstractSyntaxTree()

	result = outputOf(stdinArgs=[1])
	assert result.count("\n") == 1, "Output should be on one line"

	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert len(numbers) > 0, "No year found in the output"
	

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
def check1000():
	"""Testing birthday number 1000"""
	result = outputOf(stdinArgs=[1000])
	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 6124 in numbers