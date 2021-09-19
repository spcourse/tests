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

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "simulate_free_fall")
	test.description = lambda : "Defines the function `simulate_free_fall()`"



def validate_sim(input_params, expected_time, xl, tl):
	start_height = input_params[0]
	end_height = input_params[1]
	_x_start, _x_end = xl[0], xl[-1]
	_t_start, _t_end = tl[0], tl[-1]

	if not all([type(v) == float or type(v) == int for v in [_x_start, _x_end, _t_start, _t_end]]):
		return False, "Both lists should only contain floats."

	if similar(_t_end, expected_time, 0.2):
		return True, ""

	if not similar(_x_start, start_height, 0.1):
		return False, "It looks like the simulation did not start at a height of 1000 meters."
	if not similar(_x_end, end_height, 1):
		return False, "It looks like the simulation did not stop at a height of 200 meters."
	if not similar(_t_start, 0, 0.1):
		return False, "It looks like the starting time of the simulation is not 0."

	return False, f"Did not expect a total elapsed time of {tl[-1]} (with input {input_params})"


@t.passed(containsRequiredFunctionDefinitions)
@t.test(1)
def testBasejump1(test):
	def testMethod():
		try:
			_input = 1000.0, 200.0, 72.0, 0, 0.01
			_fn = lib.getFunction("simulate_free_fall", _fileName)
			_xl, _tl = apply_function(_fn, _input, (list, list))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if len(_xl) != len(_tl):
			return False, "Function is expected to return two lists of the same length."

		return validate_sim(_input, 12.77, _xl, _tl)


	test.test = testMethod
	test.description = lambda : "Test simulation without air resistance. Starting at 1000m and ending at 200m."
	test.timeout = lambda : 90

@t.passed(containsRequiredFunctionDefinitions)
@t.test(2)
def testBasejump2(test):
	def testMethod():
		try:
			_input = 1000.0, 200.0, 72.0, 0.24, 0.01
			_fn = lib.getFunction("simulate_free_fall", _fileName)
			_xl, _tl = apply_function(_fn, _input, (list, list))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if len(_xl) != len(_tl):
			return False, "Function is expected to return two lists of the same length."

		return validate_sim(_input, 18.58, _xl, _tl)


	test.test = testMethod
	test.description = lambda : "Test simulation with air resistance. Starting at 1000m and ending at 200m."
	test.timeout = lambda : 90

@t.passed(containsRequiredFunctionDefinitions)
@t.test(3)
def testBasejump3(test):
	def testMethod():
		try:
			_input = 1200, 300, 78, 0.24, 0.01
			_fn = lib.getFunction("simulate_free_fall", _fileName)
			_xl, _tl = apply_function(_fn, _input, (list, list))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if len(_xl) != len(_tl):
			return False, "Function is expected to return two lists of the same length."

		return validate_sim(_input, 19.93, _xl, _tl)


	test.test = testMethod
	test.description = lambda : f"Test simulation with paramaters 1200, 300, 78, 0.24, 0.01."
	test.timeout = lambda : 90

@t.test(4)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig") or assertlib.fileContainsFunctionCalls(_fileName, "show")
	test.description = lambda : "Either saves a graph into a file, or shows a graph on the screen."
