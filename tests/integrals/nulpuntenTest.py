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


@t.test(0)
def hasNulpunten(test):
    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "nulpunten")
    test.description = lambda : "definieert de functie nulpunten()"

@t.passed(hasNulpunten)
@t.test(10)
def returnTypeIsList(test):
    test.test = lambda : assertlib.sameType(lib.getFunction("nulpunten", _fileName)(1,2,-10), [])
    test.description = lambda : "nulpunten geeft een lijst terug"

@t.passed(hasNulpunten)
@t.test(20)
def correct(test):
	test.test = lambda : assertlib.exact(sorted(int(p * 10) for p in lib.getFunction("nulpunten", _fileName)(1,2,-10)), [-43, 23])
	test.description = lambda : "vindt de nulpunten voor invoer a=1, b=2, c=-10"

@t.passed(hasNulpunten)
@t.test(30)
def correctNone(test):
    test.test = lambda : assertlib.exact(sorted(int(p * 10) for p in lib.getFunction("nulpunten", _fileName)(3,6,9)), [])
    test.description = lambda : "vindt geen nulpunten voor invoer a=3, b=6, c=9"
