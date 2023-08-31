from checkpy import *

import ast
import re

only("listprimes.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@passed(noBreakAndImport, timeout=90, hide=False)
def outputsNumbers():
    """The code outputs numbers"""
    assert ast.Break not in static.AbstractSyntaxTree()

    # Use a regular expression to extract integers from the output string
    output = list(map(int, re.findall(r'\d+', outputOf(stdinArgs=[10]))))

    # Check that at least one number was found in the output
    assert len(output) > 0, "No numbers found in the output. Make sure your program prints numbers."


@passed(outputsNumbers, timeout=90, hide=False)
def validInputHandling():
    """Checks if the program asks for retry on invalid input"""
    # This test checks if the program asks the user to try again
    # when the input is not a whole number bigger than 2.
    actual = list(map(int, re.findall(r'\d+', outputOf(stdinArgs=[2, -5, 1, 10]))))
    assert 7 in actual, "When a user provides a value that is not valid (<= 2), ask the user to try again."


@passed(outputsNumbers, timeout=90, hide=False)
def isListSorted():
    """Checks if the output list of primes is sorted"""
    # This test checks if the output list of prime numbers is sorted in ascending order.
    actual = list(map(int, re.findall(r'\d+', outputOf(stdinArgs=[100]))))
    assert actual == sorted(actual), "The list of prime numbers should be sorted in ascending order."


@passed(outputsNumbers, timeout=90, hide=False)
def correctList10():
	"""Correct list of primes below 10"""
	expected = [2, 3, 5, 7]
	actual = list(map(int, re.findall(r'\d+', outputOf(stdinArgs=[10]))))
	assert actual == expected


@passed(outputsNumbers, timeout=90, hide=False)
def correctList11():
	"""Correct list of primes below 11"""
	expected = [2, 3, 5, 7]
	actual = list(map(int, re.findall(r'\d+', outputOf(stdinArgs=[11]))))
	assert actual == expected
        

@passed(outputsNumbers, timeout=90, hide=False)
def correctList100():
	"""Correct list of primes below 100"""
	expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
	actual = list(map(int, re.findall(r'\d+', outputOf(stdinArgs=[100]))))
	assert actual == expected