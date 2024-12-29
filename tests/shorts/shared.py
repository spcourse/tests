from checkpy import *
from checkpy.entities.exception import InputError

def outputOfExactStdin(args):
    try:
        # test with one fewer args
        output = outputOf(stdinArgs=args[:-1])
    except InputError as e:
        # if to few args: test with all the args
        return outputOf(stdinArgs=args)
    assert False, "expected the program to ask more user input"
import ast

@test()
def noBreakAndImport():
    """Checking for disallowed code."""
    not_allowed = [ast.Break, ast.Import, ast.ImportFrom]
    disallow(not_allowed)

@test()
def noImportLoop():
    """Checking for disallowed code."""
    not_allowed = [ast.For, ast.While, ast.Import, ast.ImportFrom]
    disallow(not_allowed)

@test()
def noImportSum():
    """Checking for disallowed code."""
    not_allowed = ["sum", ast.Import, ast.ImportFrom]
    disallow(not_allowed)

@test()
def noImportLoopSubAdd():
    """Checking for disallowed code."""
    not_allowed = [ast.For, ast.While, ast.Sub, ast.Add, ast.Import, ast.ImportFrom]
    disallow(not_allowed)

@test()
def noImportPow():
    """Checking for disallowed code."""
    not_allowed = [ast.Pow, ast.Import, ast.ImportFrom]
    disallow(not_allowed)

@test()
def noImport():
    """Checking for disallowed code."""
    not_allowed = [ast.Import, ast.ImportFrom]
    disallow(not_allowed)

def disallow(not_allowed):
    printable_na = [pp_ast(op) for op in not_allowed]
    issues = [op for op in not_allowed if (not isinstance(op, str) and op in static.AbstractSyntaxTree()) or op in collect_function_names()]
    printable_is = [pp_ast(op) for op in issues]
    assert len(printable_is) == 0, \
        "For this assignment you're not allowed to use any of these operations:\n" + \
        f"\033[91m{', '.join(printable_na)}\033[0m\n" + \
        f"You're using:\n\033[91m{', '.join(printable_is)}\033[0m"

def collect_function_names():
    source = static.getSource(fileName=None)
    function_names = []
    for node in static.getAstNodes(ast.AST, source):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                function_names.append(node.func.id)
    return function_names

def pp_ast(node_class):
    if isinstance(node_class, str):
        return node_class + '()'

    mapping = {
        "ImportFrom": "from ... import ...",
        "Sub": "-",
        "Add": "+",
        "Pow": "**"
    }
    return mapping.get(node_class.__name__, node_class.__name__.lower())
