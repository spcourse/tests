from checkpy import *
from shared import outputOfExactStdin, noImportLoop

only("leap_year.py")

@test()
def test1():
	"""Testing 2004"""
	output = outputOf(stdinArgs=[2004])
	assert "2004 is a leap year!" == output.strip()

@test()
def test2():
	"""Testing 1900"""
	output = outputOf(stdinArgs=[1900])
	assert "1900 is not a leap year." == output.strip()

@test()
def test3():
	"""Testing 2000"""
	output = outputOf(stdinArgs=[2000])
	assert "2000 is a leap year!" == output.strip()
