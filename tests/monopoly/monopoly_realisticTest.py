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
		lib.neutralizeFunction(plt.show)
	except ImportError:
		pass

	try:
		import numpy
		numpy.seterr('raise')
	except ImportError:
		pass

def after():
	import matplotlib.pyplot as plt
	plt.switch_backend("TkAgg")
	importlib.reload(plt)

@t.test(0)
def hassimulate_monopoly_games(test):

	def testMethod():
		correctFunction = False

		if assertlib.fileContainsFunctionDefinitions(_fileName, "simulate_monopoly_games"):
			nArguments = len(lib.getFunction("simulate_monopoly_games", _fileName).arguments)

			if nArguments == 3:
				correctFunction = True
		return correctFunction

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = testMethod
	test.fail = lambda info : "make sure that the simulate_monopoly_games function has three arguments, the number of games, the starting_money for player 1, and the starting_money for player 2"
	test.description = lambda : "defines functie simulate_monopoly_games with the proper number of arguments"
	test.timeout = lambda : 90


@t.passed(hassimulate_monopoly_games)
@t.test(10)
def correctAverageDiff(test):
	def testMethod():
		outcome = lib.getFunction("simulate_monopoly_games", _fileName)(10000, 1500, 1500)
		if assertlib.sameType(outcome, None):
			info = "Make sure that the function simulate_monopoly_games only returns the difference in the number of streets owned"
		elif assertlib.between(outcome, -99999999, 0):
			info = "Are you sure you are subtracting player 2s values from player 1 and not the other way around?"
		else:
			info = "The difference in street ownership is not that big, it should be less than 1 street on average."
		return assertlib.between(outcome, .35, .55), info

	test.test = testMethod
	test.description = lambda : "Monopoly with two players gives the correct average difference in owned streets"
	test.timeout = lambda : 90



@t.passed(correctAverageDiff)
@t.test(20)
def correctAverageDiff2(test):
	def testMethod():
		def findline(outputOf):
			tsts = ['starting', 'money', 'equal', 'number', 'streets']
			for line in outputOf.split("\n"):
				if all([assertlib.contains(line, tst) for tst in tsts]):
					return line
			return ""

		line = findline(lib.outputOf(_fileName))

		info = ""
		if not line:
			info = "Check the assignment for the proper output format of the solution."
		elif not any([assertlib.numberOnLine(number, line) for number in [0, 50, 100, 150, 200]]):
			info = "The found value was not rounded to the nearest value of 50 euros."
		else:
			info = "Properly rounded to the nearest value, but the value returned was incorrect."
		return assertlib.numberOnLine(150, line), info

	test.test = testMethod
	test.description = lambda : "Monopoly with two players finds the correct amount of extra starting money for player 2"
	test.timeout = lambda : 90
