import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

# Test once again test if the function is in the code with the right amount of 
# arguments and right type of return, but only gives a mesage at test 0.

test_text = """He proposed in the dunes, they were wed by the sea, Their nine-day-long honeymoon was on the isle of Capri. For their supper they had one specatular dish- a simmering stew of mollusks and fish. And while he savored the broth, her bride's heart made a wish. That wish came true-she gave birth to a baby. But was this little one human Well, maybe. Ten fingers, ten toes, he had plumbing and sight. He could hear, he could feel, but normal? Not quite. This unnatural birth, this canker, this blight, was the start and the end and the sum of their plight. She railed at the doctor: "He cannot be mine. He smells of the ocean, of seaweed and brine." "You should count yourself lucky, for only last week, I treated a girl with three ears and a beak. That your son is half oyster you cannot blame me. ... have you ever considered, by chance, a small home by the sea?" Not knowing what to name him, they just called him Sam, or sometimes, "that thing that looks like a clam" Everyone wondered, but no one could tell, When would young Oyster Boy come out of his shell? When the Thompson quadruplets espied him one day, they called him a bivalve and ran quickly away. One spring afternoon, Sam was left in the rain. At the southwestern corner of Seaview and Main, he watched the rain water as it swirled down the drain. His mom on the freeway in the breakdown lane was pouding the dashboard- she couldn't contain the ever-rising grief, frustration, and pain. "Really, sweetheart," she said "I don't mean to make fun, but something smells fishy and I think it's our son. I don't like to say this, but it must be said, you're blaming our son for your problems in bed." He tried salves, he tried ointments that turned everything red. He tried potions and lotions and tincture of lead. He ached and he itched and he twitched and he bled. The doctor diagnosed, "I can't quite be sure, but the cause of the problem may also be the cure. They say oysters improve your sexual powers. Perhaps eating your son would help you do it for hours!" He came on tiptoe, he came on the sly, sweat on his forehead, and on his lips-a lie. "Son, are you happy? I don't mean to pry, but do you dream of Heaven? Have you ever wanted to die? Sam blinked his eye twice. but made no reply. Dad fingered his knife and loosened his tie. As he picked up his son, Sam dripped on his coat. With the shell to his lips, Sam slipped down his throat. They burried him quickly in the sand by the sea -sighed a prayer, wept a tear- and they were back home by three. A cross of greay driftwood marked Oyster Boy's grave. Words writ in the sand promised Jesus would save. But his memory was lost with one high-tide wave."""


@t.test(0)
def Correctwithspaces(test):
    function_name = "text_to_lines"
    max_length = 77
    
    def testMethod():
        hasfunction = assertlib.fileContainsFunctionDefinitions(_fileName, function_name)
        if not hasfunction:
            info = "Make sure you use a function named " + function_name + " as you're writing your code."
            return False, info
        
        nArguments = len(lib.getFunction(function_name, _fileName).arguments)
        if nArguments != 2:
            info = "Make sure your function has 2 argument."
            return False, info

        correct_return = assertlib.sameType(lib.getFunction(function_name, _fileName)(test_text, max_length), "abc")
        if not correct_return:
            info = "Make sure you return an string and nothing else."
            return False, info


        outputtext = lib.getFunction(function_name, _fileName)(test_text, max_length)

        if "  " in outputtext:
            info = "Make sure there are no double spaces in the reformatted text."
            return False, info
        if " \n" in outputtext or "\n " in outputtext:
            info = "Make sure lines don't start with a white space."
            return False, info

        return True

        
    test.test = testMethod
    test.description = lambda : "Reformatted text has no unexpected white spaces."


@t.test(1)
def Correctreformatting(test):
    max_length = 77
    function_name = "text_to_lines"
    
    def testMethod():
        hasfunction = assertlib.fileContainsFunctionDefinitions(_fileName, function_name)
        if not hasfunction:
            return False
        
        nArguments = len(lib.getFunction(function_name, _fileName).arguments)
        if nArguments != 2:
            return False

        correct_return = assertlib.sameType(lib.getFunction(function_name, _fileName)(test_text, max_length), "abc")
        if not correct_return:
            return False


        reformatted_test_text = ""
        test_text_splitup = test_text.split()

        counter = 0
        for word in test_text_splitup:
            if reformatted_test_text == "":
                reformatted_test_text = word
                counter += len(word)
            if len(word) + counter < max_length:
                reformatted_test_text += " " + word
                counter += len(word) + 1
            else:
                reformatted_test_text += "\n" + word
                counter = len(word)

        outputtext = lib.getFunction(function_name, _fileName)(test_text, max_length)
        return outputtext == reformatted_test_text

        
    test.test = testMethod
    test.description = lambda : "A given text is reformatted correctly."

    