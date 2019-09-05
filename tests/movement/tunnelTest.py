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

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "tunnel")
	test.description = lambda : "definieert de functie `tunnel()`"

@t.test(1)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig")
	test.description = lambda : "slaat een grafiek op"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(10)
def correctMaxSpeed(test):
	test.test = lambda : assertlib.numberOnLine(28474.32, lib.getLine(lib.outputOf(_fileName), 0), deviation = 500)
	test.description = lambda : "print de maximale snelheid van de appel"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(11)
def correctTimeTillReturn(test):
	test.test = lambda : assertlib.numberOnLine(5061, lib.getLine(lib.outputOf(_fileName), 1), deviation = 50)
	test.description = lambda : "print het tijdstip van terugkeer na loslaten"
