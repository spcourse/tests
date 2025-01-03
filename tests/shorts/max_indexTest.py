from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("max_index.py")


fun = (declarative
    .function("max_index")
    .returnType(int)
    .params("lst")
)

test1 = test()(fun
    .call([1, 6, 19, 2, -8])
    .returns(2)
)

test2 = test()(fun
    .call([1, 6, -19, 2, -8])
    .returns(1)
)

test3 = test()(fun
    .call([-9000000000000])
    .returns(0)
)
