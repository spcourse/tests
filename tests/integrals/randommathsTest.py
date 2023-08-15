import math

from checkpy import *

only("randommaths.py")

@test()
def correctAmount(test):
	"""randommaths.py yields the correct answer"""
	test.success = "does the number ring familiar?"
	assert approx(math.e, abs=0.0027) in static.getNumbersFrom(outputOf())