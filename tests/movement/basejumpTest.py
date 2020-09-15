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
def containsRequiredFunctionDefinitions(test):

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "basejump")
	test.description = lambda : "defines the function `basejump()`"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(10)
def correctTimeTillParachute(test):
	test.test = lambda : assertlib.numberOnLine(12.18, lib.getLine(lib.outputOf(_fileName), 0), deviation = 0.1)
	test.description = lambda : "prints the number of seconds elapsed until the parachute opens"

@t.passed(containsRequiredFunctionDefinitions)
@t.test(11)
def correctExtraTime(test):
	test.test = lambda : assertlib.numberOnLine(5.06, lib.getLine(lib.outputOf(_fileName), 1), deviation = 0.1)
	test.description = lambda : "prints the number of seconds added to that because of air resistance"
