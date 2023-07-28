import ast
from checkpy import *

only("fit.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def containsRequiredFunctionDefinitions():
	"""defines the function fit()"""
	assert ast.Break not in static.AbstractSyntaxTree()
	assert "fit" in static.getFunctionDefinitions()

@passed(containsRequiredFunctionDefinitions, hide=False)
def correctC():
	"""prints the best value of c"""
	firstLine = outputOf().split("\n")[0]
	assert approx(60.3, abs=1) in static.getNumbersFrom(firstLine)

@passed(containsRequiredFunctionDefinitions, hide=False)
def correctUncertainy():
	"""prints the uncertainty of c"""
	assert outputOf().count("\n") >= 2, "expected fit.py to print at least two lines of output"

	secondLine = outputOf().split("\n")[1]
	assert approx(1.5, abs=0.1) in static.getNumbersFrom(secondLine)
