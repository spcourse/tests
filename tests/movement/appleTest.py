from typing import Tuple
import pathlib
import sys

from checkpy import *

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from notAllowedCode import *
import helpers


only("apple.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()


testDef1 = helpers.assertDefFactory(
	function="simulate_apple1",
	parameters=["x", "dt"],
	before=lambda: notAllowedCode({"break": "break"})
)


def apple1Hint(output):
	t, v = output
	if v == approx(4.52, abs=0.1) or t == approx(159.47, abs=1):
		assert False, "Did you mix up the order of the return values?"

	if v == approx(44.3, abs=0.3):
		assert False, "Did you forget to convert to km/h?"

testApple1 = passed(testDef1, timeout=90, hide=False)(
	helpers.assertFuncFactory(
		function="simulate_apple1",
		input=(100, 0.01),
		output=(approx(159.47, abs=0.1), approx(4.52, abs=0.1)),
		outputType=Tuple[float, float],
		hint=apple1Hint
	)
)


testDef2 = helpers.assertDefFactory(
	function="simulate_apple2",
	parameters=["dt"],
	before=lambda: notAllowedCode({"break": "break"})
)


testApple2 = passed(testDef2, timeout=90, hide=False)(
	helpers.assertFuncFactory(
		function="simulate_apple2",
		input=(0.01,),
		output=approx(2.84, abs=0.02),
		outputType=float
	)
)

## pytest v2 style
# @test()
# def testDef1():
# 	"""Defines the function `simulate_apple1()`"""
# 	notAllowedCode({"break": "break"})

# 	assert "simulate_apple1" in static.getFunctionDefinitions()

# 	simulate_apple1 = getFunction("simulate_apple1")

# 	assert simulate_apple1.parameters == ["x", "dt"],\
# 		"make sure the function has the correct parameters"


# @passed(testDef1, timeout=90, hide=False)
# def testApple1():
# 	"""Testing simulate_apple1()"""
# 	x, dt = 100, 0.01
# 	simulate_apple1 = getFunction("simulate_apple1")
# 	output = simulate_apple1(x, dt)

# 	assert output == Type(Tuple[float, float]),\
# 		"make sure the function returns the correct type"

# 	t, v = output

# 	if v == approx(4.52, abs=0.1) or t == approx(159.47, abs=1):
# 		assert False, "Did you mix up the order of the return values?"

# 	if v == approx(44.3, abs=0.3):
# 		assert False, "Did you forget to convert to km/h?"

# 	assert t == approx(4.52, abs=0.1) and v == approx(159.47, abs=0.1),\
# 		f"Did not expect output {t}, {v} (with input {x}, {dt})"
