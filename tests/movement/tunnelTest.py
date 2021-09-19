import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *
from helpers import apply_function, InvalidFunctionApplication, similar

def before():
	try:
		import matplotlib
		matplotlib.use("Agg")
		import matplotlib.pyplot as plt
		plt.switch_backend("Agg")
		lib.neutralizeFunction(plt.pause)
	except ImportError:
		pass

	try:
		import numpy
		numpy.seterr('raise')
	except ImportError:
		pass


def after():
	try:
		import matplotlib.pyplot as plt
		plt.switch_backend("TkAgg")
		importlib.reload(plt)
	except ImportError:
		pass


@t.test(0)
def containsRequiredFunctionDefinitions(test):

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "simulate_ultimate_free_fall")
	test.description = lambda : "Defines the function `simulate_ultimate_free_fall()`"


def validate_sim1(input_params, expected, rl, vl):
	min_height, max_height, min_speed, max_speed = expected
	_min_height, _max_height, _min_speed, _max_speed = min(rl), max(rl), min(vl), max(vl)

	tol = max_height // 1000
	if not similar(min_height, _min_height, tol):
		return False, f"Incorrect minimum distance (got {_min_height}, expected approximately {min_height})"
	if not similar(max_height, _max_height, tol):
		return False, f"Incorrect maximum distance (got {_max_height}, expected approximately {max_height})"
	if not similar(min_speed, _min_speed, 2):
		return False, f"Incorrect minimum speed (got {_min_speed}, expected approximately {min_speed})"
	if not similar(max_speed, _max_speed, 2):
		return False, f"Incorrect maximum speed (got {_max_speed}, expected approximately {max_speed})"
	return True, f""


@t.passed(containsRequiredFunctionDefinitions)
@t.test(1)
def testTunnel1(test):
	def testMethod():
		try:
			_input = 6.38e6, 0.01
			_fn = lib.getFunction("simulate_ultimate_free_fall", _fileName)
			_rl, _vl, _tl = apply_function(_fn, _input, (list, list, list))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if len(_rl) != len(_tl) or len(_vl) != len(_tl):
			return False, "Function is expected to return three lists of the same length."


		return validate_sim1(_input, (-6380124.4,  6380249, -7925, 7925.2), _rl, _vl)


	test.test = testMethod
	test.description = lambda : "Correct speeds and distances starting at height 6.38e6."
	test.timeout = lambda : 90


@t.passed(containsRequiredFunctionDefinitions)
@t.test(2)
def testTunnel2(test):
	def testMethod():
		try:
			_input = 6.38e6, 0.01
			_fn = lib.getFunction("simulate_ultimate_free_fall", _fileName)
			_rl, _vl, _tl = apply_function(_fn, _input, (list, list, list))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if len(_rl) != len(_tl) or len(_vl) != len(_tl):
			return False, "Function is expected to return three lists of the same length."

		if not similar(_tl[-1], 5058.3, 4):
			return False, f"Did not expected the time of the simulated free fall to be {_tl[-1]} seconds."


		return True, ""


	test.test = testMethod
	test.description = lambda : "Correct simulation length."
	test.timeout = lambda : 90

@t.passed(containsRequiredFunctionDefinitions)
@t.test(3)
def testTunnel3(test):
	def testMethod():
		try:
			_input = 3474, 0.01
			_fn = lib.getFunction("simulate_ultimate_free_fall", _fileName)
			_rl, _vl, _tl = apply_function(_fn, _input, (list, list, list))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if len(_rl) != len(_tl) or len(_vl) != len(_tl):
			return False, "Function is expected to return three lists of the same length."

		return validate_sim1(_input, (-3474, 3474, -4.315, 4.315), _rl, _vl)


	test.test = testMethod
	test.description = lambda : "Correct speeds and distances starting at height 3474"
	test.timeout = lambda : 90

@t.test(5)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig") or assertlib.fileContainsFunctionCalls(_fileName, "show")
	test.description = lambda : "Either saves a graph into a file, or shows a graph on the screen."
