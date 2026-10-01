import numpy as np
import pandas as pd

from checkpy import *

only("xkcd.py")

RAW = "https://github.com/spcourse/pandas/raw/main"
download("animals.tsv", f"{RAW}/xkcd1/data/animals.tsv")
download("stars.csv", f"{RAW}/xkcd2/data/stars.csv")
download("star-names.csv", f"{RAW}/xkcd2/data/star-names.csv")
download("particles.txt", f"{RAW}/xkcd3/data/particles.txt")

# checkpy has no plotly equivalent of patchMatplotlib(), so neutralize show() the same
# way patchMatplotlib() does. Without this, importing the student's module opens a
# browser tab per test run.
try:
    import plotly.basedatatypes
    import plotly.io
    monkeypatch.neutralizeFunction(plotly.io.show)
    monkeypatch.neutralizeFunction(plotly.basedatatypes.BaseFigure.show)
except ImportError:
    pass

# Bind values to a local before asserting on them. checkpy runs the rewritten
# assertion through re.sub as a replacement, so any DataFrame or Series *inside*
# the assert expression breaks the whole run with "invalid group reference".

# ---------------------------------------------------------------- step 1: animals
# Everything below hangs off hasAnageReader, so a student who has not written
# read_anage_data() yet sees one message instead of a wall of failures. The later
# steps get their own gate in the same shape.

ANAGE_COLUMNS = {"name", "mass_kg", "lifespan_yr", "category"}
ANAGE_ROWS = 136

# One species per planted notation in "Adult weight (g)", in kilograms.
BLUE_WHALE = 136000.0        # "136M"
BLACK_TREE_KANGAROO = 8.0    # "8k"
AMUR_STURGEON = 104.5        # "104,500"
HUMAN_MASS, HUMAN_LIFE = 62.035, 122.5

# Names that arrive with stray spaces around them.
ANAGE_PADDED = ["American eel", "Least shrew", "Moustached warbler", "Great white shark"]

ANAGE_MASS_RANGE = (0.0005, 136000.0)
ANAGE_LIFE_RANGE = (2.7, 211.0)

_cache = {}


def studentFunction(name):
    """getFunction, but a crash further down the script does not hide earlier steps.

    The script runs top to bottom on import, so an exception in the star section would
    otherwise take the animal tests down with it and report them as "not found"."""
    return getFunction(name, ignoreExceptions=(Exception,))


def anageResult():
    """The student's cleaned animal data. Imports the module once, not once per test."""
    if "anage" not in _cache:
        _cache["anage"] = studentFunction("read_anage_data")()
    return _cache["anage"]


@test()
def hasAnageReader():
    """Animals: read_anage_data() exists"""
    studentFunction("read_anage_data")


@passed(hasAnageReader)
def anageReturnsADataFrame():
    """Animals: read_anage_data() returns a DataFrame with the four expected columns"""
    df = anageResult()
    kind = type(df).__name__
    columns = set(df.columns) if kind == "DataFrame" else set()
    assert kind == "DataFrame", f"read_anage_data() returns a {kind}"
    assert columns == ANAGE_COLUMNS, \
        f"expected the columns {sorted(ANAGE_COLUMNS)}, got {sorted(columns)}"


@passed(hasAnageReader)
def anageHasTheRightTypes():
    """Animals: text for name and category, numbers for the rest"""
    df = anageResult()
    isText = {c: bool(pd.api.types.is_string_dtype(df[c])) for c in ["name", "category"]}
    isNumber = {c: bool(pd.api.types.is_float_dtype(df[c]))
                for c in ["mass_kg", "lifespan_yr"]}
    assert all(isText.values()), f"name and category should be text: {isText}"
    assert all(isNumber.values()), \
        f"mass_kg and lifespan_yr should be floating point numbers: {isNumber}"


@passed(hasAnageReader)
def anageParsedTheAbbreviatedWeights():
    """Animals: the abbreviated weights are read as numbers, not thrown away"""
    df = anageResult()
    masses = dict(zip(df["name"], df["mass_kg"]))
    got = {name: masses.get(name) for name in
           ["Blue whale", "Black tree kangaroo", "Amur sturgeon"]}
    missing = [name for name, value in got.items() if value is None]
    assert not missing, (
        f"{missing} disappeared. The weight column mixes notations -- 136M, 8k and "
        "104,500 all mean grams. to_numeric turns each of them into NaN unless you "
        "convert the text first"
    )
    assert got["Blue whale"] == approx(BLUE_WHALE), \
        f"'136M' is 136 million grams, so 136000 kg, not {got['Blue whale']}"
    assert got["Black tree kangaroo"] == approx(BLACK_TREE_KANGAROO), \
        f"'8k' is 8000 grams, so 8 kg, not {got['Black tree kangaroo']}"
    assert got["Amur sturgeon"] == approx(AMUR_STURGEON), \
        f"'104,500' is 104500 grams, so 104.5 kg, not {got['Amur sturgeon']}"


@passed(hasAnageReader)
def anageConvertedGramsToKilograms():
    """Animals: mass_kg is in kilograms, and lifespan_yr in years"""
    df = anageResult()
    row = df[df["name"] == "Human"]
    mass = float(row["mass_kg"].iloc[0]) if len(row) else None
    life = float(row["lifespan_yr"].iloc[0]) if len(row) else None
    assert mass is not None, "no row for Human"
    assert mass == approx(HUMAN_MASS), \
        f"a human is about 62 kg, not {mass} -- the file gives the weight in grams"
    assert life == approx(HUMAN_LIFE), f"expected {HUMAN_LIFE} years, got {life}"


@passed(hasAnageReader)
def anageStrippedTheNames():
    """Animals: names have no stray spaces around them"""
    df = anageResult()
    names = [str(n) for n in df["name"]]
    untrimmed = [n for n in names if n != n.strip()]
    missing = [n for n in ANAGE_PADDED if n not in names]
    assert not untrimmed, f"these names still carry spaces: {untrimmed[:5]}"
    assert not missing, (
        f"{missing} not found. In the file these names have spaces around them, so "
        "either they were not trimmed, or they were dropped somewhere earlier on"
    )


# There is deliberately no test for removing the non-animals. AnAge carries four plants,
# a fungus and a bacterium, and noticing them is a real validation step -- but none of
# them has an adult weight, so they are dropped by any NaN filter whether the student
# looked at Kingdom or not. A test for it passes no matter what, which is worse than no
# test at all. Raise it in the discussion instead. See CONCEPT-MAP.md.


@passed(hasAnageReader)
def anageHasNoMissingValues():
    """Animals: there are no missing values left"""
    df = anageResult()
    perColumn = {c: int(df[c].isna().sum()) for c in df.columns}
    total = sum(perColumn.values())
    assert total == 0, (
        f"{total} missing values: {perColumn}. A NaN does not raise on a log axis, "
        "it simply is not drawn -- the plot will look fine and be wrong"
    )


@passed(hasAnageReader)
def anageHasNoDuplicates():
    """Animals: each species appears once"""
    df = anageResult()
    extras = int(df["name"].duplicated().sum())
    repeated = sorted(set(str(n) for n in df["name"][df["name"].duplicated()]))
    assert extras == 0, \
        f"{extras} rows appear more than once: {repeated[:5]}"


# Dormant in step 1 on purpose: the animal data contains no zero or negative values, so
# this cannot fail yet. It is the guard for step 3, where the PDG's four stable particles
# have a width of exactly 0 and a lifetime of infinity.
@passed(hasAnageReader)
def anageHasOnlyPositiveValues():
    """Animals: nothing that a log axis cannot draw"""
    df = anageResult()
    badMass = int((df["mass_kg"] <= 0).sum())
    badLife = int((df["lifespan_yr"] <= 0).sum())
    assert badMass == 0 and badLife == 0, (
        f"{badMass} masses and {badLife} lifespans are zero or negative. "
        "log10(0) is minus infinity, so those points vanish from the plot silently"
    )


@passed(hasAnageReader)
def anageSetTheCategory():
    """Animals: every row is labelled as an animal"""
    df = anageResult()
    values = sorted(set(str(c) for c in df["category"]))
    assert values == ["animal"], \
        f'category should be "animal" for every row, found {values}'


@passed(hasAnageReader)
def anageHasAllTheRows():
    """Animals: no rows lost, and none kept that should have gone"""
    df = anageResult()
    rows = len(df)
    massRange = (float(df["mass_kg"].min()), float(df["mass_kg"].max()))
    lifeRange = (float(df["lifespan_yr"].min()), float(df["lifespan_yr"].max()))
    assert rows == ANAGE_ROWS, (
        f"expected {ANAGE_ROWS} rows, got {rows}. Too few usually means a parsing step "
        "quietly turned values into NaN; too many means something was not filtered out"
    )
    assert massRange == approx(ANAGE_MASS_RANGE), \
        f"mass_kg runs {massRange}, expected {ANAGE_MASS_RANGE}"
    assert lifeRange == approx(ANAGE_LIFE_RANGE), \
        f"lifespan_yr runs {lifeRange}, expected {ANAGE_LIFE_RANGE}"


# ---------------------------------------------------------------- step 2: stars

# 19 of the 34 stars in the file. The other 15 have left the main sequence and must be
# filtered out -- "lifespan" means something else for a giant.
STAR_ROWS = 19

# The Sun anchors the formula: one solar mass, ten billion years, by definition.
SUN_MASS, SUN_LIFE = 1.989e30, 1e10
SIRIUS_MASS, SIRIUS_LIFE = 4.09734e30, 1.64184e9
BELLATRIX_LIFE = 4.61056e7

# Giants and supergiants, in the file but not on the plot.
STAR_EVOLVED = ["Betelgeuse", "Rigel", "Alnilam", "Aldebaran", "Pollux", "Capella",
                "Arcturus", "Antares", "Deneb", "Polaris"]

# Stars with no common name, known by their designation instead.
STAR_FALLBACK = ["Wolf 359", "Tau Ceti", "Lalande 21185", "Barnard's Star",
                 "61 Cygni A", "Groombridge 34 A", "Kapteyn's Star", "Lacaille 9352"]

# Their designations carry a stray space in star-names.csv, so a merge on the raw key
# misses them and they fall back to the designation instead of the common name.
STAR_TRICKY_NAMES = ["Altair", "Fomalhaut"]

STAR_MASS_RANGE = (1.7901e29, 1.71054e31)
STAR_LIFE_RANGE = (46105620.57, 4115226337448.56)


def starResult():
    """The student's cleaned star data."""
    if "stars" not in _cache:
        _cache["stars"] = studentFunction("read_star_data")()
    return _cache["stars"]


@test()
def hasStarReader():
    """Stars: read_star_data() exists"""
    studentFunction("read_star_data")


@passed(hasStarReader)
def starsReturnADataFrame():
    """Stars: read_star_data() returns a DataFrame with the same four columns"""
    df = starResult()
    kind = type(df).__name__
    columns = set(df.columns) if kind == "DataFrame" else set()
    assert kind == "DataFrame", f"read_star_data() returns a {kind}"
    assert columns == ANAGE_COLUMNS, \
        f"expected the columns {sorted(ANAGE_COLUMNS)}, got {sorted(columns)}"


@passed(hasStarReader)
def starsHaveTheRightTypes():
    """Stars: the columns have the same types as the animal ones"""
    df = starResult()
    isText = {c: bool(pd.api.types.is_string_dtype(df[c])) for c in ["name", "category"]}
    isNumber = {c: bool(pd.api.types.is_float_dtype(df[c]))
                for c in ["mass_kg", "lifespan_yr"]}
    assert all(isText.values()), f"name and category should be text: {isText}"
    assert all(isNumber.values()), \
        f"mass_kg and lifespan_yr should be floating point numbers: {isNumber}"


@passed(hasStarReader)
def starsConvertedTheMasses():
    """Stars: the masses are read correctly and converted to kilograms"""
    df = starResult()
    masses = dict(zip(df["name"], df["mass_kg"]))
    sun = masses.get("Sun")
    assert sun is not None, "no row for the Sun"
    assert sun == approx(SUN_MASS, rel=1e-3), (
        f"the Sun should weigh {SUN_MASS:.4g} kg, got {sun}. The file gives mass in "
        "solar masses -- and it writes numbers with a comma, not a point"
    )
    sirius = masses.get("Sirius")
    assert sirius == approx(SIRIUS_MASS, rel=1e-3), \
        f"Sirius should weigh {SIRIUS_MASS:.4g} kg, got {sirius}"


@passed(hasStarReader)
def starsComputedTheLifespan():
    """Stars: the lifespans are computed from the masses"""
    df = starResult()
    lives = dict(zip(df["name"], df["lifespan_yr"]))
    sun = lives.get("Sun")
    assert sun == approx(SUN_LIFE, rel=1e-3), (
        f"the Sun should live {SUN_LIFE:.4g} years, got {sun}. No file gives a lifespan "
        "-- it is calculated from the mass"
    )
    sirius = lives.get("Sirius")
    bellatrix = lives.get("Bellatrix")
    assert sirius == approx(SIRIUS_LIFE, rel=1e-3), \
        f"Sirius should live {SIRIUS_LIFE:.4g} years, got {sirius}"
    assert bellatrix == approx(BELLATRIX_LIFE, rel=1e-3), (
        f"Bellatrix should live {BELLATRIX_LIFE:.4g} years, got {bellatrix}. Heavier "
        "stars burn out sooner, so the exponent is negative"
    )


@passed(hasStarReader)
def starsKeptTheUnnamedOnes():
    """Stars: those without a common name are kept, under their designation"""
    df = starResult()
    names = set(str(n) for n in df["name"])
    missing = [n for n in STAR_FALLBACK if n not in names]
    assert not missing, (
        f"{missing} missing. Not every star has a common name, and one that does not "
        "is still a star -- an inner join drops it and says nothing"
    )


@passed(hasStarReader)
def starsUsedTheCommonNames():
    """Stars: those with a common name are listed under it, not their designation"""
    df = starResult()
    names = set(str(n) for n in df["name"])
    missing = [n for n in STAR_TRICKY_NAMES if n not in names]
    assert not missing, (
        f"{missing} missing, so those stars kept their designation instead. The two "
        "files do not write every designation the same way, and a key that does not "
        "match exactly does not match at all"
    )


@passed(hasStarReader)
def starsDroppedTheGiants():
    """Stars: those that have left the main sequence are not on the plot"""
    df = starResult()
    names = set(str(n) for n in df["name"])
    found = [n for n in STAR_EVOLVED if n in names]
    assert not found, (
        f"{found} should not be here. Those stars have left the main sequence, and a "
        "giant's lifespan is not the same quantity as a main-sequence star's -- the "
        "file says which is which"
    )


@passed(hasStarReader)
def starsHaveNoMissingValues():
    """Stars: there are no missing values left"""
    df = starResult()
    perColumn = {c: int(df[c].isna().sum()) for c in df.columns}
    total = sum(perColumn.values())
    assert total == 0, (
        f"{total} missing values: {perColumn}. A star with no common name still needs "
        "a name"
    )


@passed(hasStarReader)
def starsHaveNoDuplicates():
    """Stars: each star appears once"""
    df = starResult()
    extras = int(df["name"].duplicated().sum())
    repeated = sorted(set(str(n) for n in df["name"][df["name"].duplicated()]))
    assert extras == 0, (
        f"{extras} stars appear more than once: {repeated[:5]}. A merge multiplies rows "
        "when the key is not unique on both sides"
    )


@passed(hasStarReader)
def starsSetTheCategory():
    """Stars: every row is labelled as a star"""
    df = starResult()
    values = sorted(set(str(c) for c in df["category"]))
    assert values == ["star"], \
        f'category should be "star" for every row, found {values}'


@passed(hasStarReader)
def starsHaveAllTheRows():
    """Stars: no stars lost, and none gained"""
    df = starResult()
    rows = len(df)
    massRange = (float(df["mass_kg"].min()), float(df["mass_kg"].max()))
    lifeRange = (float(df["lifespan_yr"].min()), float(df["lifespan_yr"].max()))
    assert rows == STAR_ROWS, (
        f"expected {STAR_ROWS} stars, got {rows}. The file holds 34, of which 15 are "
        "not main sequence. Fewer than expected also happens when the merge drops the "
        "stars with no common name; more when it keeps a name that has no star"
    )
    assert massRange == approx(STAR_MASS_RANGE, rel=1e-3), \
        f"mass_kg runs {massRange}, expected {STAR_MASS_RANGE}"
    assert lifeRange == approx(STAR_LIFE_RANGE, rel=1e-3), \
        f"lifespan_yr runs {lifeRange}, expected {STAR_LIFE_RANGE}"


# ---------------------------------------------------------------- step 3: particles

PDG_ROWS = 135          # 168 rows in the file, minus 29 blank and 4 that never decay

NEUTRON_MASS, NEUTRON_LIFE = 1.674927498e-27, 2.7835951279e-05
PION_PLUS_LIFE, PION_ZERO_LIFE = 8.2492795e-16, 2.6706118e-24

# Width exactly 0 means a particle that does not decay, so hbar/0 is infinity. These
# four must not reach the plot -- and nothing except an explicit check removes them.
PDG_STABLE = ["e-", "p+", "g0", "gamma0"]

PDG_MASS_RANGE = (1.8835316e-28, 3.0763397e-25)
PDG_LIFE_RANGE = (8.3580358e-33, 2.7835951e-05)


def pdgResult():
    """The student's cleaned particle data."""
    if "pdg" not in _cache:
        _cache["pdg"] = studentFunction("read_pdg_data")()
    return _cache["pdg"]


@test()
def hasPdgReader():
    """Particles: read_pdg_data() exists"""
    studentFunction("read_pdg_data")


@passed(hasPdgReader)
def particlesReturnADataFrame():
    """Particles: read_pdg_data() returns a DataFrame with the same four columns"""
    df = pdgResult()
    kind = type(df).__name__
    columns = set(df.columns) if kind == "DataFrame" else set()
    assert kind == "DataFrame", f"read_pdg_data() returns a {kind}"
    assert columns == ANAGE_COLUMNS, \
        f"expected the columns {sorted(ANAGE_COLUMNS)}, got {sorted(columns)}"


@passed(hasPdgReader)
def particlesHaveTheRightTypes():
    """Particles: the columns have the same types as the other two sources"""
    df = pdgResult()
    isText = {c: bool(pd.api.types.is_string_dtype(df[c])) for c in ["name", "category"]}
    isNumber = {c: bool(pd.api.types.is_float_dtype(df[c]))
                for c in ["mass_kg", "lifespan_yr"]}
    assert all(isText.values()), f"name and category should be text: {isText}"
    assert all(isNumber.values()), \
        f"mass_kg and lifespan_yr should be floating point numbers: {isNumber}"


@passed(hasPdgReader)
def particlesUsedNameAndCharge():
    """Particles: the name includes the charge, so the pions can be told apart"""
    df = pdgResult()
    names = set(str(n) for n in df["name"])
    missing = [n for n in ["pi+", "pi0", "n0", "mu-"] if n not in names]
    assert not missing, (
        f"{missing} not found. 22 names in the file are used by more than one row, so "
        "the name on its own does not identify a particle -- the charge belongs with it"
    )


@passed(hasPdgReader)
def particlesConvertedTheMass():
    """Particles: the masses are converted from GeV to kilograms"""
    df = pdgResult()
    masses = dict(zip(df["name"], df["mass_kg"]))
    neutron = masses.get("n0")
    assert neutron is not None, "no row for the neutron"
    assert neutron == approx(NEUTRON_MASS, rel=1e-4), (
        f"the neutron should weigh {NEUTRON_MASS:.4g} kg, got {neutron}. The file gives "
        "mass in GeV; 1 GeV is 1.782661922e-27 kg"
    )


@passed(hasPdgReader)
def particlesComputedTheLifetime():
    """Particles: the lifetimes are worked out from the decay widths"""
    df = pdgResult()
    lives = dict(zip(df["name"], df["lifespan_yr"]))
    neutron = lives.get("n0")
    assert neutron == approx(NEUTRON_LIFE, rel=1e-3), (
        f"the neutron should live {NEUTRON_LIFE:.4g} years -- about 878 seconds -- but "
        f"got {neutron}. lifetime = hbar / width gives seconds, and the plot wants years"
    )
    plus, zero = lives.get("pi+"), lives.get("pi0")
    assert plus == approx(PION_PLUS_LIFE, rel=1e-3), \
        f"pi+ should live {PION_PLUS_LIFE:.4g} years, got {plus}"
    assert zero == approx(PION_ZERO_LIFE, rel=1e-3), \
        f"pi0 should live {PION_ZERO_LIFE:.4g} years, got {zero}"


@passed(hasPdgReader)
def particlesDroppedTheStableOnes():
    """Particles: the ones that never decay are not on the plot"""
    df = pdgResult()
    names = set(str(n) for n in df["name"])
    found = [n for n in PDG_STABLE if n in names]
    assert not found, (
        f"{found} should not be here. Their decay width is exactly 0, because they do "
        "not decay at all, so hbar / width is infinity. That is not a missing value and "
        "it is not negative, so neither dropna nor a positive-values filter removes it. "
        "It reaches the plot and is then silently not drawn, because a log axis cannot "
        "place an infinite value"
    )


@passed(hasPdgReader)
def particlesAreAllFinite():
    """Particles: every value is a real number, not an infinity"""
    df = pdgResult()
    badMass = int((~np.isfinite(df["mass_kg"].to_numpy(dtype="float64"))).sum())
    badLife = int((~np.isfinite(df["lifespan_yr"].to_numpy(dtype="float64"))).sum())
    assert badMass == 0 and badLife == 0, (
        f"{badMass} masses and {badLife} lifespans are infinite. Dividing by a width of "
        "zero does not raise and does not give NaN -- it gives inf, which survives every "
        "ordinary clean-up and then quietly fails to plot"
    )


@passed(hasPdgReader)
def particlesHaveNoMissingValues():
    """Particles: there are no missing values left"""
    df = pdgResult()
    perColumn = {c: int(df[c].isna().sum()) for c in df.columns}
    total = sum(perColumn.values())
    assert total == 0, (
        f"{total} missing values: {perColumn}. 29 rows in the file have no mass or no "
        "width at all"
    )


@passed(hasPdgReader)
def particlesHaveNoDuplicates():
    """Particles: each particle appears once"""
    df = pdgResult()
    extras = int(df["name"].duplicated().sum())
    repeated = sorted(set(str(n) for n in df["name"][df["name"].duplicated()]))
    assert extras == 0, \
        f"{extras} particles appear more than once: {repeated[:5]}"


@passed(hasPdgReader)
def particlesSetTheCategory():
    """Particles: every row is labelled as a particle"""
    df = pdgResult()
    values = sorted(set(str(c) for c in df["category"]))
    assert values == ["particle"], \
        f'category should be "particle" for every row, found {values}'


@passed(hasPdgReader)
def particlesHaveAllTheRows():
    """Particles: no rows lost, and none kept that should have gone"""
    df = pdgResult()
    rows = len(df)
    massRange = (float(df["mass_kg"].min()), float(df["mass_kg"].max()))
    lifeRange = (float(df["lifespan_yr"].min()), float(df["lifespan_yr"].max()))
    assert rows == PDG_ROWS, (
        f"expected {PDG_ROWS} particles, got {rows}. The file holds 168: 29 have no mass "
        "or no width, and 4 more never decay. 137 usually means the four that never "
        "decay were only partly removed"
    )
    assert massRange == approx(PDG_MASS_RANGE, rel=1e-4), \
        f"mass_kg runs {massRange}, expected {PDG_MASS_RANGE}"
    assert lifeRange == approx(PDG_LIFE_RANGE, rel=1e-3), \
        f"lifespan_yr runs {lifeRange}, expected {PDG_LIFE_RANGE}"


# ---------------------------------------------------------------- combining
# These check only that the sources are stacked correctly. Whether the sources themselves
# are right is the job of the tests above, so the expected row count is taken from the
# student's own DataFrames, never from our numbers. A student whose animal data is wrong
# should still be told that their combine_data() works.

@test()
def hasCombineData():
    """Combining: combine_data() exists"""
    studentFunction("combine_data")


@passed(hasCombineData, hasAnageReader, hasStarReader)
def combinesAnimalsAndStars():
    """Combining: the animal and star data are stacked without losing rows"""
    combine = studentFunction("combine_data")
    animals, stars = anageResult(), starResult()

    expected = len(animals) + len(stars)
    before = (len(animals), len(stars))

    combined = combine([animals, stars])
    kind = type(combined).__name__
    rows = len(combined) if kind == "DataFrame" else 0
    columns = set(combined.columns) if kind == "DataFrame" else set()

    assert kind == "DataFrame", f"combine_data() returns a {kind}"
    assert rows == expected, (
        f"combining {before[0]} animals and {before[1]} stars gave {rows} rows, "
        f"expected {expected}. combine_data() should not clean anything up -- each "
        "read_..._data() already delivers correct rows, so nothing needs dropping here"
    )
    assert columns == ANAGE_COLUMNS, \
        f"expected the columns {sorted(ANAGE_COLUMNS)}, got {sorted(columns)}"
    assert (len(animals), len(stars)) == before, \
        "combine_data() changed the DataFrames it was given -- work on a copy"


@passed(hasCombineData, hasAnageReader, hasStarReader)
def combinedKeepsBothCategories():
    """Combining: both categories survive, and can still be told apart"""
    combine = studentFunction("combine_data")
    animals, stars = anageResult(), starResult()
    combined = combine([animals, stars])

    counts = {str(k): int(v) for k, v in combined["category"].value_counts().items()}
    expected = {"animal": len(animals), "star": len(stars)}
    duplicatedIndex = int(combined.index.duplicated().sum())

    assert counts == expected, f"expected {expected} rows per category, got {counts}"
    assert duplicatedIndex == 0, (
        f"{duplicatedIndex} rows share an index value with another row. Stacking keeps "
        "the original row numbers unless you tell it not to"
    )


@passed(hasCombineData, hasAnageReader, hasStarReader, hasPdgReader)
def combinesAllThreeSources():
    """Combining: all three sources stack into one DataFrame"""
    combine = studentFunction("combine_data")
    frames = [anageResult(), starResult(), pdgResult()]
    expected = sum(len(f) for f in frames)

    combined = combine(frames)
    rows = len(combined)
    counts = {str(k): int(v) for k, v in combined["category"].value_counts().items()}
    perSource = {str(f["category"].iloc[0]): len(f) for f in frames}

    assert rows == expected, (
        f"combining {[len(f) for f in frames]} gave {rows} rows, expected {expected}"
    )
    assert counts == perSource, f"expected {perSource} rows per category, got {counts}"


# ---------------------------------------------------------------- all steps

@test()
def showsThePlot():
    """Plot: the script draws the scatter plot"""
    calls = static.getFunctionCalls()
    scatter = any("scatter" in c for c in calls)
    shows = any(c.endswith(".show") for c in calls)
    assert scatter, "no call to px.scatter"
    assert shows, "the figure is never shown -- call fig.show()"
