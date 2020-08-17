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


@t.test(1)
def outputsYears(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[2000,2010])

		for line in clean_lines(result):
			years = lib.getPositiveIntegersFromString(line)
			if len(years) > 0:
				return True

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = testMethod

	test.description = lambda : "The code outputs years"
	test.timeout = lambda : 90

@t.test(2)
def outputsOneYearPerLine(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[2000,2010])

		for line in clean_lines(result):
			years = lib.getPositiveIntegersFromString(line)
			if len(years) != 1:
				return False
		return True

	test.test = testMethod

	test.description = lambda : "The code outputs exactly one year per line"
	test.timeout = lambda : 90

@t.test(3)
def leapYearsStraight(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[2004,2013])
		expected_years = set([2004,2008,2012])
		printed_years = set(lib.getPositiveIntegersFromString(result))
		return expected_years == printed_years

	test.test = testMethod

	test.description = lambda : "Leap years between 2004 and 2013"
	test.timeout = lambda : 90

@t.test(4)
def leapYears100(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[1890,1920])
		expected_years = set([1892, 1896, 1904, 1908, 1912, 1916])
		printed_years = set(lib.getPositiveIntegersFromString(result))
		return expected_years == printed_years

	test.test = testMethod

	test.description = lambda : "Leap years between 1890 and 1920"
	test.timeout = lambda : 90

@t.test(5)
def leapYears400(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[1990,2020])
		expected_years = set([1992, 1996, 2000, 2004, 2008, 2012, 2016])
		printed_years = set(lib.getPositiveIntegersFromString(result))
		return expected_years == printed_years

	test.test = testMethod

	test.description = lambda : "Leap years between 1990 and 2020"
	test.timeout = lambda : 90
