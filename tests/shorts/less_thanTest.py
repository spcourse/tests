from checkpy import *
from shared import outputOfExactStdin, noImportLoop

only("less_than.py")

@test()
def test1():
	"""Checking input 5.0"""
	output = outputOf(stdinArgs=[5.0])
	assert "5.0 is smaller than 10.0!" == output.strip()

@test()
def test2():
	"""Checking input 15.5"""
	output = outputOf(stdinArgs=[15.5])
	assert "15.5 is not smaller than 10.0!" == output.strip()

@test()
def test3():
	"""Checking input 10.0"""
	output = outputOf(stdinArgs=[10.0])
	assert "10.0 is not smaller than 10.0!" == output.strip()
