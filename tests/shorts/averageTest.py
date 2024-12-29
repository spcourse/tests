from checkpy import *
from shared import outputOfExactStdin, noImportSum

only("average.py")

@test()
def test1():
	"""Testing 5, 10, 15, -1"""
	output = outputOfExactStdin([5, 10, 15, -1])
	assert "The average of [5.0, 10.0, 15.0] is 10.0." == output.strip()


@test()
def test1():
	"""Testing 1.2, 2.5, 3.8, 0"""
	output = outputOfExactStdin([1.2, 2.5, 3.8, 0])
	assert "The average of [1.2, 2.5, 3.8] is 2.5." == output.strip()
