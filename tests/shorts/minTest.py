from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("min.py")


fun = (declarative
    .function("min")
    .returnType(float)
    .params("a", "b")
)

test1 = test()(fun
    .call(10, 5)
    .returns(5)
)

test2 = test()(fun
    .call(8, 16)
    .returns(8)
)
