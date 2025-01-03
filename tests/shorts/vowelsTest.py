from checkpy import *
from shared import noBreakAndImport, ApproxString
import ast
import typing


only("vowels.py")

fun = (declarative
    .function("vowels")
    .returnType(str)
    .params("text")
)

test1 = test()(fun
    .call("Hello, world!")
    .returns("eoo")
)
