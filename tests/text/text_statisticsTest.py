# all test first look if the checked function is in the code, hase the right 
# number of arguments and returns an answer of the right type.
# if not, a message will show.

from checkpy import *

only("text_statistics.py")

correct_number_of_letters_in = test()(declarative
    .function("number_of_letters_in")
    .params("text")
    .returns(int)
    .call("Stick Boy liked Match Girl, he liked her a lot")
    .returns(36)
)

correct_number_of_words_in = test()(declarative
    .function("number_of_words_in")
    .params("text")
    .returnType(int)
    .call("He liked her cute figure, he thought she was hot.")
    .returns(10)
)

correct_number_of_sentences_in = test()(declarative
    .function("number_of_sentences_in")
    .params("text")
    .returnType(int)
    .call("But could a flame. ever burn. for a match and a stick.")
    .returns(4)
)

correct_avarage_word_length = test()(declarative
    .function("average_word_length")
    .params("text")
    .returnType(float)
    .call("It did quite literally; he burned up pretty quick.")
    .returns(40 / 9)
)
