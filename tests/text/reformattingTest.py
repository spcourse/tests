from checkpy import *

only("reformatting.py")

   
text_to_lines = (declarative
                 .function("text_to_lines")
                 .params("text", "max_length")
                 .returnType(str)
                 )

testDef = test()(text_to_lines
                 .description("Function is defined correctly")
                 )

testT1 = "Hello, my name is Bob. And I like to fish!  "
max_lengthT1 = 10

correctOutputT1 = "Hello, my\nname is\nBob. And I\nlike to\nfish!  "

# test if there are no spaces at the end of the line
correctSpaces = test()(text_to_lines
                       .call(testT1, max_lengthT1)
                       .returns(correctOutputT1)
                       .description("Function handles spaces at the end of the text correctly")
                       )

testT2 = "Cat Cat Cat"
max_lengthT2 = 10

correctOutputT2 = "Cat Cat\nCat"

# test if there if the first word is handled correctly
correctFirstWord = test()(text_to_lines
                       .call(testT2, max_lengthT2)
                       .returns(correctOutputT2)
                       .description("Function handles the first word correctly")
                       )

testT3 = "Will do"
max_lengthT3 = 6

correctOutputT3 = "Will\ndo"

correctSpaceInclusionInLineLength = test()(text_to_lines
                                           .call(testT3, max_lengthT3)
                                           .returns(correctOutputT3)
                                           .description("Function includes spaces in the line length calculation")
                                           )


testT4 = "Will do just fine"
max_lengthT4 = 7

correctOutputT4 = "Will do\njust\nfine"

correctLineSplitConsideringSpaces = test()(text_to_lines
                                           .call(testT4, max_lengthT4)
                                           .returns(correctOutputT4)
                                           .description("Function splits lines considering spaces and does not leave out single words")
                                           )

# The function should ignore trailing and leading spaces in the input text while splitting the text into lines.
testT5 = "       This is a significantly longer sentence with more spaces around it.        "
max_lengthT5 = 20

correctOutputT5 = "       This is a\nsignificantly longer\nsentence with more\nspaces around it.   \n    "

correctTextWithSpaces = test()(text_to_lines
                                   .call(testT5, max_lengthT5)
                                   .returns(correctOutputT5)
                                   .description("Function works with a text with substantial trailing and leading spaces")
                                   )

# The function should handle multiple spaces between words and consider only a single space while splitting the text into lines.
testT6 = "The  quick   brown    fox   jumps   over    the     lazy   dog."
max_lengthT6 = 15

correctOutputT6 = "The  quick  \nbrown    fox  \njumps   over   \nthe     lazy  \ndog."

correctHandlingOfMultipleSpaces = test()(text_to_lines
                                         .call(testT6, max_lengthT6)
                                         .returns(correctOutputT6)
                                         .description("Function handles multiple spaces between words and considers only a single space while splitting the text into lines")
                                         )

# When the input text contains a single word, the function should return the word as is, regardless of the max_length.
testT7 = "Supercalifragilisticexpialidocious"
max_lengthT7 = 15

correctOutputT7 = "Supercalifragilisticexpialidocious"

correctHandlingOfSingleWord = test()(text_to_lines
                                         .call(testT7, max_lengthT7)
                                         .returns(correctOutputT7)
                                         .description("Function returns the single word as is, regardless of the max_length")
                                         )

# When the input text is empty, the function should return an empty string.
# Test with a single word text:
testT8 = ""
max_lengthT8 = 15

correctOutputT8 = ""

correctHandlingOfEmptyInput = test()(text_to_lines
                                     .call(testT8, max_lengthT8)
                                     .returns(correctOutputT8)
                                     .description("Function returns an empty string when the input text is empty")
                                     )

testT9 = """He proposed in the dunes, they were wed by the sea, Their nine-day-long honeymoon was on the isle of Capri. For their supper they had one specatular dish- a simmering stew of mollusks and fish. And while he savored the broth, her bride's heart made a wish. That wish came true-she gave birth to a baby. But was this little one human Well, maybe. Ten fingers, ten toes, he had plumbing and sight. He could hear, he could feel, but normal? Not quite. This unnatural birth, this canker, this blight, was the start and the end and the sum of their plight. She railed at the doctor: "He cannot be mine. He smells of the ocean, of seaweed and brine." "You should count yourself lucky, for only last week, I treated a girl with three ears and a beak. That your son is half oyster you cannot blame me. ... have you ever considered, by chance, a small home by the sea?" Not knowing what to name him, they just called him Sam, or sometimes, "that thing that looks like a clam" Everyone wondered, but no one could tell, When would young Oyster Boy come out of his shell? When the Thompson quadruplets espied him one day, they called him a bivalve and ran quickly away. One spring afternoon, Sam was left in the rain. At the southwestern corner of Seaview and Main, he watched the rain water as it swirled down the drain. His mom on the freeway in the breakdown lane was pouding the dashboard- she couldn't contain the ever-rising grief, frustration, and pain. "Really, sweetheart," she said "I don't mean to make fun, but something smells fishy and I think it's our son. I don't like to say this, but it must be said, you're blaming our son for your problems in bed." He tried salves, he tried ointments that turned everything red. He tried potions and lotions and tincture of lead. He ached and he itched and he twitched and he bled. The doctor diagnosed, "I can't quite be sure, but the cause of the problem may also be the cure. They say oysters improve your sexual powers. Perhaps eating your son would help you do it for hours!" He came on tiptoe, he came on the sly, sweat on his forehead, and on his lips-a lie. "Son, are you happy? I don't mean to pry, but do you dream of Heaven? Have you ever wanted to die? Sam blinked his eye twice. but made no reply. Dad fingered his knife and loosened his tie. As he picked up his son, Sam dripped on his coat. With the shell to his lips, Sam slipped down his throat. They burried him quickly in the sand by the sea -sighed a prayer, wept a tear- and they were back home by three. A cross of greay driftwood marked Oyster Boy's grave. Words writ in the sand promised Jesus would save. But his memory was lost with one high-tide wave."""
max_lengthT9 = 77

correctOutputT9 = """He proposed in the dunes, they were wed by the sea, Their nine-day-long
honeymoon was on the isle of Capri. For their supper they had one specatular
dish- a simmering stew of mollusks and fish. And while he savored the broth,
her bride's heart made a wish. That wish came true-she gave birth to a baby.
But was this little one human Well, maybe. Ten fingers, ten toes, he had
plumbing and sight. He could hear, he could feel, but normal? Not quite. This
unnatural birth, this canker, this blight, was the start and the end and the
sum of their plight. She railed at the doctor: "He cannot be mine. He smells
of the ocean, of seaweed and brine." "You should count yourself lucky, for
only last week, I treated a girl with three ears and a beak. That your son is
half oyster you cannot blame me. ... have you ever considered, by chance, a
small home by the sea?" Not knowing what to name him, they just called him
Sam, or sometimes, "that thing that looks like a clam" Everyone wondered, but
no one could tell, When would young Oyster Boy come out of his shell? When
the Thompson quadruplets espied him one day, they called him a bivalve and
ran quickly away. One spring afternoon, Sam was left in the rain. At the
southwestern corner of Seaview and Main, he watched the rain water as it
swirled down the drain. His mom on the freeway in the breakdown lane was
pouding the dashboard- she couldn't contain the ever-rising grief,
frustration, and pain. "Really, sweetheart," she said "I don't mean to make
fun, but something smells fishy and I think it's our son. I don't like to say
this, but it must be said, you're blaming our son for your problems in bed."
He tried salves, he tried ointments that turned everything red. He tried
potions and lotions and tincture of lead. He ached and he itched and he
twitched and he bled. The doctor diagnosed, "I can't quite be sure, but the
cause of the problem may also be the cure. They say oysters improve your
sexual powers. Perhaps eating your son would help you do it for hours!" He
came on tiptoe, he came on the sly, sweat on his forehead, and on his lips-a
lie. "Son, are you happy? I don't mean to pry, but do you dream of Heaven?
Have you ever wanted to die? Sam blinked his eye twice. but made no reply.
Dad fingered his knife and loosened his tie. As he picked up his son, Sam
dripped on his coat. With the shell to his lips, Sam slipped down his throat.
They burried him quickly in the sand by the sea -sighed a prayer, wept a
tear- and they were back home by three. A cross of greay driftwood marked
Oyster Boy's grave. Words writ in the sand promised Jesus would save. But his
memory was lost with one high-tide wave."""

correctLongText = test()(text_to_lines
                        .call(testT9, max_lengthT9)
                        .returns(correctOutputT9)
                        .description("Function works with a long text")
                        )