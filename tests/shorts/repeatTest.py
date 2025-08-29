from checkpy import *
from shared import noBreakAndImport, outputOfExactStdin
import ast
import typing


only("repeat.py")

@test()
def noStringMultiplication():
    """the program does not use string multiplication"""
    stringVars = getStringVars()
    ops = [binOp for binOp in static.getAstNodes(ast.BinOp) if isinstance(binOp.op, ast.Mult)]

    for op in ops:
        if (
            isinstance(op.left, ast.Str)
            or (isinstance(op.left, ast.Name) and op.left.id in stringVars)
            or isinstance(op.right, ast.Str)
            or (isinstance(op.right, ast.Name) and op.right.id in stringVars)
        ):
            line = static.getSource().split('\n')[op.lineno - 1]
            raise AssertionError(
                f"String multiplication is used on line {op.lineno}:\n"
                f"    {line}\n"
                f"Try to tackle this assignment without string multiplication."
            )

@test()
def test1():
    """Testing hello, 5"""
    output = outputOf(stdinArgs=["hello", 5])
    assert "hellohellohellohellohello" == output.strip()
    assert "hellohellohellohellohello\n" == output, "you forgot a new-line at the end of your output"

@test()
def test2():
    """Testing #, 18"""
    output = outputOf(stdinArgs=["#", 18])
    assert "##################" == output.strip()
    assert "##################\n" == output, "you forgot a new-line at the end of your output"



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
