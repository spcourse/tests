from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("snake_case.py")


fun = (declarative
    .function("snake_case")
    .returnType(str)
    .params("text")
)


test1 = test()(fun
    .call("snakeCase")
    .returns("snake_case")
)

test2 = test()(fun
    .call("textProcessingVariable")
    .returns("text_processing_variable")
)
