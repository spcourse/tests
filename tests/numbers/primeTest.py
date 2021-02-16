import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

@t.test(0)
def exact1(test):

	notAllowed = {"lists": "[", "break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = lambda : assertlib.numberOnLine(2, lib.getLine(lib.outputOf(_fileName, stdinArgs=[1]), 0))
	test.description = lambda : "input of 1 yields output of 2"

@t.test(10)
def exact1000(test):
	test.test = lambda : assertlib.numberOnLine(7919, lib.getLine(lib.outputOf(_fileName, stdinArgs=[1000]), 0))
	test.description = lambda : "input of 1000 yields output of 7919"
	test.timeout = lambda : 90

@t.passed(exact1)
@t.test(30)
def handlesWrongInput(test):
	test.test = lambda : assertlib.numberOnLine(2, lib.getLine(lib.outputOf(_fileName, stdinArgs=[-90, -1, 0, 1]), 0))
	test.description = lambda : "rejects zero as input and rejects negative input"
