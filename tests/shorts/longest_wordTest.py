from checkpy import *
from shared import noBreakAndImport
import ast
import typing


only("longest_word.py")

fun = (declarative
    .function("longest_word")
    .returnType(str)
    .params("text")
)

alice = "seen a rabbit with either a waistcoat-pocket, or a watch"

test1 = test()(fun
    .call(alice)
    .returns("waistcoat-pocket,")
)
