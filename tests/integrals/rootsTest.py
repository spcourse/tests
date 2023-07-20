from checkpy import *

only("roots.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def hasNulpunten():
    """defines the function roots()"""
    assert "roots" in static.getFunctionDefinitions()

@passed(hasNulpunten, hide=False)
def returnTypeIsList():
    """roots() returns a list"""
    assert type(getFunction("roots")(1, 2, -10)) is list

@passed(returnTypeIsList, hide=False)
def correct():
    """roots() yields the two correct roots for a=1, b=2, c=-10"""
    assert sorted(int(p * 10) / 10 for p in getFunction("roots")(1, 2, -10)) == [-4.3, 2.3]

@passed(returnTypeIsList, hide=False)
def correctNone():
    """roots() yields no roots for a=3, b=6, c=9"""
    assert getFunction("roots")(3, 6, 9) == []
