from checkpy import *
from shared import outputOfExactStdin, noImport

only("between.py")

@test()
def test1():
	"""Testing  3, 8"""
	output = outputOfExactStdin([3, 8])
	assert "3\n4\n5\n6\n7" == output.strip()
