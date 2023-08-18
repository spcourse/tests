import ast
from checkpy import *

only("leap.py")


@test(timeout=90)
def outputsYears():
	"""Prints years"""
	assert ast.Break not in static.AbstractSyntaxTree()
	
	numbers = static.getNumbersFrom(outputOf(stdinArgs=[2000, 2010]))
	assert len(numbers) > 0		


@passed(outputsYears, timeout=90, hide=False)
def outputsOneYearPerLine():
	"""Prints exactly one year per line"""
	result = outputOf(stdinArgs=[2000, 2010])

	for line in result.split("\n"):
		if line.strip() == "":
			continue

		years = static.getNumbersFrom(line)
		assert len(years) == 1


@passed(outputsOneYearPerLine, timeout=90, hide=False)
def leapYearsStraight():
	"""Prints leap years between 2004 and 2013"""
	expected = [2004, 2008, 2012]
	actual = sorted(set(static.getNumbersFrom(outputOf(stdinArgs=[2004, 2013]))))
	assert actual == expected


@passed(outputsOneYearPerLine, timeout=90, hide=False)
def leapYears100():
	"""Prints leap years between 1890 and 1920; every 100th year is not a leap year"""
	expected = [1892, 1896, 1904, 1908, 1912, 1916]
	actual = sorted(set(static.getNumbersFrom(outputOf(stdinArgs=[1890, 1920]))))
	assert actual == expected, "Did you implement a rule such that every 100th year is not a leap year?"
	

@passed(outputsOneYearPerLine, timeout=90, hide=False)
def leapYears400():
	"""Prints leap years between 1990 and 2020; every 400th year is a leap year"""
	expected = [1992, 1996, 2000, 2004, 2008, 2012, 2016]
	actual = sorted(set(static.getNumbersFrom(outputOf(stdinArgs=[1990, 2020]))))
	assert actual == expected, "Did you implement a rule such that every 400th year is a leap year?"


@test(timeout=90)
def handlesEqualYears():
    """Handles equal first and last year correctly"""
    assert ast.Break not in static.AbstractSyntaxTree()
    
    result = outputOf(stdinArgs=[2000, 2000, 2010])
    expected = [2000, 2004, 2008]
    actual =  sorted(set(static.getNumbersFrom(result)))
    assert actual == expected, "Did you ensure that the program asks for a new last year when the first year is equal to the last year?"


@test(timeout=90)
def handlesDecreasingYears():
    """Handles decreasing years correctly"""
    assert ast.Break not in static.AbstractSyntaxTree()
    
    result = outputOf(stdinArgs=[2000, 1990, 2010])
    expected = [2000, 2004, 2008]
    actual =  sorted(set(static.getNumbersFrom(result)))
    assert actual == expected, "Did you ensure that the program asks for a new last year when the first year is greater than the last year?"


@test(timeout=90)
def leapYearAt400Boundary():
    """Identifies a year that is a multiple of 400 as a leap year"""
    assert ast.Break not in static.AbstractSyntaxTree()
    
    result = outputOf(stdinArgs=[2400, 2401])
    expected = [2400]
    actual =  sorted(set(static.getNumbersFrom(result)))
    assert actual == expected, "Did you implement the rule that every 400th year is a leap year?"


@test(timeout=90)
def nonLeapYearAt100Boundary():
    """Identifies a year that is a multiple of 100 (but not 400) as a non-leap year"""
    assert ast.Break not in static.AbstractSyntaxTree()
    
    result = outputOf(stdinArgs=[1900, 1901])
    expected = []
    actual =  sorted(set(static.getNumbersFrom(result)))
    assert actual == expected, "Did you implement the rule that every 100th year is not a leap year, unless it is a 400th year?"
