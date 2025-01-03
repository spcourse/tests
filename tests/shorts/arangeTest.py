from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("arange.py")


fun = (declarative
    .function("arange")
    .returnType(list)
    .params("a", "b", "step_size")
)

test1 = test()(fun
    .call(0,10,1)
    .returns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
)

test2 = test()(fun
    .call(-1,1,0.25)
    .returns([-1, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75])
)
