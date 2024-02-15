from checkpy import outputOf
from checkpy.entities.exception import InputError


def outputOfExactStdin(args):
    try:
        # test with one fewer args
        output = outputOf(stdinArgs=args[:-1])
    except InputError as e:
        # if to few args: test with all the args
        return outputOf(stdinArgs=args)
    assert False, "expected the program to ask more user input"
