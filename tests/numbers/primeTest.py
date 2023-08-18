import ast
from checkpy import *

@test(timeout=90)
def outputsPrimes():
	"""the code outputs a line containing a number"""
	assert ast.Break not in static.AbstractSyntaxTree()

	result = outputOf(stdinArgs=[1])
	assert result.count("\n") == 1, "Output should be on one line"

	numbers = static.getNumbersFrom(result.split('\n')[0])
	assert len(numbers) > 0, "No number found in the output"

@test(timeout=90)
def noExtraOutput():
    """checks if the program only outputs the prime number"""
    result = outputOf(stdinArgs=[5])
    assert result.strip().isdigit(), "Ensure that your program only outputs the prime number without any extra text or characters."

@test(timeout=90)
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
def exact1000():
	"""input of 1000 yields output of 7919"""
	assert 7919 in static.getNumbersFrom(outputOf(stdinArgs=[1000]))


@passed(exact1, timeout=90, hide=False)
def handlesWrongInput():
	"""rejects negative input and rejects input of zero"""
	assert 2 in static.getNumbersFrom(outputOf(stdinArgs=[-90, -1, 0, 1]))