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
	assert 0.51 <= getFunction("square")(10000) <= 0.54
