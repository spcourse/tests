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
    import matplotlib.pyplot as plt
    plt.switch_backend("Agg")
    lib.neutralizeFunction(plt.pause)
    # lib.neutralizeFunction(matplotlib.use)

def after():
    import matplotlib.pyplot as plt
    plt.switch_backend("TkAgg")
    importlib.reload(plt)

@t.test(0)
def hasworp_met_twee_dobbelstenen(test):

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "worp_met_twee_dobbelstenen")
	test.description = lambda : "definieert de functie worp_met_twee_dobbelstenen"
	test.timeout = lambda : 60


@t.passed(hasworp_met_twee_dobbelstenen)
@t.test(10)
def correctDice(test):
	test.test = lambda : assertlib.between(lib.getFunction("worp_met_twee_dobbelstenen", _fileName)(), 2, 12)
	test.description = lambda : "returnt een correcte waarde voor een worp van twee dobbelstenen"
	test.timeout = lambda : 120


@t.passed(correctDice)
@t.test(20)
def hassimuleer_potjeAndsimuleer_groot_aantal_potjes_monopoly(test):

	def testMethod():
		test_potje = assertlib.fileContainsFunctionDefinitions(_fileName, "simuleer_potje_monopoly")
		test_groot_aantal_potjes = assertlib.fileContainsFunctionDefinitions(_fileName, "simuleer_groot_aantal_potjes_monopoly")
		info = ""
		if not test_potje:
			info = "de functie simuleer_potje_monopoly is nog niet gedefinieerd"
		elif not test_groot_aantal_potjes:
			info = "de functie simuleer_potje_monopoly is gedefinieerd :) \n  - de functie simuleer_groot_aantal_potjes_monopoly nog niet"
		return test_potje and test_groot_aantal_potjes, info



	test.test = lambda : testMethod()
	test.description = lambda : "definieert de functie simuleer_potje_monopoly en simuleer_groot_aantal_potjes_monopoly"
	test.timeout = lambda : 60


@t.passed(hassimuleer_potjeAndsimuleer_groot_aantal_potjes_monopoly)
@t.test(30)
def correctAverageTrump(test):

	def testMethod():
		nArguments = len(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName).arguments)

		# Trump
		if nArguments == 1:
			testInput = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(1000)
			test.success = lambda info : "De code werkt zonder startgeld, je kunt nu startgeld invoeren!"
			if assertlib.sameType(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(10000), None):
				test.fail = lambda info : "Zorg er voor dat de functie simuleer_groot_aantal_potjes_monopoly het gemiddeld aan benodigde worpen returnt en ook alleen deze waarde returnt"

		# Stargeld, 1 speler
		elif nArguments == 2:
			twoArguments = True
			testInput = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(1000, 1000000)
			if assertlib.sameType(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(10000, 1000000), None):
				test.fail = lambda info : "Zorg er voor dat de functie simuleer_groot_aantal_potjes_monopoly het gemiddeld aan benodigde worpen returnt en ook alleen deze waarde returnt"

		else:
			testInput = False
			test.fail = lambda info : "Zorg er voor dat de functie simuleer_groot_aantal_potjes_monopoly bij Trumpmode 1 argument heeft en bij starggeld 2 argumenten"

		return testInput

	test.test = lambda : assertlib.between(testMethod(), 145, 149)
	test.test = lambda : testMethod()
	test.description = lambda : "Monopoly werkt voor Trumpmode"
	test.timeout = lambda : 120


@t.passed(correctAverageTrump)
@t.test(40)
def correctAverageStartgeld(test):

	def testMethod():
		nArguments = len(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName).arguments)

		if nArguments == 2:
			testInput = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(10000, 1500)
			if assertlib.sameType(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(10000, 1500), None):
				test.fail = lambda info : "Zorg er voor dat de functie simuleer_groot_aantal_potjes_monopoly het gemiddeld aan benodigde worpen returnt en ook alleen deze waarde returnt"
			return testInput
		else:
			return 0

	test.test = lambda : assertlib.between(testMethod(), 184, 189)
	test.description = lambda : "Monopoly werkt met 1500 euro startgeld"
	test.timeout = lambda : 60
