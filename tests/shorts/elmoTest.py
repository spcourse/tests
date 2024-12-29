from checkpy import *
from shared import outputOfExactStdin, noBreakAndImport

only("elmo.py")

@test()
def test1():
    """Testing Elmo"""
    output = outputOfExactStdin(["Elmo"])
    assert "Elmo is so happy to see you!" == output.strip()

@test()
def test2():
    """Testing Cookie, Big Bird, Elmo"""
    output = outputOfExactStdin(["Cookie", "Big Bird", "Elmo"])
    assert "Elmo is so happy to see you!" == output.strip()
