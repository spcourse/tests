from checkpy import *

only("plot.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()


@test()
def showsGraph():
	"""Either saves a graph into a file, or shows a graph on the screen."""
	assert "savefig" in static.getFunctionCalls() or "show" in static.getFunctionCalls()


@test()
def givesMin():
	"""prints the correct minimum as text"""
	assert "min" not in static.getFunctionCalls(), "make sure not to use the min() function while solving this problem"
	
	numbers = static.getNumbersFrom(outputOf())
	assert approx(0.37, abs=0.05) in numbers and approx(0.69, abs=0.05) in numbers
