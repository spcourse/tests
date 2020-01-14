import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

# all test first look if the checked function is in the code, hase the right 
# number of arguments and returns an answer of the right type.
# if not, a message will show.


@t.test(0)
def Correctnumber_of_letters_in(test):
    test_text = "Stick Boy liked Match Girl, he liked her a lot"
    function_name = "number_of_letters_in"
    
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
            info = "Make sure you return an integer and nothing else."
            return False, info

        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), 36)

    test.test = testMethod
    test.description = lambda : "Finds the correct number of letters in a text."


@t.test(1)
def Correctnumber_of_words_in(test):
    test_text = "He liked her cute figure, he thought she was hot."
    function_name = "number_of_words_in"
    
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
            info = "Make sure you return an integer and nothing else."
            return False, info

        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), len(test_text.split(" "))  )

    test.test = testMethod
    test.description = lambda : "Finds the correct number of words in a text."



@t.test(2)
def Correctnumber_of_sentences_in(test):
    test_text = "But could a flame. ever burn. for a match and a stick."
    function_name = "number_of_sentences_in"
    
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
            info = "Make sure you return an integer and nothing else."
            return False, info
                
        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), len(test_text.split(".")) -1)

    test.test = testMethod
    test.description = lambda : "Finds the correct number of sentences in a text."



@t.test(3)
def Correctaverage_word_length(test):
    test_text = "It did quite literally; he burned up pretty quick."
    function_name = "average_word_length"
    
    def testMethod():
        hasfunction = assertlib.fileContainsFunctionDefinitions(_fileName, function_name)
        if not hasfunction:
            info = "Make sure you use a function named " + function_name + " as you're writing your code."
            return False, info
        
        nArguments = len(lib.getFunction(function_name, _fileName).arguments)
        if nArguments != 1:
            info = "Make sure your function has 1 argument."
            return False, info

        correct_return = assertlib.sameType(lib.getFunction(function_name, _fileName)(test_text), 1.)
        if not correct_return:
            info = "Make sure you return an integer and nothing else."
            return False, info
                
        return assertlib.exact(lib.getFunction(function_name, _fileName)(test_text), 40/9)

    test.test = testMethod
    test.description = lambda : "Finds the correct average length of words in a sentence."
