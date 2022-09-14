import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import math
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
def hasSomRandomGetallen(test):
    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "sum_random_numbers")
    test.description = lambda : "defines the function sum_random_numbers()"

@t.passed(hasSomRandomGetallen)
@t.test(10)
def correctBelow40(test):
    tsts = ['40', 'veertig', 'forty']
    test.test = lambda : (assertlib.numberOnLine(5, lib.getLine(lib.outputOf(_fileName), 0), deviation = 5) or assertlib.numberOnLine(0.05, lib.getLine(lib.outputOf(_fileName), 0), deviation = 0.05)) and sum([assertlib.contains(lib.outputOf(_fileName), tst) for tst in tsts])
    test.fail = lambda info : "make sure you output a sentence containing the answer on the first line of output"
    test.description = lambda : "prints, on the first line, how often the sum is less than 40"

@t.passed(hasSomRandomGetallen)
@t.test(20)
def correctAbove60(test):
	tsts = ['60', 'zestig', 'sixty']
	test.test = lambda : (assertlib.numberOnLine(5, lib.getLine(lib.outputOf(_fileName), 1), deviation = 5) or assertlib.numberOnLine(0.05, lib.getLine(lib.outputOf(_fileName), 1), deviation = 0.05))and sum([assertlib.contains(lib.outputOf(_fileName), tst) for tst in tsts])
	test.fail = lambda info : "make sure you output a sentence containing the answer on the second line of output"
	test.description = lambda : "prints, on the first line, how often the sum is more than 60"
