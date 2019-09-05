import checkpy.lib as lib
import re

def findLineWith(text, value):
    regex = re.compile(".*" + str(value) + ".*", re.DOTALL)
    for line in text.split("\n"):
        if regex.match(line):
            return line
    return None

def isHardcodedIn(value, fileName):
    source = lib.removeComments(lib.source(fileName))
    return bool(findLineWith(source, value))
