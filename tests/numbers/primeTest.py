import checkpy.lib as lib
import checkpy.assertlib as assertlib

import ast
from checkpy import *


@test()
def exact1():
	"""input of 1 yields output of 2"""
	assert ast.Break not in static.AbstractSyntaxTree()
	assert ast.List not in static.AbstractSyntaxTree()

	assert 2 in static.getNumbersFrom(outputOf(stdinArgs=[1]))


@passed(exact1, timeout=90, hide=False)
def exact1000():
	"""input of 1000 yields output of 7919"""
	assert 7919 in static.getNumbersFrom(outputOf(stdinArgs=[1000]))


@passed(exact1, timeout=90, hide=False)
def handlesWrongInput():
	"""rejects negative input and rejects input of zero"""
	assert 2 in static.getNumbersFrom(outputOf(stdinArgs=[-90, -1, 0, 1]))
