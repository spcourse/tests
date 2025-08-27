import typing
from checkpy import *

only("weather5.py")
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
def correctFirstHeatWave():
    """prints the first year that had a heatwave"""
    assertNotHardcoded("1911")
    assert "1911" in outputOf(overwriteAttributes=[("__name__", "__main__")])
