from checkpy import *

import ast

only("collect.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@test()
def test1():
    """input of 0.41"""
    output = outputOf(stdinArgs=[0.41])
    assert "You should return these coins: [25, 10, 5, 1]" == output.strip()

@test()
def test2():
    """input of 0.1"""
    output = outputOf(stdinArgs=[0.1])
    assert "You should return these coins: [10]" == output.strip()

@test()
def test3():
    """input of 4.2"""
    output = outputOf(stdinArgs=[4.2])
    assert "You should return these coins: [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 10, 10]" == output.strip()


@test()
def test4():
    """rejects negative input, then accepts an input of 0.41"""
    output = outputOf(stdinArgs=[-1, -1, 0.41])
    assert "You should return these coins: [25, 10, 5, 1]" == output.strip()
