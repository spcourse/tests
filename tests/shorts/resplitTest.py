from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("resplit.py")


fun = (declarative
    .function("resplit")
    .returnType(list)
    .params("text")
)


test1 = test()(fun
    .call("a,b.c.d")
    .returns(["a", "b", "c", "d"])
)

alice = "If I had a world of my own, everything would be nonsense. Nothing " +\
    "would be what it is because everything would be what it isn’t. And " +\
    "contrariwise, what it is, it wouldn’t be, and what it wouldn’t be, it would."

splitted = ['If I had a world of my own', 'everything would be nonsense', 'Nothing would be what it is because everything would be what it isn’t', 'And contrariwise', 'what it is', 'it wouldn’t be', 'and what it wouldn’t be', 'it would']

test2 = test()(fun
    .call(alice)
    .returns(splitted)
)
