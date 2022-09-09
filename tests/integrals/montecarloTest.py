import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import math
import importlib

def before():
	try:
		import matplotlib
		import warnings
		warnings.filterwarnings("ignore", module = "plot")
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
def hasMontecarlo(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "montecarlo")
	test.description = lambda : "defines the function montecarlo()"

@t.passed(hasMontecarlo)
@t.test(1)
def correctFunc1(test):
	test.test = lambda : assertlib.between(lib.getFunction("montecarlo", _fileName)(lambda x : x**(x + 0.5), 0, 0, 1, 1), 0.51, 0.54)
	test.description = lambda : "montecarlo() yields the correct value of an integral on [0,1] for the square function"

@t.passed(hasMontecarlo)
@t.test(2)
def correctFunc2(test):
	test.test = lambda : assertlib.between(lib.getFunction("montecarlo", _fileName)(lambda x : math.tan(math.cos(math.sin(x))), 0.2, 0, 2.2, 1.5), 1.69, 1.73)
	test.description = lambda : "montecarlo() yields the correct value when an interval does not start at x=0"

@t.passed(hasMontecarlo)
@t.test(3)
def correctFunc3(test):
	test.test = lambda : assertlib.between(lib.getFunction("montecarlo", _fileName)(lambda x : math.sin(x**2), 0, -1, math.pi, 1), 0.75, 0.79)
	test.description = lambda : "montecarlo() yields the correct value when a function goes below the x-axis"
