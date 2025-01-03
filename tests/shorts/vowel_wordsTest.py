from checkpy import *
from shared import noBreakAndImport, ApproxString
import ast
import typing


only("vowel_words.py")

fun = (declarative
    .function("vowel_words")
    .returnType(str)
    .params("text")
)

test1 = test()(fun
    .call("Sometimes I have believed as many as six impossible things before breakfast.")
    .returns(ApproxString("I as as impossible"))
)
