from checkpy import *
from shared import outputOfExactStdin, noImport

only("buzz.py")

@test()
def test1():
	"""Testing 10, 17"""
	output = outputOfExactStdin([10, 17])
	assert "buzz\n11\n12\n13\n14\nbuzz\n16" == output.strip()
