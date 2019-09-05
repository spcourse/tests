import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

# @t.test(0)
# def exact16times4(test):
#
#     notAllowed = {"import": "import"}
#     notAllowedCode(test, lib.source(_fileName), notAllowed)
#
#     test.test = lambda : assertlib.numberOnLine(64, lib.getLine(lib.outputOf(_fileName, stdinArgs=[16, 4]), 0))
#     test.description = lambda : "het product van 16 en 4 is 64"
#
# @t.test(1)
# def exact27times5(test):
#     test.test = lambda : assertlib.numberOnLine(135, lib.getLine(lib.outputOf(_fileName, stdinArgs=[27, 5]), 0))
#     test.description = lambda : "het product van 27 en 5 is 135"

@t.test(2)
def exact3492times9876(test):
	test.test = lambda : assertlib.numberOnLine(34486992, lib.getLine(lib.outputOf(_fileName, stdinArgs=[3492, 9876]), 0))
	test.description = lambda : "input of 3492 and 9876 yields 34486992"
