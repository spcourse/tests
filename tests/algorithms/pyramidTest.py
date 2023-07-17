from checkpy import *

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from notAllowedCode import *


@test()
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
	""""prints a well-formed pyramid of height 23"""
	pyramid, regex = getPyramid(23)
	if regex.match(outputOf(stdinArgs=[23])) is None:
		assert outputOf(stdinArgs=[23]) == pyramid


@passed(exactMario3, hide=False)
def handlesWrongInput():
	""""rejects heights of -100 and 24, then accepts a height of 3"""
	notAllowedCode({
		"the * operator, but instead loops": "*"
	})
	output = outputOf(stdinArgs=[-100, 24, 3])
	pyramid, regex = getPyramid(3)
	if regex.match(output) is None:
		assert output == pyramid


def getLine(i, height):
	return (height - i - 1) * "  " + " ".join("#" for i in range(i + 2))


def getPyramid(height):
	pyramid = [getLine(i, height) for i in range(height)]
	regex = ".*"
	for line in pyramid:
		regex += f"({line})[ ]*(\n)"
	regex += ".*"
	return "\n".join(pyramid), re.compile(regex, re.MULTILINE)