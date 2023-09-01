from checkpy import *

import ast

only("sentiment.py")
download("pos_words.txt", "https://github.com/spcourse/text/raw/main/en/sentiment/pos_words.txt")
download("neg_words.txt", "https://github.com/spcourse/text/raw/main/en/sentiment/neg_words.txt")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"


correct_def_cleanup = test()(declarative
    .function("cleanup")
    .returnType(str)
    .params("word")
    .call("ClEaN!")
    .returns("clean")
    .description("correctly defines the cleanup() function")
)


correct_def_sentiment_of_text = test()(declarative
    .function("sentiment_of_text")
    .params("text")
    .returnType(int)
    .call("")
    .description("correctly defines the sentiment_of_text() function")
)


sentiment_of_text = (declarative
    .function("sentiment_of_text")
)


cleanup = (declarative
    .function("cleanup")
)


@passed(correct_def_sentiment_of_text, hide=False)
def correctForPos():
    """recognises a positive sentence"""
    sentiment_of_text.call("Coronet has the best lines of all day cruisers.").returns(1)()


@passed(correct_def_sentiment_of_text, hide=False)
def correctForNeutral():
    """recognises a neutral sentence"""
    sentiment_of_text.call("Bertram has a deep V hull and runs easily through seas.").returns(0)()


@passed(correct_def_sentiment_of_text, hide=False)
def correctForNeg():
    """recognises a negative sentence"""
    sentiment_of_text.call("I dislike old cabin cruisers.").returns(-1)()