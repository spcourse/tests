import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib
import helpers
import re

def sandbox():
	lib.require("DeBiltTempMax.txt", "http://www.nikhef.nl/~ivov/Python/KlimaatData/DeBiltTempMax.txt")
	lib.require("DeBiltTempMin.txt", "http://www.nikhef.nl/~ivov/Python/KlimaatData/DeBiltTempMin.txt")


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

# Thanks to Vera Schild!

@t.test(10)
def correctHighestTemp(test):
	def testMethod():
		correctAnswer = "36.8"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. {} staat in de source code!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "print hoogste temperatuur"

@t.passed(correctHighestTemp)
@t.test(11)
def correctDateHighestTemp(test):
	def testMethod():
		if helpers.isHardcodedIn(1947, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. 1947 staat in de source code!"

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = helpers.findLineWith(output, "36.8")

		correctDay = assertlib.contains(line, '27')
		correctMonth = any([assertlib.contains(line.lower(), month) for month in ["6", "juni", "june", "jun"]])
		correctYear = assertlib.contains(line, '1947')
		return correctDay and correctMonth and correctYear

	test.test = testMethod
	test.description = lambda : "print datum hoogste temperatuur"

@t.test(20)
def correctLowestTemp(test):
	def testMethod():
		correctAnswer = "-24.8"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. {} staat in de source code!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "print laagste temperatuur"

@t.passed(correctLowestTemp)
@t.test(21)
def correctDateLowestTemp(test):
	def testMethod():
		if helpers.isHardcodedIn(1942, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. 1942 staat in de source code!"

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = helpers.findLineWith(output, "-24.8")

		correctDay = assertlib.contains(line, '27')
		correctMonth = any([assertlib.contains(line.lower(), month) for month in ["1", "januari", "january", "jan"]])
		correctYear = assertlib.contains(line, '1942')
		return correctDay and correctMonth and correctYear

	test.test = testMethod
	test.description = lambda : "print datum laagste temperatuur"

@t.test(30)
def correctLongestFreezing(test):
	def testMethod():
		correctAnswer = "21"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. {} staat in de source code!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "print de langste periode dat het aaneengesloten heeft gevroren"

@t.passed(correctLongestFreezing)
@t.test(31)
def correctDateLongestFreezingp(test):
	def testMethod():
		if helpers.isHardcodedIn(1947, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. 1947 staat in de source code!"

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = helpers.findLineWith(output, "21")

		correctDay = assertlib.contains(line, '24')
		correctMonth = any([assertlib.contains(line.lower(), month) for month in ["2", "februari", "february", "feb"]])
		correctYear = assertlib.contains(line, '1947')
		return correctDay and correctMonth and correctYear

	test.test = testMethod
	test.description = lambda : "print laatste dag van de langste periode dat het aaneengesloten heeft gevroren"

@t.test(40)
def correctFirstHeatWave(test):
	def testMethod():
		correctAnswer = "1911"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "let op: deze output is hardcoded. {} staat in de source code!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "print het eerste jaartal waarin er sprake was van een hittegolf"

@t.test(50)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig") or assertlib.fileContainsFunctionCalls(_fileName, "show")
	test.description = lambda : "slaat een grafiek op, of laat een grafiek zien"
