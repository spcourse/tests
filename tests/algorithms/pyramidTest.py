import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import re

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

@t.test(0)
def exactMario0(test):
	test.test = lambda : assertlib.match(lib.outputOf(_fileName, stdinArgs=[1]),
		re.compile(".*(# #)[ ]*(\n)"))
	test.description = lambda : "prints a well-formed pyramid of height 1"

@t.test(1)
def exactMario3(test):
	test.test = lambda : assertlib.match(lib.outputOf(_fileName, stdinArgs=[3]), 
		re.compile(".*"
			"(    # #)[ ]*(\n)"
			"(  # # #)[ ]*(\n)"
			"(# # # #)[ ]*"
			".*", re.MULTILINE))
	test.description = lambda : "prints a well-formed pyramid of height 3"

@t.test(2)
def exactMario23(test):
	test.test = lambda : assertlib.match(lib.outputOf(_fileName, stdinArgs=[23]),
		re.compile(".*"
			"(                                            # #)[ ]*(\n)"
			"(                                          # # #)[ ]*(\n)"
			"(                                        # # # #)[ ]*(\n)"
			"(                                      # # # # #)[ ]*(\n)"
			"(                                    # # # # # #)[ ]*(\n)"
			"(                                  # # # # # # #)[ ]*(\n)"
			"(                                # # # # # # # #)[ ]*(\n)"
			"(                              # # # # # # # # #)[ ]*(\n)"
			"(                            # # # # # # # # # #)[ ]*(\n)"
			"(                          # # # # # # # # # # #)[ ]*(\n)"
			"(                        # # # # # # # # # # # #)[ ]*(\n)"
			"(                      # # # # # # # # # # # # #)[ ]*(\n)"
			"(                    # # # # # # # # # # # # # #)[ ]*(\n)"
			"(                  # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(                # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(              # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(            # # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(          # # # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(        # # # # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(      # # # # # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(    # # # # # # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(  # # # # # # # # # # # # # # # # # # # # # # #)[ ]*(\n)"
			"(# # # # # # # # # # # # # # # # # # # # # # # #)[ ]*"
			".*", re.MULTILINE))
	test.description = lambda : "prints a well-formed pyramid of height 23"

@t.test(10)
def handlesWrongInput(test):
	notAllowed = {"the * operator, but instead loops": "*"}
	
	def test_code():
		notAllowedCode(test, lib.source(_fileName), notAllowed)
		return assertlib.match(lib.outputOf(_fileName, stdinArgs=[-100, 24, 1])

	test.test = test_code,
	re.compile(".*(# #)[ ]*(\n)"))
	test.description = lambda : "rejects heights of -100 and 24, then accepts a height of 1"
