import pandas as pd

from checkpy import *

only("weather-pandas.py")
download("DeBiltTempMaxOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMaxOLD.txt")
download("DeBiltTempMinOLD.txt", "https://github.com/spcourse/bigdata/raw/main/data/DeBiltTempMinOLD.txt")

monkeypatch.patchMatplotlib()

# Bind values to a local before asserting on them. checkpy runs the rewritten
# assertion through re.sub as a replacement, so any DataFrame or Series *inside*
# the assert expression breaks the whole run with "invalid group reference".

MAX_FILE, MIN_FILE = "DeBiltTempMaxOLD.txt", "DeBiltTempMinOLD.txt"

HIGHEST, HIGHEST_DAY = 36.8, pd.Timestamp("1947-06-27")
LOWEST, LOWEST_DAY = -24.8, pd.Timestamp("1942-01-27")
FIRST_DAY, LAST_DAY = pd.Timestamp("1901-01-01"), pd.Timestamp("2015-07-31")

_cache = {}


def student(name):
    """The student's function. Imports the module once, not once per test."""
    if name not in _cache:
        _cache[name] = getFunction(name)
    return _cache[name]


def data(filename):
    """Our own reading, so steps 4 and 5 don't depend on step 1."""
    if filename not in _cache:
        df = pd.read_csv(filename, skiprows=18, skipinitialspace=True)
        df["DATE"] = pd.to_datetime(df["DATE"], format="%Y%m%d")
        df["TEMP"] = df.iloc[:, 3] / 10
        _cache[filename] = df
    return _cache[filename]


def studentData(filename):
    if ("read", filename) not in _cache:
        _cache["read", filename] = student("read_temperatures")(filename)
    return _cache["read", filename]


@test()
def readsTheData():
    """read_temperatures() returns all 41850 days, with TEMP in whole degrees"""
    df = studentData(MAX_FILE)
    kind, rows = type(df).__name__, len(df)
    highest = float(df["TEMP"].max()) if "TEMP" in df.columns else None
    assert kind == "DataFrame"
    assert rows == 41850
    assert highest == approx(HIGHEST), "TEMP in whole degrees, not tenths"


@test()
def parsesTheDates():
    """read_temperatures() turns DATE into real dates"""
    dates = studentData(MAX_FILE)["DATE"]
    isDate = pd.api.types.is_datetime64_any_dtype(dates)
    span = (dates.min(), dates.max())
    assert isDate
    assert span == (FIRST_DAY, LAST_DAY), \
        'everything on 1970-01-01? pd.to_datetime needs format="%Y%m%d"'


@test()
def readsBothFiles():
    """read_temperatures() reads the minimum file just as well"""
    lowest = float(studentData(MIN_FILE)["TEMP"].min())
    assert lowest == approx(LOWEST), \
        "the column is TX in one file and TN in the other, so select it with .iloc"


@test()
def findsTheExtremes():
    """get_highest_temperature() and get_lowest_temperature() return (temperature, date)"""
    for name, df, value, day in [
        ("get_highest_temperature", data(MAX_FILE), HIGHEST, HIGHEST_DAY),
        ("get_lowest_temperature", data(MIN_FILE), LOWEST, LOWEST_DAY),
    ]:
        temperature, date = student(name)(df)
        assert isinstance(temperature, float), f"{name} returns the temperature first"
        assert (temperature, date) == (approx(value), day)


@test()
def printsTheExtremes():
    """the script prints both temperatures with their dates"""
    lines = outputOf(overwriteAttributes=[("__name__", "__main__")]).split("\n")
    for value, day in [(HIGHEST, HIGHEST_DAY), (LOWEST, LOWEST_DAY)]:
        # both on one line: describe() also prints -24.800000
        assert any(str(value) in n and str(day.year) in n for n in lines), \
            f"no line with both {value} and {day.year}"


@test()
def countsPerYear():
    """plot_summer_tropical() returns the counts per year"""
    perYear = student("plot_summer_tropical")(data(MAX_FILE))
    kind, rows = type(perYear).__name__, len(perYear)
    assert kind == "DataFrame"
    assert rows == 115
    years = (int(perYear.index.min()), int(perYear.index.max()))
    summer = int(perYear["is_summer"].sum())
    tropical = int(perYear["is_tropical"].sum())
    assert years == (1901, 2015)
    assert (summer, tropical) == (2478, 360)


@test()
def showsThePlot():
    """the script shows a plot"""
    calls = static.getFunctionCalls()
    assert "plt.show" in calls or "plt.savefig" in calls
