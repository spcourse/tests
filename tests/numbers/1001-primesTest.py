from checkpy import *
from inputArgs import outputOfExactStdin

import ast

only("1001-primes.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@passed(noBreakAndImport, timeout=90, hide=False)
def outputsPrimes():
	"""the code outputs a line containing a number"""
	assert ast.Break not in static.AbstractSyntaxTree()

	result = outputOf(stdinArgs=[1])
	assert 1 == result.count("\n"), "Output should be on one line"

	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert 0 < len(numbers), "No number found in the output"


@passed(noBreakAndImport, timeout=90, hide=False)
def handlesWrongInput():
	"""rejects negative input and rejects input of zero"""
	assert 2 in static.getNumbersFrom(outputOf(stdinArgs=[-90, -1, 0, 1]))


@passed(noBreakAndImport, timeout=90, hide=False)
def noExtraOutput():
    """checks if the program only outputs the prime number"""
    result = outputOf(stdinArgs=[5])
    assert result.strip().isdigit(), "Ensure that your program only outputs the prime number without any extra text or characters."


@passed(noBreakAndImport, timeout=90, hide=False)
def exact1():
	"""input of 1 yields output of 2"""
	assert ast.Break not in static.AbstractSyntaxTree()
	assert ast.List not in static.AbstractSyntaxTree()

	assert 2 in static.getNumbersFrom(outputOf(stdinArgs=[1]))


@passed(exact1, timeout=90, hide=False)
def doesNotSkipPrimes():
    """ensures no primes are skipped"""
    assert 3 in static.getNumbersFrom(outputOf(stdinArgs=[2])), "The second prime number is 3. Make sure your program is not skipping any primes."


@passed(exact1, timeout=90, hide=False)
def exact1001():
	"""input of 1001 yields output of 7927"""
	assert 7927 in static.getNumbersFrom(outputOf(stdinArgs=[1001]))
