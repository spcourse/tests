import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

def sandbox():
	lib.require("AutoRitData.csv", "http://www.nikhef.nl/~ivov/Python/SensorData/AutoRitData.csv")

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
	test.description = lambda : "print de afgelegde afstand"

@t.test(1)
def showsGraph(test):
	test.test = lambda : assertlib.fileContainsFunctionCalls(_fileName, "savefig") or assertlib.fileContainsFunctionCalls(_fileName, "show")
	test.description = lambda : "slaat een grafiek op, of laat een grafiek zien"
