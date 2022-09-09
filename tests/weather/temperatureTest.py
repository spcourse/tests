import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib
import helpers
import re

def sandbox():
	lib.require("DeBiltTempMaxOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMaxOLD.txt")
	lib.require("DeBiltTempMinOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLD.txt")


def before():
	try:
		import matplotlib
		import warnings
		warnings.filterwarnings("ignore", module = "plot")
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

# Thanks to Vera Schild!

@t.test(10)
def correctHighestTemp(test):
	def testMethod():
		correctAnswer = "36.8"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "watch out: {} appears to be hardcoded!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "prints the highest temperature"

@t.passed(correctHighestTemp)
@t.test(11)
def correctDateHighestTemp(test):
	def testMethod():
		if helpers.isHardcodedIn(1947, test.fileName):
			test.success = lambda info : "watch out: 1947 appears to be hardcoded!"

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = helpers.findLineWith(output, "36.8")

		correctDay = assertlib.contains(line, '27')
		correctMonth = any([assertlib.contains(line.lower(), month) for month in ["juni", "june", "jun"]])
		correctYear = assertlib.contains(line, '1947')
		return correctDay and correctMonth and correctYear

	test.test = testMethod
	test.description = lambda : "prints the date of the highest temperature"

@t.test(20)
def correctLowestTemp(test):
	def testMethod():
		correctAnswer = "-24.8"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "watch out: {} appears to be hardcoded!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "prints the lowest temperature"

@t.passed(correctLowestTemp)
@t.test(21)
def correctDateLowestTemp(test):
	def testMethod():
		if helpers.isHardcodedIn(1942, test.fileName):
			test.success = lambda info : "watch out: 1942 appears to be hardcoded!"

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = helpers.findLineWith(output, "-24.8")

		correctDay = assertlib.contains(line, '27')
		correctMonth = any([assertlib.contains(line.lower(), month) for month in ["januari", "january", "jan"]])
		correctYear = assertlib.contains(line, '1942')
		return correctDay and correctMonth and correctYear

	test.test = testMethod
	test.description = lambda : "prints the date of the lowest temperature"

@t.test(30)
def correctLongestFreezing(test):
	def testMethod():
		correctAnswer = "21"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "watch out: {} appears to be hardcoded!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "prints the longest period of frost (in days)"

@t.passed(correctLongestFreezing)
@t.test(31)
def correctDateLongestFreezingp(test):
	def testMethod():
		if helpers.isHardcodedIn(1947, test.fileName):
			test.success = lambda info : "watch out: 1947 appears to be hardcoded!"

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = helpers.findLineWith(output, "21")

		correctDay = assertlib.contains(line, '24')
		correctMonth = any([assertlib.contains(line.lower(), month) for month in ["februari", "february", "feb"]])
		correctYear = assertlib.contains(line, '1947')
		return correctDay and correctMonth and correctYear, "Did you print the date on the same line as the longest period of frost?"

	test.test = testMethod
	test.description = lambda : "prints the last day of the longest freezing period"

@t.test(40)
def correctFirstHeatWave(test):
	def testMethod():
		correctAnswer = "1911"
		if helpers.isHardcodedIn(correctAnswer, test.fileName):
			test.success = lambda info : "watch out: {} appears to be hardcoded!".format(correctAnswer)

		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		return assertlib.contains(output, correctAnswer)

	test.test = testMethod
	test.description = lambda : "prints the first year that had a heatwave"

@t.test(50)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig") or assertlib.fileContainsFunctionCalls(_fileName, "show")
	test.description = lambda : "either saves a plot to image, or shows it"
