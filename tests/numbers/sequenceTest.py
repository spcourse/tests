import ast
from checkpy import *

@test(timeout=90)
def correctBarriers():
	"""prints the correct start and end of the sequence"""
	assert ast.Break not in static.AbstractSyntaxTree()

	firstLine = outputOf().split("\n")[0]
	assert "9552" in firstLine and "9586" in firstLine, "note that primes are not actually part of the sequence!"


@passed(correctBarriers, timeout=90, hide=False)
def correctDistance():
	"""prints the correct length of the sequence"""
	output = outputOf()
	assert 2 == output.count("\n"), "expected exactly 2 lines of output"

	secondLine = output.split("\n")[1]
	assert "35" in secondLine, "is the length printed on the second line?"
