from checkpy import *

import sys

# let students import their own earlier files, as `python file.py` would
if "" not in sys.path:
    sys.path.insert(0, "")

only("plot_regression.py", "apply_affine.py", "vec_operations.py", "inner_product.py")
monkeypatch.patchMatplotlib()

import matplotlib.pyplot as plt

SIZES = [30.0, 45.0, 60.0, 75.0, 90.0, 120.0]
ACTUAL = [280000.0, 400000.0, 540000.0, 660000.0, 760000.0, 1020000.0]
W, B = 8000.0, 50000.0


def allAxes():
    """Run the student's file and return every axes it drew on."""
    getModule()
    return [ax for num in plt.get_fignums() for ax in plt.figure(num).axes]


def scatterPoints(ax):
    return [[(float(x), float(y)) for x, y in c.get_offsets()] for c in ax.collections]


def close(a, b):
    return abs(a - b) <= 1e-6 * max(1.0, abs(b))


@test()
def usesApplyAffine():
    """the program uses apply_affine to compute the line"""
    assert "apply_affine" in static.getFunctionCalls(), (
        "Compute the y-values of the line with your apply_affine function.\n"
        "Copy it into plot_regression.py, or import it from apply_affine.py."
    )


@test(timeout=90)
def showsGraph():
    """the program shows the graph or saves it to a file"""
    calls = static.getFunctionCalls()
    assert any(c.endswith("show") or c.endswith("savefig") for c in calls), (
        "Show the graph with plt.show(), or save it with plt.savefig()."
    )


@passed(showsGraph, timeout=90, hide=False)
def scatterOfData():
    """the six apartments are drawn as a scatter plot, prices divided by 1000"""
    point_sets = [pts for ax in allAxes() for pts in scatterPoints(ax)]
    assert point_sets, "No scatter plot found. Use plt.scatter() for the data points."

    wanted = sorted(zip(SIZES, [p / 1000 for p in ACTUAL]))
    undivided = sorted(zip(SIZES, ACTUAL))
    for pts in point_sets:
        if len(pts) != len(wanted):
            continue
        got = sorted(pts)
        if all(close(g[0], w[0]) and close(g[1], w[1]) for g, w in zip(got, wanted)):
            return
        if all(close(g[0], w[0]) and close(g[1], w[1]) for g, w in zip(got, undivided)):
            raise AssertionError(
                "The scatter plot shows the prices in euros.\n"
                "Divide every price by 1000 before plotting it."
            )

    sizes = [len(pts) for pts in point_sets]
    raise AssertionError(
        "The scatter plot does not show the six apartments.\n"
        f"Expected 6 points (size, price / 1000), found scatter plots with {sizes} points."
    )


@passed(showsGraph, timeout=90, hide=False)
def regressionLine():
    """the line f(x) = 8000x + 50000 is drawn, prices divided by 1000"""
    lines = [line for ax in allAxes() for line in ax.get_lines() if len(line.get_xdata()) >= 2]
    assert lines, "No line found. Use plt.plot() to draw the regression line."

    def follows(line, scale):
        xs = [float(x) for x in line.get_xdata()]
        ys = [float(y) for y in line.get_ydata()]
        return all(close(y, (W * x + B) / scale) for x, y in zip(xs, ys))

    for line in lines:
        if follows(line, 1000):
            xs = [float(x) for x in line.get_xdata()]
            assert min(xs) <= min(SIZES) and max(xs) >= max(SIZES), (
                "The line should cover the whole range of the data, "
                f"at least from {min(SIZES):g} to {max(SIZES):g} m².\n"
                f"Your line runs from {min(xs):g} to {max(xs):g}."
            )
            return
    if any(follows(line, 1) for line in lines):
        raise AssertionError(
            "The line shows the prices in euros.\n"
            "Divide every predicted price by 1000 before plotting it."
        )
    raise AssertionError(
        "None of the lines follows f(x) = 8000x + 50000 (divided by 1000).\n"
        "Use apply_affine with w = 8000 and b = 50000."
    )


@passed(showsGraph, timeout=90, hide=False)
def labels():
    """the axes are labelled"""
    axes = allAxes()
    xlabels = [ax.get_xlabel() for ax in axes]
    ylabels = [ax.get_ylabel() for ax in axes]
    assert any("size" in l.lower() for l in xlabels), (
        "Label the x-axis 'Size (m²)' with plt.xlabel()."
    )
    assert any("price" in l.lower() for l in ylabels), (
        "Label the y-axis 'Price (× €1000)' with plt.ylabel()."
    )


@passed(showsGraph, timeout=90, hide=False)
def legend():
    """there is a legend for the data and the line"""
    legends = [ax.get_legend() for ax in allAxes()]
    legends = [lg for lg in legends if lg is not None]
    assert legends, (
        "No legend found. Give the scatter and the line a label=... and call plt.legend()."
    )
    texts = [t.get_text().lower() for lg in legends for t in lg.get_texts()]
    assert any("data" in t for t in texts), "The legend needs an entry 'data' for the scatter plot."
    assert any("8000" in t for t in texts), (
        "The legend needs an entry 'f(x) = 8000x + 50000' for the line."
    )
