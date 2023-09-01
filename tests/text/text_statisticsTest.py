from checkpy import *

import ast

only("text_statistics.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


@test()
def noStrCount():
    """the program does not use str.count method"""
    assert not any(".count" in line for line in static.getFunctionCalls()), "you cannot use the str.count method"


correct_def_number_of_letters_in = test()(declarative
    .function("number_of_letters_in")
    .params("text")
    .returnType(int)
    .call("Test sentence")
    .description("correctly defines the number_of_letters_in() function")
)


correct_def_number_of_words_in = test()(declarative
    .function("number_of_words_in")
    .params("text")
    .returnType(int)
    .call("Test sentence")
    .description("correctly defines the number_of_words_in() function")
)


correct_def_number_of_sentences_in = test()(declarative
    .function("number_of_sentences_in")
    .params("text")
    .returnType(int)
    .call("Test sentence")
    .description("correctly defines the number_of_sentences_in() function")
)


correct_def_average_word_length = test()(declarative
    .function("average_word_length")
    .params("text")
    .returnType(float)
    .call("Test sentence")
    .description("correctly defines the average_word_length() function")
)


@passed(correct_def_number_of_letters_in, hide=False)
def correctNumberOfLetters():
    """function works correctly for counting letters"""
    declarative.function("number_of_letters_in").call("Stick Boy liked Match Girl, he liked her a lot").returns(36)()


@passed(correct_def_number_of_words_in, hide=False)
def correctNumberOfWords():
    """function works correctly for counting words"""
    declarative.function("number_of_words_in").call("He liked her cute figure, he thought she was hot.").returns(10)()


@passed(correct_def_number_of_sentences_in, hide=False)
def correctNumberOfSentences():
    """function works correctly for counting sentences"""
    declarative.function("number_of_sentences_in").call("But could a flame. ever burn. for a match and a stick.").returns(3)()


@passed(correct_def_average_word_length, hide=False)
def correctAverageWordLength():
    """function works correctly for calculating average word length"""
    declarative.function("average_word_length").call("It did quite literally; he burned up pretty quick.").returns(40 / 9)()