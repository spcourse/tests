from checkpy import *

@test()
def exactWater0():
	"""0 minutes in the shower is 0 bottles of water"""
	assert "0\n" == outputOf(stdinArgs=[0])

@test()
def exactWater10():
	"""10 minutes in the shower is 120 bottles of water"""
	assert "120\n" == outputOf(stdinArgs=[10])

@test()
def exactWater327():
	"""327 minutes in the shower is 3924 bottles of water"""
	assert "3924\n" == outputOf(stdinArgs=[327])
