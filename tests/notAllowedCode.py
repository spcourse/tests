from typing import Dict

from checkpy.tester import getActiveTest
from checkpy.lib import source, removeComments


def _notAllowedCode(notAllowed: Dict[str, str]):
    src = removeComments(source())

    abc = []

    for element in notAllowed:
        if notAllowed[element] in src:
            abc.append(element)

    if len(abc) > 0:
        warning = "however, make sure you do not use " + ", ".join(abc) + " for solving this problem!"
        test = getActiveTest()
        test.fail = test.success = warning


# TODO: rm me, only exists for backward compatibility
def notAllowedCode(*args):
    if len(args) == 1:
        return _notAllowedCode(args[0])
    return _notAllowedCode(args[2])