import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

def notAllowedCode(test, source, notAllowed):
# source = lib.source(_fileName)
    source_no_comments = lib.removeComments(source)

    abc = []

    for element in notAllowed:
        if notAllowed[element] in source_no_comments:
            abc.append(element)


    if len(abc) > 0:
        warning = "however, make sure you do not use " + ", ".join(abc) + " for solving this problem!"
        test.fail = lambda info : warning
        test.success = lambda info : warning
