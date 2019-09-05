import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import math
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
def hasSomRandomGetallen(test):
    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "SomRandomGetallen")
    test.description = lambda : "definieert de functie SomRandomGetallen"

@t.passed(hasSomRandomGetallen)
@t.test(10)
def correctBelow40(test):
    tsts = ['40', 'veertig', 'forty']
    test.test = lambda : (assertlib.numberOnLine(5, lib.getLine(lib.outputOf(_fileName), 0), deviation = 5) or assertlib.numberOnLine(0.05, lib.getLine(lib.outputOf(_fileName), 0), deviation = 0.05)) and sum([assertlib.contains(lib.outputOf(_fileName), tst) for tst in tsts])
    test.fail = lambda info : "zorg dat je de waarde in een volledige zin zet, op de eerste regel"
    test.description = lambda : "print op de eerste regel hoe vaak de som minder dan 40 is"

@t.passed(hasSomRandomGetallen)
@t.test(20)
def correctAbove60(test):
	tsts = ['60', 'zestig', 'sixty']
	test.test = lambda : (assertlib.numberOnLine(5, lib.getLine(lib.outputOf(_fileName), 1), deviation = 5) or assertlib.numberOnLine(0.05, lib.getLine(lib.outputOf(_fileName), 1), deviation = 0.05))and sum([assertlib.contains(lib.outputOf(_fileName), tst) for tst in tsts])
	test.fail = lambda info : "zorg dat je de waarde in een volledige zin zet, op de tweede regel"
	test.description = lambda : "print op de tweede regel hoe vaak de som meer dan 60 is"
