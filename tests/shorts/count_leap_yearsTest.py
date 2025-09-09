from checkpy import *
from shared import outputOfExactStdin, noImport

only("count_leap_years.py")


@test()
def test1():
    """Testing 2000, 2021"""
    output = outputOf(stdinArgs=[2000, 2021])
    numbers = static.getNumbersFrom(output)
    assert 6 in numbers
