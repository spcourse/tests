from checkpy import *

only("whiz.py")

@test()
def exact0times0():
	"""input of 0 and 0 yields 0"""
	assert 0 in static.getNumbersFrom(outputOf(stdinArgs=[0, 0]))


@test()
def exact4times4():
	"""input of 4 and 4 yields 16"""
	assert 16 in static.getNumbersFrom(outputOf(stdinArgs=[4, 4]))


@test()
def exact3492times9876():
	"""input of 3492 and 9876 yields 34486992"""
	assert 34486992 in static.getNumbersFrom(outputOf(stdinArgs=[3492, 9876]))