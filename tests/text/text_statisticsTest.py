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
    .description("correctly defined the function number_of_letters_in")
)


correct_def_number_of_words_in = test()(declarative
    .function("number_of_words_in")
    .params("text")
    .returnType(int)
    .description("correctly defined the function number_of_words_in")
)


correct_def_number_of_sentences_in = test()(declarative
    .function("number_of_sentences_in")
    .params("text")
    .returnType(int)
    .description("correctly defined the function number_of_sentences_in")
)


correct_def_avarage_word_length = test()(declarative
    .function("average_word_length")
    .params("text")
    .returnType(float)
    .description("correctly defined the function average_word_length")
)


correct_number_of_letters_in = test()(declarative
    .function("number_of_letters_in")
    .call("Stick Boy liked Match Girl, he liked her a lot")
    .returns(36)
    .description("correctly counts the number of letters in a text")
)


correct_number_of_words_in = test()(declarative
    .function("number_of_words_in")
    .call("He liked her cute figure, he thought she was hot.")
    .returns(10)
    .description("correctly counts the number of words in a text")
)


correct_number_of_sentences_in = test()(declarative
    .function("number_of_sentences_in")
    .call("But could a flame. ever burn. for a match and a stick.")
    .returns(3)
    .description("correctly counts the number of sentences in a text")
)


correct_avarage_word_length = test()(declarative
    .function("average_word_length")
    .call("It did quite literally; he burned up pretty quick.")
    .returns(40 / 9)
    .description("correctly calculates the average word length in a text")
)