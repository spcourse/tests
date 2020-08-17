import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

def clean_lines(text):
	lines = text.split('\n')
	lines = [line.strip() for line in lines]
	if lines[-1] == "":
		lines = lines[:-1]
	return lines

def testBirthday(vali, valo):
	result = lib.outputOf(_fileName, stdinArgs=[vali])
	lines = clean_lines(result)
	if len(lines) < 1:
		return False, "No output"
	line = lines[0]
	ints = set(lib.getPositiveIntegersFromString(line))
	if valo in ints:
		return True
	return False, f'Expected {valo}'

@t.test(1)
def outputsYears(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[1])

		lines = clean_lines(result)
		if len(lines) > 1:
			return False, "Output consists of more than one line"
		if len(lines) < 1:
			return False, "No output"
		line = lines[0]
		ints = lib.getPositiveIntegersFromString(line)
		if len(ints) < 1:
			return False, "No year found in the output"
		return True

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = testMethod
	test.fail = lambda info: info
	test.description = lambda : "The code outputs a line containing a number"
	test.timeout = lambda : 90


@t.test(1)
def check1(test):
	test.test = lambda: testBirthday(1, 2004)
	test.fail = lambda info: info
	test.description = lambda : "Testing birthday number 1"
	test.timeout = lambda : 90

@t.test(2)
def check2(test):
	test.test = lambda: testBirthday(2, 2008)
	test.fail = lambda info: info
	test.description = lambda : "Testing birthday number 2"
	test.timeout = lambda : 90

@t.test(3)
def check1000(test):
	test.test = lambda: testBirthday(1000, 6124)
	test.fail = lambda info: info
	test.description = lambda : "Testing birthday number 1000"
	test.timeout = lambda : 90
