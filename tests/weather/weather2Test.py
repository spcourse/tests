import typing
from checkpy import *

only("weather2.py")
download("DeBiltTempMaxOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMaxOLD.txt")
download("DeBiltTempMinOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLD.txt")

def findLineWith(text: str, value: str) -> typing.Optional[str]:
    for line in text.split("\n"):
        if value in line:
            return line
    return None

def assertNotHardcoded(answer: str):
    assert answer not in static.removeComments(static.getSource()),\
        f"Hmmm, {answer} appears to be hardcoded!"


@test()
def correctHighestTemp():
    """prints the highest temperature"""
    assertNotHardcoded("36.8")
    assert "36.8" in outputOf(overwriteAttributes=[("__name__", "__main__")])


@passed(correctHighestTemp, hide=False)
def correctDateHighestTemp():
    """prints the date of the highest temperature"""
    assertNotHardcoded("1947")

    output = outputOf(overwriteAttributes=[("__name__", "__main__")])
    line = findLineWith(output, "36.8")

    assert "27" in line, "incorrect day"
    assert "juni" in line.lower() or "june" in line.lower() or "jun" in line.lower(), "incorrect month"
    assert "1947" in line, "incorrect year"


@test()
def correctLowestTemp():
    """prints the lowest temperature"""
    assertNotHardcoded("-24.8")
    assert "-24.8" in outputOf(overwriteAttributes=[("__name__", "__main__")])


@passed(correctLowestTemp, hide=False)
def correctDateLowestTemp():
    """prints the date of the lowest temperature"""
    assertNotHardcoded("1942")

    output = outputOf(overwriteAttributes=[("__name__", "__main__")])
    line = findLineWith(output, "-24.8")

    assert "27" in line, "incorrect day"
    assert "januari" in line.lower() or "january" in line.lower() or "jan" in line.lower(), "incorrect month"
    assert "1942" in line, "incorrect year"

