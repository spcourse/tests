# Test once again test if the function is in the code with the right amount of
# arguments and right type of return, but only gives a mesage at test 0.

from checkpy import *

only("sentiment.py")
download("pos_words.txt", "https://github.com/spcourse/text/raw/main/en/sentiment/pos_words.txt")
download("neg_words.txt", "https://github.com/spcourse/text/raw/main/en/sentiment/neg_words.txt")

sentiment_of_text = (declarative
    .function("sentiment_of_text")
    .params("text")
    .returnType(int)
)

correctForPos = test()(sentiment_of_text
    .call("Coronet has the best lines of all day cruisers.")
    .returns(1)
    .description("recognises a positive sentence")
)

correctForNeutral = test()(sentiment_of_text
    .call("Bertram has a deep V hull and runs easily through seas.")
    .returns(0)
    .description("recognises a neutral sentence")
)

correctForNeg = test()(sentiment_of_text
    .call("I dislike old cabin cruisers.")
    .returns(-1)
    .description("recognises a negative sentence")
)