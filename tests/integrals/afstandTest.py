import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

def before():
	try:
		import matplotlib
		matplotlib.use("Agg")
		import matplotlib.pyplot as plt
		plt.switch_backend("Agg")
		lib.neutralizeFunction(plt.pause)
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
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "vierkant")
	test.description = lambda : "definieert de functie vierkant()"

@t.passed(hasVierkant)
@t.test(11)
def correctVierkant(test):
	test.test = lambda : assertlib.between(lib.getFunction("vierkant", _fileName)(10000), 0.51, 0.54)
	test.description = lambda : "vierkant geeft de goede afstand terug"
