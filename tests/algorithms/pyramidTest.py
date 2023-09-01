from checkpy import *

import ast
import re

only("pyramid.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@passed(noBreakAndImport, hide=False)
def noStringMultiplication():
    """the program does not use string multiplication"""
    stringVars = getStringVars()
    ops = [binOp for binOp in static.getAstNodes(ast.BinOp) if isinstance(binOp.op, ast.Mult)]

    for op in ops:
        if (
            isinstance(op.left, ast.Str)
            or (isinstance(op.left, ast.Name) and op.left.id in stringVars)
        ):
            line = static.getSource().split('\n')[op.lineno - 1]
            raise AssertionError(
                f"String multiplication is used on line {op.lineno}:\n"
                f"    {line}\n"
                f"Try to tackle this assignment without string multiplication."
            )


@passed(noBreakAndImport, noStringMultiplication, hide=False)
def handlesWrongInput():
    """rejects heights of -100 and 24, then accepts a height of 3"""
    output = outputOf(stdinArgs=[-100, 24, 3])
    assert '#' in output, "expected the program to print a pyramid"


@passed(noBreakAndImport, noStringMultiplication, hide=False)
def exactMario1():
    """prints a well-formed pyramid of height 1"""

    pyramid, regex = getPyramid(1)
    if regex.match(outputOf(stdinArgs=[1])) is None:
        assert outputOf(stdinArgs=[1]) == pyramid


@passed(exactMario1, hide=False)
def exactMario3():
    """prints a well-formed pyramid of height 3"""
    pyramid, regex = getPyramid(3)
    if regex.match(outputOf(stdinArgs=[3])) is None:
        assert outputOf(stdinArgs=[3]) == pyramid


@passed(exactMario3, hide=False)
def exactMario23():
    """prints a well-formed pyramid of height 23"""
    pyramid, regex = getPyramid(23)
    if regex.match(outputOf(stdinArgs=[23])) is None:
        assert outputOf(stdinArgs=[23]) == pyramid


def getLine(i, height):
    return (height - i - 1) * "  " + " ".join("#" for i in range(i + 2))


def getPyramid(height):
    pyramid = [getLine(i, height) for i in range(height)]
    regex = ".*"
    for line in pyramid:
        regex += f"({line})[ ]*(\n)"
    regex += ".*"
    return "\n".join(pyramid), re.compile(regex, re.MULTILINE)


def getStringVars():
    """get variables that are assigned a string in the AST"""
    assignments = static.getAstNodes(ast.Assign)
    vars = set()
    for assignment in assignments:
        for target in assignment.targets:
            if isinstance(target, ast.Name):
                if (isinstance(assignment.value, ast.Str) 
                    or (isinstance(assignment.value, ast.Name) and assignment.value.id in vars)):
                    vars.add(target.id)
    return vars
