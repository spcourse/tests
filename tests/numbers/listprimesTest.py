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
def outputsNumbers(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[10])

		for line in clean_lines(result):
			years = lib.getPositiveIntegersFromString(line)
			if len(years) > 0:
				return True

	notAllowed = {"break": "break"}
	notAllowedCode(test, lib.source(_fileName), notAllowed)

	test.test = testMethod

	test.description = lambda : "The code outputs numbers"
	test.timeout = lambda : 90


@t.test(2)
def correctList10(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[10])
		expected_numbers = set([2, 3, 5, 7])
		printed_numbers = set(lib.getPositiveIntegersFromString(result))
		return expected_numbers == printed_numbers

	test.test = testMethod

	test.description = lambda : "Correct list of primes below 10"
	test.timeout = lambda : 90

@t.test(3)
def correctList11(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[11])
		expected_numbers = set([2, 3, 5, 7])
		printed_numbers = set(lib.getPositiveIntegersFromString(result))
		return expected_numbers == printed_numbers

	test.test = testMethod

	test.description = lambda : "Correct list of primes below 11"
	test.timeout = lambda : 90

@t.test(3)
def correctList100(test):
	def testMethod():
		result = lib.outputOf(_fileName, stdinArgs=[100])
		expected_numbers = set([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
		printed_numbers = set(lib.getPositiveIntegersFromString(result))
		return expected_numbers == printed_numbers

	test.test = testMethod

	test.description = lambda : "Correct list of primes below 100"
	test.timeout = lambda : 90
