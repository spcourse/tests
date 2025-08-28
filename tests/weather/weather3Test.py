import typing
from checkpy import *

only("weather3.py")
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
def correctLongestFreezing():
    """prints the longest period of frost (in days)"""
    assertNotHardcoded("21")
    assert "21" in outputOf(overwriteAttributes=[("__name__", "__main__")])


@passed(correctLongestFreezing, hide=False)
def correctDateLongestFreezingp():
    """prints the last day of the longest freezing period"""
    assertNotHardcoded("1947")

    output = outputOf(overwriteAttributes=[("__name__", "__main__")])
    line = findLineWith(output, "21")

    assert "24" in line, "incorrect day"
    assert "februari" in line.lower() or "february" in line.lower() or "feb" in line.lower(), "incorrect month"
    assert "1947" in line, "incorrect year"
