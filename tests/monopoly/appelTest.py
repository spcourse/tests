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

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "appel")
	test.description = lambda : "definieert de functie `appel()`"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(1)
def correctTime(test):
	test.test = lambda : assertlib.numberOnLine(4.51, lib.getLine(lib.outputOf(_fileName), 0), deviation = 0.01)
	test.description = lambda : "print het tijdstip waarop de appel de grond raakt"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(2)
def correctSpeed(test):
	test.test = lambda : assertlib.numberOnLine(159.5, lib.getLine(lib.outputOf(_fileName), 1), deviation = 0.1)
	test.description = lambda : "print de snelheid waarmee de appel de grond raakt"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(3)
def correctSecondsToHit100(test):
	test.test = lambda : assertlib.numberOnLine(2.83, lib.getLine(lib.outputOf(_fileName), 2), deviation = 0.01)
	test.description = lambda : "print het tijdstip waarop een snelheid van 100km/u wordt bereikt"
