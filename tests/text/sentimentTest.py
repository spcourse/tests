import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

# Test once again test if the function is in the code with the right amount of
# arguments and right type of return, but only gives a mesage at test 0.

def sandbox():
	lib.require("pos_words.txt", "https://sp1.mprog.nl/course/modules/text/en/sentiment/pos_words.txt")
	lib.require("neg_words.txt", "https://sp1.mprog.nl/course/modules/text/en/sentiment/neg_words.txt")


@t.test(0)
def Correctfor_pos(test):
    test_text = "Coronet has the best lines of all day cruisers."
    function_name = "sentiment_of_text"

    def testMethod():
        hasfunction = assertlib.fileContainsFunctionDefinitions(_fileName, function_name)
        if not hasfunction:
            info = "Make sure you use a function named " + function_name + " as you're writing your code."
            return False, info

        nArguments = len(lib.getFunction(function_name, _fileName).arguments)
        if nArguments != 1:
            info = "Make sure your function has 1 argument."
            return False, info

        correct_return = assertlib.sameType(lib.getFunction(function_name, _fileName)(test_text), 1)
        if not correct_return:
            info = "Make sure you return an list and nothing else."
            return False, info

        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), 1)

    test.test = testMethod
    test.description = lambda : "Recognises a positive sentence."


@t.test(1)
def Correctfor_neu(test):
    test_text = "Bertram has a deep V hull and runs easily through seas."
    function_name = "sentiment_of_text"

    def testMethod():
        hasfunction = assertlib.fileContainsFunctionDefinitions(_fileName, function_name)
        if not hasfunction:
            return False

        nArguments = len(lib.getFunction(function_name, _fileName).arguments)
        if nArguments != 1:
            return False

        correct_return = assertlib.sameType(lib.getFunction(function_name, _fileName)(test_text), 1)
        if not correct_return:
            return False

        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), 0)

    test.test = testMethod
    test.description = lambda : "Recognises a neutral sentence."


@t.test(3)
def Correctfor_neg(test):
    test_text = "I dislike old cabin cruisers."
    function_name = "sentiment_of_text"

    def testMethod():
        hasfunction = assertlib.fileContainsFunctionDefinitions(_fileName, function_name)
        if not hasfunction:
            return False

        nArguments = len(lib.getFunction(function_name, _fileName).arguments)
        if nArguments != 1:
            return False

        correct_return = assertlib.sameType(lib.getFunction(function_name, _fileName)(test_text), 1)
        if not correct_return:
            return False

        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), -1)

    test.test = testMethod
    test.description = lambda : "Recognises a negative sentence."
