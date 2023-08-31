from checkpy import *

import ast

only("reformatting.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"

   
correct_def_text_to_lines = (declarative
                 .function("text_to_lines")
                 .params("text", "max_length")
                 .returnType(str)
                 .description("function is defined correctly")
                 )

text_to_lines = (declarative
                 .function("text_to_lines")
                 )

testT1 = "Hello, my name is Bob. And I like to fish!  "
max_lengthT1 = 10

correctOutputT1 = "Hello, my\nname is\nBob. And I\nlike to\nfish!  "

# test if there are no spaces at the end of the line
correctSpaces = test()(text_to_lines
                       .call(testT1, max_lengthT1)
                       .returns(correctOutputT1)
                       .description("function handles spaces at the end of the text correctly")
                       )

testT2 = "Cat Cat Cat"
max_lengthT2 = 10

correctOutputT2 = "Cat Cat\nCat"

# test if there if the first word is handled correctly
correctFirstWord = test()(text_to_lines
                       .call(testT2, max_lengthT2)
                       .returns(correctOutputT2)
                       .description("function handles the first word correctly")
                       )

testT3 = "Will do"
max_lengthT3 = 6

correctOutputT3 = "Will\ndo"

correctSpaceInclusionInLineLength = test()(text_to_lines
                                           .call(testT3, max_lengthT3)
                                           .returns(correctOutputT3)
                                           .description("function includes spaces in the line length calculation")
                                           )


testT4 = "Will do just fine"
max_lengthT4 = 7

correctOutputT4 = "Will do\njust\nfine"

correctLineSplitConsideringSpaces = test()(text_to_lines
                                           .call(testT4, max_lengthT4)
                                           .returns(correctOutputT4)
                                           .description("function splits lines considering spaces and does not leave out single words")
                                           )

# The function should ignore trailing and leading spaces in the input text while splitting the text into lines.
testT5 = "       This is a significantly longer sentence with more spaces around it.        "
max_lengthT5 = 20

correctOutputT5 = "       This is a\nsignificantly longer\nsentence with more\nspaces around it.   \n    "

correctTextWithSpaces = test()(text_to_lines
                                   .call(testT5, max_lengthT5)
                                   .returns(correctOutputT5)
                                   .description("function works with a text with substantial trailing and leading spaces")
                                   )

# The function should handle multiple spaces between words and consider only a single space while splitting the text into lines.
testT6 = "The  quick   brown    fox   jumps   over    the     lazy   dog."
max_lengthT6 = 15

correctOutputT6 = "The  quick  \nbrown    fox  \njumps   over   \nthe     lazy  \ndog."

correctHandlingOfMultipleSpaces = test()(text_to_lines
                                         .call(testT6, max_lengthT6)
                                         .returns(correctOutputT6)
                                         .description("function handles multiple spaces between words and considers only a single space while splitting the text into lines")
                                         )

# When the input text contains a single word, the function should return the word as is, regardless of the max_length.
testT7 = "Supercalifragilisticexpialidocious"
max_lengthT7 = 15

correctOutputT7 = "Supercalifragilisticexpialidocious"

correctHandlingOfSingleWord = test()(text_to_lines
                                         .call(testT7, max_lengthT7)
                                         .returns(correctOutputT7)
                                         .description("function returns the single word as is, regardless of the max_length")
                                         )

# When the input text is empty, the function should return an empty string.
# Test with a single word text:
testT8 = ""
max_lengthT8 = 15

correctOutputT8 = ""

correctHandlingOfEmptyInput = test()(text_to_lines
                                     .call(testT8, max_lengthT8)
                                     .returns(correctOutputT8)
                                     .description("function returns an empty string when the input text is empty")
                                     )

testT9 = """Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, `and what is the use of a book,' thought Alice `without pictures or conversation?' So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her. There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, `Oh dear! Oh dear! I shall be late!' (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT- POCKET, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge. In another moment down went Alice after it, never once considering how in the world she was to get out again. The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well. Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled `ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it. `Well!' thought Alice to herself, `after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.) Down, down, down. Would the fall NEVER come to an end! `I wonder how many miles I've fallen by this time?' she said aloud. `I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think--' (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a VERY good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) `--yes, that's about the right distance--but then I wonder what Latitude or Longitude I've got to?' (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)"""
max_lengthT9 = 77

correctOutputT9 = """Alice was beginning to get very tired of sitting by her sister on the bank,
and of having nothing to do: once or twice she had peeped into the book her
sister was reading, but it had no pictures or conversations in it, `and what
is the use of a book,' thought Alice `without pictures or conversation?' So
she was considering in her own mind (as well as she could, for the hot day
made her feel very sleepy and stupid), whether the pleasure of making a
daisy-chain would be worth the trouble of getting up and picking the daisies,
when suddenly a White Rabbit with pink eyes ran close by her. There was
nothing so VERY remarkable in that; nor did Alice think it so VERY much out
of the way to hear the Rabbit say to itself, `Oh dear! Oh dear! I shall be
late!' (when she thought it over afterwards, it occurred to her that she
ought to have wondered at this, but at the time it all seemed quite natural);
but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT- POCKET, and
looked at it, and then hurried on, Alice started to her feet, for it flashed
across her mind that she had never before seen a rabbit with either a
waistcoat-pocket, or a watch to take out of it, and burning with curiosity,
she ran across the field after it, and fortunately was just in time to see it
pop down a large rabbit-hole under the hedge. In another moment down went
Alice after it, never once considering how in the world she was to get out
again. The rabbit-hole went straight on like a tunnel for some way, and then
dipped suddenly down, so suddenly that Alice had not a moment to think about
stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of
time as she went down to look about her and to wonder what was going to
happen next. First, she tried to look down and make out what she was coming
to, but it was too dark to see anything; then she looked at the sides of the
well, and noticed that they were filled with cupboards and book-shelves; here
and there she saw maps and pictures hung upon pegs. She took down a jar from
one of the shelves as she passed; it was labelled `ORANGE MARMALADE', but to
her great disappointment it was empty: she did not like to drop the jar for
fear of killing somebody, so managed to put it into one of the cupboards as
she fell past it. `Well!' thought Alice to herself, `after such a fall as
this, I shall think nothing of tumbling down stairs! How brave they'll all
think me at home! Why, I wouldn't say anything about it, even if I fell off
the top of the house!' (Which was very likely true.) Down, down, down. Would
the fall NEVER come to an end! `I wonder how many miles I've fallen by this
time?' she said aloud. `I must be getting somewhere near the centre of the
earth. Let me see: that would be four thousand miles down, I think--' (for,
you see, Alice had learnt several things of this sort in her lessons in the
schoolroom, and though this was not a VERY good opportunity for showing off
her knowledge, as there was no one to listen to her, still it was good
practice to say it over) `--yes, that's about the right distance--but then I
wonder what Latitude or Longitude I've got to?' (Alice had no idea what
Latitude was, or Longitude either, but thought they were nice grand words to
say.)"""

correctLongText = test()(text_to_lines
                        .call(testT9, max_lengthT9)
                        .returns(correctOutputT9)
                        .description("Function works with a long text")
                        )