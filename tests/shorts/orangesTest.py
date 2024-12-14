from checkpy import *
from inputArgs import outputOfExactStdin

only("oranges.py")

@test()
def test1():
	"""Divide: checking 17 oranges and 4 baskets"""
	output = outputOfExactStdin([17, 4])
	numbers = static.getNumbersFrom(output)
	assert 4 == numbers[0], "expected 4 oranges per basket"
	assert 1 == numbers[1], "expected 1 orange left over"

@test()
def test2():
	"""Divide: checking 1 oranges and 3 baskets"""
	output = outputOfExactStdin([1, 3])
	numbers = static.getNumbersFrom(output)
	assert 0 == numbers[0], "expected 0 oranges per basket"
	assert 1 == numbers[1], "expected 1 orange left over"
