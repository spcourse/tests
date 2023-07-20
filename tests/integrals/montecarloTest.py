import math

from checkpy import *

only("montecarlo.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def hasMontecarlo():
	"""defines the function montecarlo()"""
	assert "montecarlo" in static.getFunctionDefinitions()

@passed(hasMontecarlo, hide=False)
def correctFunc1():
	"""montecarlo() yields the correct value of an integral on [0,1] for the square function"""
	square = monkeypatch.documentFunction(
		lambda x: x**(x + 0.5),
		"lambda x: x**(x + 0.5)"
	)
	assert getFunction("montecarlo")(square, 0, 0, 1, 1) == approx(0.525, abs=0.015)

@passed(correctFunc1, hide=False)
def correctFunc2():
	"""montecarlo() yields the correct value when an interval does not start at x=0"""
	tanCosSin = monkeypatch.documentFunction(
		lambda x: math.tan(math.cos(math.sin(x))),
		"lambda x: tan(cos(sin(x)))"
	)
	assert getFunction("montecarlo")(tanCosSin, 0.2, 0, 2.2, 1.5) == approx(1.71, abs=0.02)

@passed(correctFunc1, hide=False)
def correctFunc3():
	"""montecarlo() yields the correct value when a function goes below the x-axis"""
	squaredSin = monkeypatch.documentFunction(
		lambda x : math.sin(x**2),
		"lambda x: sin(x**2)"
	)
	assert getFunction("montecarlo")(squaredSin, 0, -1, math.pi, 1) == approx(0.77, abs=0.02)
