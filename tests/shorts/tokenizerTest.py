from checkpy import *
from shared import noBreakAndImport
import ast
import typing

only("tokenizer.py")


fun = (declarative
    .function("tokenize")
    .returnType(list)
    .params("text")
)


test1 = test()(fun
    .call("The cat sat on the mat.")
    .returns(["The", "cat", "sat", "on", "the", "mat."])
)

test2 = test()(fun
    .call("hello")
    .returns(["hello"])
)

test3 = test()(fun
    .call("Hello, world! How are you?")
    .returns(["Hello,", "world!", "How", "are", "you?"])
)
