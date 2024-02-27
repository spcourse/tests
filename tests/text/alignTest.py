from checkpy import *

import ast

only("align.py")

@test()
def noBreakAndImport():
    """the program does not use break or import statements"""
    assert ast.Import not in static.AbstractSyntaxTree(), "you cannot use import statements"
    assert ast.Break not in static.AbstractSyntaxTree(), "you cannot use break statements"

correct_def_right_align = test()(declarative
                 .function("right_align")
                 .params("text")
                 .returnType(str)
                 .description("correctly defines the text_to_lines() function")
                 )

text_to_lines = (declarative.function("right_align"))

@passed(correct_def_right_align, hide=False)
def test2():
    """function gets padding for short text right (ignoring trailing whitespace)"""
    _input = "This text is left aligned.\nLets change that."
    _expected = "This text is left aligned.\n         Lets change that."
    state = text_to_lines.call(_input)()
    _actual = state.returned.rstrip()
    assert _expected == _actual


@passed(correct_def_right_align, hide=False)
def test3():
    """function gets padding for long text right (ignoring trailing whitespace)"""
    _input = "ASDF is the sequence of letters that appear\non the first four keys on the home row of\na QWERTY or QWERTZ keyboard. They are often used\nas a sample or test case or as random, meaningless\nnonsense. It is also a common learning tool\nfor keyboard classes, since all four keys are\nlocated on Home row."
    _expected = "       ASDF is the sequence of letters that appear\n         on the first four keys on the home row of\n  a QWERTY or QWERTZ keyboard. They are often used\nas a sample or test case or as random, meaningless\n       nonsense. It is also a common learning tool\n     for keyboard classes, since all four keys are\n                              located on Home row."
    state = text_to_lines.call(_input)()
    _actual = state.returned.rstrip()
    assert _expected == _actual


@passed(test2, hide=False)
def test4():
    """function gets padding for short text right inlcuding trailing whitespace"""
    _input = "This text is left aligned.\nLets change that."
    _expected = "This text is left aligned.\n         Lets change that."
    state = text_to_lines.call(_input)()
    _actual = state.returned
    assert _expected == _actual


@passed(test3, hide=False)
def test5():
    """function gets padding for long text right inlcuding trailing whitespace"""
    _input = "ASDF is the sequence of letters that appear\non the first four keys on the home row of\na QWERTY or QWERTZ keyboard. They are often used\nas a sample or test case or as random, meaningless\nnonsense. It is also a common learning tool\nfor keyboard classes, since all four keys are\nlocated on Home row."
    _expected = "       ASDF is the sequence of letters that appear\n         on the first four keys on the home row of\n  a QWERTY or QWERTZ keyboard. They are often used\nas a sample or test case or as random, meaningless\n       nonsense. It is also a common learning tool\n     for keyboard classes, since all four keys are\n                              located on Home row."
    state = text_to_lines.call(_input)()
    _actual = state.returned
    assert _expected == _actual
