import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
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


@t.test(10)
def hasVierkant(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "square")
	test.description = lambda : "defines the function square()"

@t.passed(hasVierkant)
@t.test(11)
def correctVierkant(test):
	test.test = lambda : assertlib.between(lib.getFunction("square", _fileName)(10000), 0.51, 0.54)
	test.description = lambda : "square() yields the correct distance"
