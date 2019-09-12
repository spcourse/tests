import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import math

@t.test(0)
def correctAmount(test):
	test.test = lambda : assertlib.numberOnLine(math.e, lib.getLine(lib.outputOf(_fileName), 0), deviation = 0.0027)
	test.description = lambda : "yields the correct answer"
	test.succes = lambda info : "does the number ring familiar?"
