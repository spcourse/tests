# Test once again test if the function is in the code with the right amount of
# arguments and right type of return, but only gives a mesage at test 0.

from checkpy import *

only("reformatting.py")

testText = """He proposed in the dunes, they were wed by the sea, Their nine-day-long honeymoon was on the isle of Capri. For their supper they had one specatular dish- a simmering stew of mollusks and fish. And while he savored the broth, her bride's heart made a wish. That wish came true-she gave birth to a baby. But was this little one human Well, maybe. Ten fingers, ten toes, he had plumbing and sight. He could hear, he could feel, but normal? Not quite. This unnatural birth, this canker, this blight, was the start and the end and the sum of their plight. She railed at the doctor: "He cannot be mine. He smells of the ocean, of seaweed and brine." "You should count yourself lucky, for only last week, I treated a girl with three ears and a beak. That your son is half oyster you cannot blame me. ... have you ever considered, by chance, a small home by the sea?" Not knowing what to name him, they just called him Sam, or sometimes, "that thing that looks like a clam" Everyone wondered, but no one could tell, When would young Oyster Boy come out of his shell? When the Thompson quadruplets espied him one day, they called him a bivalve and ran quickly away. One spring afternoon, Sam was left in the rain. At the southwestern corner of Seaview and Main, he watched the rain water as it swirled down the drain. His mom on the freeway in the breakdown lane was pouding the dashboard- she couldn't contain the ever-rising grief, frustration, and pain. "Really, sweetheart," she said "I don't mean to make fun, but something smells fishy and I think it's our son. I don't like to say this, but it must be said, you're blaming our son for your problems in bed." He tried salves, he tried ointments that turned everything red. He tried potions and lotions and tincture of lead. He ached and he itched and he twitched and he bled. The doctor diagnosed, "I can't quite be sure, but the cause of the problem may also be the cure. They say oysters improve your sexual powers. Perhaps eating your son would help you do it for hours!" He came on tiptoe, he came on the sly, sweat on his forehead, and on his lips-a lie. "Son, are you happy? I don't mean to pry, but do you dream of Heaven? Have you ever wanted to die? Sam blinked his eye twice. but made no reply. Dad fingered his knife and loosened his tie. As he picked up his son, Sam dripped on his coat. With the shell to his lips, Sam slipped down his throat. They burried him quickly in the sand by the sea -sighed a prayer, wept a tear- and they were back home by three. A cross of greay driftwood marked Oyster Boy's grave. Words writ in the sand promised Jesus would save. But his memory was lost with one high-tide wave."""

def getReformattedText(text, maxLength):
    result = ""
    counter = 0
    for word in text.split():
        if result == "":
            result = word
            counter += len(word)
        elif len(word) + counter < maxLength:
            result += " " + word
            counter += len(word) + 1
        else:
            result += "\n" + word
            counter = len(word)
    return result


@test()
def correctReformatting():
    """A given text is reformatted correctly."""
    text_to_lines = (declarative
        .function("text_to_lines")
        .params("text", "max_length")
        .returnType(str)
    )().function

    actual = text_to_lines(testText, 77)
    expected = getReformattedText(testText, 77)

    assert actual == expected, f'testing with text:\n"{testText}'
