from checkpy import *

only("distance.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def hasVierkant():
	"""defines the function square()"""
	assert "square" in static.getFunctionDefinitions()

@passed(hasVierkant, hide=False)
def correctVierkant():
	"""square() yields the correct distance"""
	assert getFunction("square")(10000) == approx(0.525, abs=0.015)
