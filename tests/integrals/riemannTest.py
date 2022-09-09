import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

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
def hasRiemann(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "riemann")
	test.description = lambda : "defines the function riemann()"

@t.passed(hasRiemann)
@t.test(1)
def correctFunc1(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(1, 1, 1, 0, 2, 1000), 6.66, 6.67)
	test.description = lambda : "riemann() yields the correct value for x^2 + x + 1"

@t.passed(hasRiemann)
@t.test(2)
def correctFunc2(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(1, 0, 0, -2, -1, 1000), 2.33, 2.34)
	test.description = lambda : "riemann() yields the correct value when an interval does not start at x=0"

@t.passed(hasRiemann)
@t.test(3)
def correctFunc3(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(1, 0, -2, -1, 1, 1000), -3.34, -3.33)
	test.description = lambda : "riemann() yields the correct value when a function goes below the x-axis"

@t.passed(hasRiemann)
@t.test(4)
def correctFunc4(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(-1, 4, 15, -2, 3, 10), 73, 74)
	test.description = lambda : "riemann() yields the correct value of an integral on [-2, 3], with n = 10, for the function -x^2 + 4x + 15"
