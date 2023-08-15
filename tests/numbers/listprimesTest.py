import ast
from checkpy import *

only("listprimes.py")


@test(timeout=90)
def outputsNumbers():
	"""The code outputs numbers"""
	assert ast.Break not in static.AbstractSyntaxTree()

	numbers = static.getNumbersFrom(outputOf(stdinArgs=[10]))
	assert len(numbers) > 0		


@passed(outputsNumbers, timeout=90, hide=False)
def correctList10():
	"""Correct list of primes below 10"""
	expected = [2, 3, 5, 7]
	actual = sorted(set(static.getNumbersFrom(outputOf(stdinArgs=[10]))))
	assert actual == expected


@passed(outputsNumbers, timeout=90, hide=False)
def correctList11():
	"""Correct list of primes below 11"""
	expected = [2, 3, 5, 7]
	actual = sorted(set(static.getNumbersFrom(outputOf(stdinArgs=[11]))))
	assert actual == expected


@passed(outputsNumbers, timeout=90, hide=False)
def correctList100():
	"""Correct list of primes below 100"""
	expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
	actual = sorted(set(static.getNumbersFrom(outputOf(stdinArgs=[100]))))
	assert actual == expected
