from checkpy import *
from inputArgs import outputOfExactStdin

only("first_or_last_year.py")

@test()
def test1():
	"""Testing 2101"""
	output = outputOfExactStdin([2101])
	assert "2101 is the first year of the century!" == output.strip()

@test()
def test2():
	"""Testing 2000"""
	output = outputOfExactStdin([2000])
	assert "2000 is the last year of the century!" == output.strip()

@test()
def test3():
	"""Testing 1999"""
	output = outputOfExactStdin([1999])
	assert "1999 is neither the first nor last year of the century." == output.strip()
