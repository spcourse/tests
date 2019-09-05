import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

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
def containsRequiredFunctionDefinitions(test):

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "fit")
	test.description = lambda : "definieert de functie `fit()`"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(10)
def correctC(test):
	test.test = lambda : assertlib.numberOnLine(60.3, lib.getLine(lib.outputOf(_fileName), 0), deviation = 1)
	test.description = lambda : "print de beste waarde van c"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(11)
def correctUncertainy(test):
	test.test = lambda : assertlib.numberOnLine(1.5, lib.getLine(lib.outputOf(_fileName), 1), deviation = 0.1)
	test.description = lambda : "print de onzekerheid bij c"
