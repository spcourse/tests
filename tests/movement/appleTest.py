from typing import Tuple
import ast

from checkpy import *

only("apple.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

def restrict(state: declarative.FunctionState):
    assert ast.Break not in static.AbstractSyntaxTree(state.fileName)

def apple1Hint(state: declarative.FunctionState):
    t, v = state.returned
    if t == approx(159.47, abs=1) or v == approx(4.52, abs=0.1):
        raise AssertionError("Did you mix up the order of the return values?")

    if v == approx(44.3, abs=0.3):
        raise AssertionError("Did you forget to convert to km/h?")

simulate_apple1 = (
    declarative.function("simulate_apple1")
    .do(restrict)
    .params("x", "dt")
    .returnType(Tuple[float, float])
)

testAppleDef1 = test()(simulate_apple1)

testApple1 = passed(testAppleDef1, hide=False)(
    simulate_apple1
    .call(100, 0.01)
    .do(apple1Hint)
    .returns((approx(4.52, abs=0.1), approx(159.47, abs=0.1)))
)


simulate_apple2 = (
    declarative.function("simulate_apple2")
    .do(restrict)
    .params("dt")
    .returnType(float)
)

testAppleDef2 = test()(simulate_apple2)

testApple2 = passed(testAppleDef2, hide=False)(
    simulate_apple2
    .call(0.01)
    .returns(approx(2.84, abs=0.02))
)
