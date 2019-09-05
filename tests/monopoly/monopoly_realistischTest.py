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
    lib.neutralizeFunction(plt.show)

def after():
    import matplotlib.pyplot as plt
    plt.switch_backend("TkAgg")
    importlib.reload(plt)

@t.test(0)
def hassimuleer_groot_aantal_potjes_Monopoly(test):

	def testMethod():
		correctFunction = False

		if assertlib.fileContainsFunctionDefinitions(_fileName, "simuleer_groot_aantal_potjes_monopoly"):
			nArguments = len(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName).arguments)

			if nArguments == 3:
				correctFunction = True
		return correctFunction

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = testMethod
	test.fail = lambda info : "zorg dat de functie drie argumenten heeft, het aantal potjes, startgeld voor speler 1 en startgeld voor speler 2"
	test.description = lambda : "definieert de functie simuleer_potje_monopoly en simuleer_groot_aanal_potjes_monopoly met drie argumenten"
	test.timeout = lambda : 90


@t.passed(hassimuleer_groot_aantal_potjes_Monopoly)
@t.test(10)
def correctAverageDiv(test):
	def testMethod():
		outcome = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(10000, 1500, 1500)
		if assertlib.sameType(outcome, None):
			info = "Zorg er voor dat de functie simuleer_groot_aantal_potjes_monopoly het verschil in het bezit van straten returnt en alleen deze waarde returnt"
		elif assertlib.between(outcome, -99999999, 0):
			info = "Als speler 1 meer straten heeft dan speler 2 is het verschil positief"
		else:
			info = "Het verschil is niet erg groot, gemiddeld zelfs minder dan 1 straat"
		return assertlib.between(outcome, .15, .45), info

	test.test = testMethod
	test.description = lambda : "Monopoly met twee spelers geeft de het correcte gemiddelde verschil in gekochten straten"
	test.timeout = lambda : 90



@t.passed(correctAverageDiv)
@t.test(20)
def correctAverageDiv2(test):
	def testMethod():
		def findline(outputOf):
			tsts = ['startgeld', 'evenveel', 'straten']
			for line in outputOf.split("\n"):
				if all([assertlib.contains(line, tst) for tst in tsts]):
					return line
			return ""

		line = findline(lib.outputOf(_fileName))

		info = ""
		if assertlib.numberOnLine(75, line):
			info = "De gevonden waarde is 75 euro. Checkpy het programma nog een keer."

		return assertlib.numberOnLine(125, line), info

	test.test = testMethod
	test.description = lambda : "Monopoly met twee spelers vindt het correcte extra startgeld voor speler 2"
	test.timeout = lambda : 90
