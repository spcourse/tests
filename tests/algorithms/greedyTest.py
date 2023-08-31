from checkpy import *

import ast

only("greedy.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@passed(noBreakAndImport, hide=False)
def handlesWrongInput():
	"""rejects negative input, then accepts an input of 0.41"""
	assert "4\n" == outputOf(stdinArgs=[-1, -1, 0.41])


@passed(noBreakAndImport, hide=False)
def exactChange0():
	"""input of 0 yields output of 0"""
	assert "0\n" == outputOf(stdinArgs=[0])


@passed(noBreakAndImport, hide=False)
def exactChange41():
	"""input of 0.41 yields output of 4"""
	assert "4\n" == outputOf(stdinArgs=[0.41])

@passed(noBreakAndImport, hide=False)
def exactChange001():
	"""input of 0.01 yields output of 1"""
	assert "1\n" == outputOf(stdinArgs=[0.01])


@passed(noBreakAndImport, hide=False)
def exactChange16():
	"""input of 1.6 yields output of 7"""
	assert "7\n" == outputOf(stdinArgs=[1.6])


@passed(noBreakAndImport, hide=False)
def exactChange420():
	"""input of 4.2 yields output of 18"""
	assert "18\n" == outputOf(stdinArgs=[4.2]), "did you forget to round your input to the nearest cent?"