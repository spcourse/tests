from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("max.py")


fun = (declarative
    .function("max")
    .returnType(int)
    .params("lst")
)

test1 = test()(fun
    .call([1, 6, 19, 2, -8])
    .returns(19)
)

test2 = test()(fun
    .call([1, 6, -19, 2, -8])
    .returns(6)
)

test3 = test()(fun
    .call([-9000000000000])
    .returns(-9000000000000)
)
