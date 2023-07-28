import ast
import typing

from checkpy import *

only("basejump.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()


def validate_sim(input_params, expected_time, xl, tl):
	start_height = input_params[0]
	end_height = input_params[1]

	assert len(xl) == len(tl), "function is expected to return two lists of the same length"

	x_start, x_end = xl[0], xl[-1]
	t_start, t_end = tl[0], tl[-1]

	if t_end == approx(expected_time, abs=0.2):
		return

	assert x_start != approx(start_height, abs=0.1),\
		"It looks like the simulation did not start at a height of 1000 meters."
	
	assert x_end != approx(end_height, abs=1),\
		"It looks like the simulation did not stop at a height of 200 meters."
	
	assert t_start != approx(0, abs=0.1),\
		"It looks like the starting time of the simulation is not 0."

	raise AssertionError(f"Did not expect a total elapsed time of {tl[-1]} (with input {input_params})")


def restrict(state: builder.FunctionState):
	assert ast.Break not in static.AbstractSyntaxTree()

testDef = (builder
	.function("simulate_free_fall")
	.do(restrict)
	.params("x_start", "x_end", "m", "xi", "dt")
	.build()
)

testBasejumpNew1 = passed(testDef, hide=False)(builder
	.function("simulate_free_fall")
	.timeout(90)
	.returnType(typing.Tuple[typing.List[float], typing.List[float]])
	.call(1000.0, 200.0, 72.0, 0, 0.01)
	.do(lambda state: validate_sim(state.args, 12.77, state.returned[0], state.returned[1]))
	.description("Test simulation without air resistance.")
	.build()
)

testBasejumpNew2 = passed(testDef, hide=False)(builder
	.function("simulate_free_fall")
	.timeout(90)
	.returnType(typing.Tuple[typing.List[float], typing.List[float]])
	.call(1000.0, 200.0, 72.0, 0.24, 0.01)
	.do(lambda state: validate_sim(state.args, 18.58, state.returned[0], state.returned[1]))
	.description("Test simulation with air resistance.")
	.build()
)

testBasejumpNew3 = passed(testDef, hide=False)(builder
	.function("simulate_free_fall")
	.timeout(90)
	.returnType(typing.Tuple[typing.List[float], typing.List[float]])
	.call(1200, 300, 78, 0.24, 0.01)
	.do(lambda state: validate_sim(state.args, 19.93, state.returned[0], state.returned[1]))
	.build()
)

@test()
def showsGraph():
	"""Either saves a graph into a file, or shows a graph on the screen."""
	assert "savefig" in static.getFunctionCalls() or "show" in static.getFunctionCalls()
