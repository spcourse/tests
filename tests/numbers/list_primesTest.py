from checkpy import *
from shared import noBreakAndImport

import ast

only("list_primes.py")

is_prime = declarative.function("is_prime").returnType(bool).params("x")

list_primes = declarative.function("list_primes").returnType(list).params("n")

test_prime1 = test()(is_prime.call(7).returns(True))

test_prime2 = test()(is_prime.call(9).returns(False))

test_prime3 = test()(is_prime.call(2).returns(True))

test_prime4 = test()(is_prime.call(1).returns(False))

test_prime5 = test()(is_prime.call(97).returns(True))

test_list1 = test()(list_primes.call(10).returns([2, 3, 5, 7]))

test_list2 = test()(list_primes.call(11).returns([2, 3, 5, 7]))

test_list3 = test()(list_primes.call(2).returns([]))

test_list4 = test()(list_primes.call(100).returns(
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
     53, 59, 61, 67, 71, 73, 79, 83, 89, 97]))


@test()
def listPrimesCallsIsPrime():
    """list_primes uses is_prime"""
    tree = ast.parse(static.getSource())
    functions = [node for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef) and node.name == "list_primes"]
    assert functions, "define a function list_primes(n)"
    calls = [node for node in ast.walk(functions[0])
             if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Name) and node.func.id == "is_prime"]
    assert calls, "list_primes should call is_prime to check each number"
