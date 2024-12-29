from checkpy import *
from shared import outputOfExactStdin, noImport

only("leap_years.py")

output1 = """2000 is a leap year!
2001 is not a leap year.
2002 is not a leap year.
2003 is not a leap year.
2004 is a leap year!
"""
@test()
def test1():
    """Testing 2000, 2005"""
    output = outputOfExactStdin([2000, 2005])
    assert output1.strip() == output.strip()


output2 = """1900 is not a leap year.
1901 is not a leap year.
1902 is not a leap year.
1903 is not a leap year.
1904 is a leap year!
"""
@test()
def test2():
    """Testing 1900, 1905"""
    output = outputOfExactStdin([1900, 1905])
    assert output2.strip() == output.strip()
