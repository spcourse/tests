
from checkpy import *

@test()
def exact3492times9876():
	"""input of 3492 and 9876 yields 34486992"""
	assert 34486992 in static.getNumbersFrom(outputOf(stdinArgs=[3492, 9876]))
