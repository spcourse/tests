from checkpy import *
from inputArgs import outputOfExactStdin

only("first_year.py")

@test()
def test1():
	"""Testing 2101"""
	output = outputOfExactStdin([2101])
	assert "2101 is the first year of the century!" == output.strip()

@test()
def test2():
	"""Testing 1999"""
	output = outputOfExactStdin([1999])
	assert "1999 is not the first year of the century." == output.strip()
