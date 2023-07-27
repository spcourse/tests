from typing import Tuple
import ast

from checkpy import *

only("apple.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

def restrict(state: builder.FunctionState):
	assert ast.Break not in static.AbstractSyntaxTree(state.fileName)

def apple1Hint(state: builder.FunctionState):
	t, v = state.returned
	if v == approx(159.47, abs=1) or t == approx(4.52, abs=0.1):
		raise AssertionError("Did you mix up the order of the return values?")

	if v == approx(44.3, abs=0.3):
		raise AssertionError("Did you forget to convert to km/h?")

apple1Builder = (builder
	.function("simulate_apple1")
	.do(restrict)
	.params("x", "dt")
    .returnType(Tuple[float, float])
)

testAppleDef1 = apple1Builder.build()

testApple1 = passed(testAppleDef1, hide=False)(apple1Builder
	.call(100, 0.01)
	.do(apple1Hint)
	.returns((approx(159.47, abs=0.1), approx(4.52, abs=0.1)))
	.build()
)


apple2Builder = (builder
	.function("simulate_apple2")
	.do(restrict)
	.params("x")
	.returnType(float)
)

testAppleDef2 = apple2Builder.build()

testApple2 = passed(testAppleDef2, hide=False)(apple2Builder
	.call(0.01)
	.returns(approx(2.84, abs=0.02))
	.build()
)
