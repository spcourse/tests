import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

@t.test(0)
def exactChange0(test):
	test.test = lambda : assertlib.numberOnLine(0, lib.getLine(lib.outputOf(_fileName, stdinArgs=[0]), 0))
	test.description = lambda : "input of 0 yields output of 0"

@t.test(1)
def exactChange41(test):
	test.test = lambda : assertlib.numberOnLine(4, lib.getLine(lib.outputOf(_fileName, stdinArgs=[0.41]), 0))
	test.description = lambda : "input of 0.41 yields output of 4"

@t.test(2)
def exactChange001(test):
	test.test = lambda : assertlib.numberOnLine(1, lib.getLine(lib.outputOf(_fileName, stdinArgs=[0.01]), 0))
	test.description = lambda : "input of 0.01 yields output of 1"

@t.test(3)
def exactChange16(test):
	test.test = lambda : assertlib.numberOnLine(7, lib.getLine(lib.outputOf(_fileName, stdinArgs=[1.6]), 0))
	test.description = lambda : "input of 1.6 yields output of 7"

@t.test(4)
def exactChange420(test):
	test.test = lambda : assertlib.numberOnLine(18, lib.getLine(lib.outputOf(_fileName, stdinArgs=[4.2]), 0))
	test.description = lambda : "input of 4.2 yields output of 18"
	test.fail = lambda info : "did you forget to round your input to the nearest cent?"

@t.test(10)
def handlesWrongInput(test):
	test.test = lambda : assertlib.numberOnLine(4, lib.getLine(lib.outputOf(_fileName, stdinArgs=[-1, -1, -1, -1, -1, -1, -1, 0.41]), 0))
	test.description = lambda : "rejects negative input"
