import typing
from checkpy import *

only("temperature.py")
download("DeBiltTempMaxOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMaxOLD.txt")
download("DeBiltTempMinOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLD.txt")
download("DeBiltTempMaxOLDSmall.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLDSmall.txt")
download("DeBiltTempMinOLDSmall.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLDSmall.txt")

monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

def findLineWith(text: str, value: str) -> typing.Optional[str]:
    for line in text.split("\n"):
        if value in line:
            return line
    return None

def assertNotHardcoded(answer: str):
    assert answer not in static.removeComments(static.getSource()),\
        f"Hmmm, {answer} appears to be hardcoded!"

fun_read_def = (
    declarative
    .function("read_data")
    .params("filename")
    .description("read_data() is correctly defined")
)

test_read_def = test()(fun_read_def)

@passed(test_read_def, hide=False)
def testReadDataReturnsTwoLists():
    """read_data returns (dates, temps) as two lists of equal length"""

    f = getFunction("read_data")

    assert isinstance(f("DeBiltTempMaxOLDSmall.txt"), tuple), \
        "read_data should return a tuple containing two lists: (dates, temps)."

    dates, temps = f("DeBiltTempMaxOLDSmall.txt")

    assert isinstance(dates, list) and isinstance(temps, list), \
        "read_data should return a tuple containing two lists: (dates, temps)."

    assert len(dates) == len(temps), \
        "dates and temps should have the same length."

    assert len(dates) > 0, \
        "dates and temps should not be empty."

@passed(test_read_def, hide=False)
def testReadDataUsesFilename_small_files():
    """read_data uses the given filename"""

    f = getFunction("read_data")

    max_dates, max_temps = f("DeBiltTempMaxOLDSmall.txt")
    min_dates, min_temps = f("DeBiltTempMinOLDSmall.txt")

    # The small files contain exactly 3 data lines
    assert len(max_dates) == 3 and len(max_temps) == 3, (
        "After testing your function with a datafile containing three lines, we get back a different length \n"
        "You may be ignoring the filename argument or reading a fixed/absolute path."
    )

    assert len(min_dates) == 3 and len(min_temps) == 3, (
        "After testing your function with a datafile containing three lines, we get back a different length \n"
        "You may be ignoring the filename argument or reading a fixed/absolute path."
    )


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


@test()
def correctFirstHeatWave():
    """prints the first year that had a heatwave"""
    assertNotHardcoded("1911")
    assert "1911" in outputOf(overwriteAttributes=[("__name__", "__main__")])


@test()
def showsGraph():
    """either saves a graph into a file, or shows a graph on the screen"""
    assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls()
