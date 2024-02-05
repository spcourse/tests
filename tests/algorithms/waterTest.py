from checkpy import *

only("water.py")

@test()
def exactWater0():
	"""0 minutes in the shower is 0 bottles of water"""
	assert 0 in static.getNumbersFrom(outputOf(stdinArgs=[0]))


@test()
def exactWater10():
	"""10 minutes in the shower is 120 bottles of water"""
	assert 120 in static.getNumbersFrom(outputOf(stdinArgs=[10]))


@test()
def exactWater327():
	"""327 minutes in the shower is 3924 bottles of water"""
	assert 3924 in static.getNumbersFrom(outputOf(stdinArgs=[327]))
