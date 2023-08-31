from checkpy import *

import ast
import re

only("pyramid.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@passed(noBreakAndImport, hide=False)
def noStringMultiplication():
    """the program does not use string multiplication"""
    assert ast.Mult not in static.AbstractSyntaxTree()


@passed(noStringMultiplication, hide=False)
def handlesWrongInput():
	"""rejects heights of -100 and 24, then accepts a height of 3"""
	output = outputOf(stdinArgs=[-100, 24, 3])
	assert '#' in output, "expected the program to print a pyramid"


@passed(noBreakAndImport, hide=False)
def exactMario1():
	"""prints a well-formed pyramid of height 1"""

	pyramid, regex = getPyramid(1)
	if regex.match(outputOf(stdinArgs=[1])) is None:
		assert outputOf(stdinArgs=[1]) == pyramid


@passed(exactMario1, hide=False)
def exactMario3():
	"""prints a well-formed pyramid of height 3"""
	pyramid, regex = getPyramid(3)
	if regex.match(outputOf(stdinArgs=[3])) is None:
		assert outputOf(stdinArgs=[3]) == pyramid


@passed(exactMario3, hide=False)
def exactMario23():
	"""prints a well-formed pyramid of height 23"""
	pyramid, regex = getPyramid(23)
	if regex.match(outputOf(stdinArgs=[23])) is None:
		assert outputOf(stdinArgs=[23]) == pyramid


def getLine(i, height):
	return (height - i - 1) * "  " + " ".join("#" for i in range(i + 2))


def getPyramid(height):
	pyramid = [getLine(i, height) for i in range(height)]
	regex = ".*"
	for line in pyramid:
		regex += f"({line})[ ]*(\n)"
	regex += ".*"
	return "\n".join(pyramid), re.compile(regex, re.MULTILINE)