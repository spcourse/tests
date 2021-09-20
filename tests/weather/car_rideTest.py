import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

def sandbox():
	lib.require("CarRideData.csv", "https://sp1.mprog.nl/materials/bigdata/data/en/CarRideData.csv")

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
def correctDistance(test):
	def testMethod():
		output = lib.outputOf(
			test.fileName,
			overwriteAttributes = [("__name__", "__main__")]
		)
		line = lib.getLine(output, 0)
		correctKm = assertlib.numberOnLine(10.86, line, deviation = 0.02)
		correctM = assertlib.numberOnLine(10860, line, deviation = 20)
		return correctKm or correctM
	test.test = testMethod
	test.description = lambda : "prints the distance traveled"

@t.test(1)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig") or assertlib.fileContainsFunctionCalls(_fileName, "show")
	test.description = lambda : "either saves a plot or shows one"
