from checkpy import *

import ast

only("read_data.py")
download("yearly_avg_temp.csv", "https://github.com/spcourse/gradient-descent/raw/main/read-data/yearly_avg_temp.csv")


@test()
def noMinMax():
    """the program finds the extremes without min() or max()"""
    calls = [
        node.func.id
        for node in static.getAstNodes(ast.Call)
        if isinstance(node.func, ast.Name)
    ]
    used = sorted({name for name in calls if name in ("min", "max")})
    assert not used, (
        f"You're using {', '.join(n + '()' for n in used)}.\n"
        "Find the coldest and warmest year with a for loop instead."
    )


@test(timeout=30)
def listsExist():
    """the lists years, avg_tns and avg_txs are defined"""
    module = getModule()
    for name in ("years", "avg_tns", "avg_txs"):
        assert hasattr(module, name), f"The list '{name}' should be defined in your code."
        assert isinstance(getattr(module, name), list), f"'{name}' should be a list."


@passed(listsExist, hide=False)
def listsContent():
    """the lists contain every row of the file, with the right types"""
    module = getModule()
    for name, kind, first, last in [
        ("years", int, 1901, 2025),
        ("avg_tns", float, 4.58, 6.68),
        ("avg_txs", float, 12.85, 15.78),
    ]:
        values = getattr(module, name)
        assert len(values) == 125, (
            f"'{name}' should have 125 values, one per year from 1901 to 2025, but it has {len(values)}.\n"
            + ("Did you skip the header line?" if len(values) == 126 else "")
        )
        assert all(type(v) is kind for v in values), (
            f"Every value in '{name}' should be a{'n' if kind is int else ''} {kind.__name__}."
        )
        assert values[0] == first and values[-1] == last, (
            f"'{name}' should start with {first} and end with {last}, "
            f"but it starts with {values[0]} and ends with {values[-1]}."
        )


@test(timeout=30)
def extremesMin():
    """prints the coldest and warmest year for the average minimum temperature"""
    output = outputOf()
    for line in [
        "Coldest year (avg min temp): 1929 (3.63°C)",
        "Warmest year (avg min temp): 2024 (7.71°C)",
    ]:
        assert line in output, f"Expected this line in the output:\n{line}"


@test(timeout=30)
def extremesMax():
    """prints the coldest and warmest year for the average maximum temperature"""
    output = outputOf()
    for line in [
        "Coldest year (avg max temp): 1963 (11.70°C)",
        "Warmest year (avg max temp): 2022 (15.96°C)",
    ]:
        assert line in output, f"Expected this line in the output:\n{line}"
