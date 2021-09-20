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
def hasNulpunten(test):
    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "roots")
    test.description = lambda : "defines the function roots()"

@t.passed(hasNulpunten)
@t.test(10)
def returnTypeIsList(test):
    test.test = lambda : assertlib.sameType(lib.getFunction("roots", _fileName)(1,2,-10), [])
    test.description = lambda : "roots() returns a list"

@t.passed(hasNulpunten)
@t.test(20)
def correct(test):
	test.test = lambda : assertlib.exact(sorted(int(p * 10) for p in lib.getFunction("roots", _fileName)(1,2,-10)), [-43, 23])
	test.description = lambda : "roots() yields the two correct roots for a=1, b=2, c=-10"

@t.passed(hasNulpunten)
@t.test(30)
def correctNone(test):
    test.test = lambda : assertlib.exact(sorted(int(p * 10) for p in lib.getFunction("roots", _fileName)(3,6,9)), [])
    test.description = lambda : "roots() yields no roots for a=3, b=6, c=9"
