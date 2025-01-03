from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("squared.py")


fun = (declarative
    .function("squared")
    .returnType(float)
    .params("x")
)

test1 = test()(fun
    .call(2)
    .returns(4)
)

test2 = test()(fun
    .call(-5.0)
    .returns(25.0)
)
