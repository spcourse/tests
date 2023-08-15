from checkpy import *

only("riemann.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def hasRiemann():
	"""defines the function riemann()"""
	assert "riemann" in static.getFunctionDefinitions()

@passed(hasRiemann, hide=False)
def correctFunc1():
	"""riemann() yields the correct value for x^2 + x + 1"""
	assert getFunction("riemann")(1, 1, 1, 0, 2, 1000) == approx(6.665, abs=0.005)

@passed(hasRiemann, hide=False)
def correctFunc2():
	"""riemann() yields the correct value when an interval does not start at x=0"""
	assert getFunction("riemann")(1, 0, 0, -2, -1, 1000) == approx(2.335, abs=0.005)

@passed(hasRiemann, hide=False)
def correctFunc3():
	"""riemann() yields the correct value when a function goes below the x-axis"""
	assert getFunction("riemann")(1, 0, -2, -1, 1, 1000) == approx(-3.335, abs=0.005)

@passed(hasRiemann, hide=False)
def correctFunc4():
	"""riemann() yields the correct value of an integral on [-2, 3], with n = 10, for the function -x^2 + 4x + 15"""
	assert getFunction("riemann")(-1, 4, 15, -2, 3, 10) == approx(73.5, abs=0.5)
