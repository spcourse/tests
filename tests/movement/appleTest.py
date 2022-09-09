import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *
from helpers import apply_function, InvalidFunctionApplication, similar, has_function

def before():
	try:
		import matplotlib
		import warnings
		warnings.filterwarnings("ignore")
		matplotlib.use("Agg")
		import matplotlib.pyplot as plt
		plt.switch_backend("Agg")
		lib.neutralizeFunction(plt.pause)
		lib.neutralizeFunction(plt.show)
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
def containsRequiredFunction1Definition(test):
	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)
	has_function(test, _fileName, "simulate_apple1", ['x', 'dt'])

@t.passed(containsRequiredFunction1Definition)
@t.test(1)
def testApple1(test):
	def testMethod():
		try:
			_input = 100, 0.01
			_fn = lib.getFunction("simulate_apple1", _fileName)
			_t, _v = apply_function(_fn, _input, (float, float))
		except InvalidFunctionApplication as e:
			return False, e.message
		except Exception as e:
			return False, f"An error occured while running the function: \n {type(e).__name__}: {str(e)}"

		if similar(_v, 4.52, atol = 0.1) or similar(_t, 159.47, atol = 1):
			return False, "Did you mix up the order of the return values?"
		if similar(_v, 44.3, atol = 0.3):
			return False, "Did you forget to convert to km/h?"
		if similar(_t, 4.52, atol = 0.1) and similar(_v, 159.47, atol = 1):
			return True, ""
		return False, f"Did not expect output {_t, _v} (with input {_input})"

	test.test = testMethod
	test.description = lambda : "Testing simulate_apple1()"
	test.timeout = lambda : 90

@t.test(2)
def containsRequiredFunction2Definition(test):
	has_function(test, _fileName, "simulate_apple2", ['dt'])

@t.passed(containsRequiredFunction2Definition)
@t.test(3)
def testApple2(test):
	def testMethod2():
		_fn = lib.getFunction("simulate_apple2", _fileName)
		try:
			_t = apply_function(_fn, (0.01,), (float,))
		except InvalidFunctionApplication as e:
			return False, e.message
		if assertlib.between(_t, 2.82, 2.86):
			return True, ""
		return False, f"Did not expect output {_t} (with input: 0.01)"

	test.test = testMethod2
	test.description = lambda : "Testing simulate_apple2()"
	test.timeout = lambda : 90
