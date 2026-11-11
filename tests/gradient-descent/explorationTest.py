from checkpy import *

import re

only("exploration.py")
download("yearly_avg_temp.csv", "https://github.com/spcourse/gradient-descent/raw/main/read-data/yearly_avg_temp.csv")
monkeypatch.patchMatplotlib()

import matplotlib.pyplot as plt

MSE_LINE = re.compile(r"MSE for w=\s*(-?[\d.]+),\s*b=\s*(-?[\d.]+):\s*(-?[\d.]+)")
FITS = [(0.022, -29.0, "0.9007"), (0.01, -6.0, "0.6523")]


def readData():
    years, txs, tns = [], [], []
    with open("yearly_avg_temp.csv") as f:
        f.readline()
        for line in f:
            year, tn, tx = line.split(",")
            years.append(int(year))
            tns.append(float(tn))
            txs.append(float(tx))
    return years, tns, txs


def mseFor(w, b):
    years, _, txs = readData()
    return sum((w * x + b - y) ** 2 for x, y in zip(years, txs)) / len(years)


def numbersIn(text):
    return [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", text)]


def allAxes():
    """Run the student's file and return every axes it drew on."""
    getModule()
    return [ax for num in plt.get_fignums() for ax in plt.figure(num).axes]


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(b))


def linesFollowing(axes, w, b):
    found = []
    for ax in axes:
        for line in ax.get_lines():
            xs = [float(x) for x in line.get_xdata()]
            ys = [float(y) for y in line.get_ydata()]
            if len(xs) >= 2 and all(close(y, w * x + b) for x, y in zip(xs, ys)):
                found.append(line)
    return found


@test(timeout=30)
def showsGraph():
    """the program shows the graph or saves it to a file"""
    calls = static.getFunctionCalls()
    assert any(c.endswith("show") or c.endswith("savefig") for c in calls), (
        "Show the graph with plt.show(), or save it with plt.savefig()."
    )


@passed(showsGraph, timeout=30, hide=False)
def scatterOfData():
    """the average maximum temperature is drawn as a scatter plot over the years"""
    years, tns, txs = readData()
    point_sets = [
        sorted((float(x), float(y)) for x, y in c.get_offsets())
        for ax in allAxes() for c in ax.collections
    ]
    assert point_sets, "No scatter plot found. Use plt.scatter() for the data points."

    for pts in point_sets:
        if pts == sorted(zip(years, txs)):
            return
        if pts == sorted(zip(years, tns)):
            raise AssertionError(
                "The scatter plot shows the average minimum temperature (avg_TN).\n"
                "Plot the average maximum temperature (avg_TX) instead."
            )
    raise AssertionError(
        "The scatter plot does not show avg_TX against the year.\n"
        f"Expected {len(years)} points, one per year from {years[0]} to {years[-1]}."
    )


@passed(showsGraph, timeout=30, hide=False)
def labelsAndTitle():
    """the axes are labelled and the plot has a title"""
    axes = allAxes()
    assert any("year" in ax.get_xlabel().lower() for ax in axes), (
        "Label the x-axis 'Year' with plt.xlabel()."
    )
    assert any("temp" in ax.get_ylabel().lower() for ax in axes), (
        "Label the y-axis 'Average max temperature (°C)' with plt.ylabel()."
    )
    assert any(ax.get_title().strip() for ax in axes), "Give the plot a title with plt.title()."


test_apply_affine = test()(declarative
    .function("apply_affine")
    .params("xs", "w", "b")
    .returnType(list)
    .call([0.0, 1.0, -2.0], 2.0, 1.0)
    .returns([1.0, 3.0, -3.0])
    .description("apply_affine is copied in and works")
)

test_mse = test()(declarative
    .function("mse")
    .params("predictions", "targets")
    .returnType(float)
    .call([1.0, 2.0, 3.0, 4.0], [2.0, 2.0, 5.0, 1.0])
    .returns(3.5)
    .description("mse is copied in and works")
)


@test(timeout=30)
def firstFit():
    """prints the MSE for w=0.022, b=-29.0 and plots that line"""
    w, b, expected = FITS[0]
    line = f"MSE for w={w}, b={b}: {expected}"
    assert line in outputOf(), f"Expected this line in the output:\n{line}"
    assert linesFollowing(allAxes(), w, b), (
        f"No line found for w={w}, b={b}.\n"
        "Use plt.plot() with the years and the predictions from apply_affine."
    )


@test(timeout=30)
def secondFit():
    """prints the MSE for w=0.01, b=-6.0 and plots that line"""
    w, b, expected = FITS[1]
    line = f"MSE for w={w}, b={b}: {expected}"
    assert line in outputOf(), f"Expected this line in the output:\n{line}"
    assert linesFollowing(allAxes(), w, b), (
        f"No line found for w={w}, b={b}.\n"
        "Use plt.plot() with the years and the predictions from apply_affine."
    )


@passed(firstFit, secondFit, timeout=30, hide=False)
def legend():
    """the legend shows which line belongs to which parameterisation"""
    legends = [ax.get_legend() for ax in allAxes()]
    texts = [t.get_text() for lg in legends if lg is not None for t in lg.get_texts()]
    assert texts, (
        "No legend found. Give each line a label=... and call plt.legend()."
    )
    for w, b, _ in FITS:
        assert any(w in numbersIn(t) and b in numbersIn(t) for t in texts), (
            f"The legend should make clear which line has w={w}, b={b}.\n"
            "Put both values in that line's label."
        )


@passed(firstFit, secondFit, timeout=30, hide=False)
def betterFit():
    """finds a better fit: prints its MSE and plots its line"""
    given = [(w, b) for w, b, _ in FITS]
    own = [
        (float(w), float(b), float(m))
        for w, b, m in MSE_LINE.findall(outputOf())
        if (float(w), float(b)) not in given
    ]
    assert own, (
        "Try your own w and b, and print its MSE in the same format:\n"
        "MSE for w=..., b=...: ..."
    )

    best = min(own, key=lambda fit: fit[2])
    w, b, printed = best
    assert close(printed, mseFor(w, b), tol=1e-3), (
        f"You printed an MSE of {printed} for w={w}, b={b}, "
        f"but that line has an MSE of {mseFor(w, b):.4f}."
    )
    assert printed < 0.6523, (
        f"Your best fit (w={w}, b={b}) has an MSE of {printed}, "
        "which is not lower than 0.6523. Keep trying!"
    )
    assert linesFollowing(allAxes(), w, b), (
        f"Also add the line for w={w}, b={b} to the plot."
    )
