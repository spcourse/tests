from checkpy import *

import re
import sys

# let students import their own earlier files, as `python file.py` would
if "" not in sys.path:
    sys.path.insert(0, "")

only("plot_regression.py", "apply_affine.py", "mse.py", "vec_operations.py", "inner_product.py")
monkeypatch.patchMatplotlib()

import matplotlib.pyplot as plt

SIZES = [30.0, 45.0, 60.0, 75.0, 90.0, 120.0]
ACTUAL = [280000.0, 400000.0, 540000.0, 660000.0, 760000.0, 1020000.0]
W, B = 8000.0, 50000.0
MSE_K = 100.0  # MSE with prices in thousands of euros

# a small case to call plot_regression with directly
T_XS = [1.0, 2.0, 3.0, 4.0]
T_YS = [3.0, 5.0, 8.0, 9.0]
T_W, T_B, T_MSE = 2.0, 1.0, 1.2345


CALL_FIGS = set()  # figures drawn by callAxes, not by the student's own program


def allAxes():
    """Run the student's file and return every axes it drew on."""
    getModule()
    nums = [num for num in plt.get_fignums() if num not in CALL_FIGS]
    return [ax for num in nums for ax in plt.figure(num).axes]


def callAxes():
    """Call plot_regression on the small case, on a fresh figure, and return the axes it drew on."""
    getModule()
    first = plt.figure().number
    getFunction("plot_regression")(T_XS, T_YS, T_W, T_B, T_MSE)
    nums = [num for num in plt.get_fignums() if num >= first]
    CALL_FIGS.update(nums)
    return [ax for num in nums for ax in plt.figure(num).axes]


def scatterPoints(ax):
    return [[(float(x), float(y)) for x, y in c.get_offsets()] for c in ax.collections]


def numbersIn(text):
    return [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", text)]


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(b))


def follows(line, w, b):
    xs = [float(x) for x in line.get_xdata()]
    ys = [float(y) for y in line.get_ydata()]
    return len(xs) >= 2 and all(close(y, w * x + b) for x, y in zip(xs, ys))


def mentions(text, *values):
    nums = numbersIn(text)
    return all(any(close(n, v, 0.01) for n in nums) for v in values)


@test()
def usesApplyAffine():
    """the program uses apply_affine to compute the line"""
    assert "apply_affine" in static.getFunctionCalls(), (
        "Compute the y-values of the line with your apply_affine function.\n"
        "Copy it into plot_regression.py, or import it from apply_affine.py."
    )


@test(timeout=90)
def definesFunction():
    """defines the function plot_regression(xs, ys, w, b, mse_value)"""
    if "plot_regression" not in static.getFunctionDefinitions():
        raise AssertionError("Define a function called plot_regression.")
    n = len(getFunction("plot_regression").arguments)
    assert n == 5, (
        f"plot_regression should take 5 parameters (xs, ys, w, b, mse_value), yours takes {n}."
    )


@passed(definesFunction, timeout=90, hide=False)
def functionScatter():
    """plot_regression draws xs and ys as a scatter plot"""
    point_sets = [pts for ax in callAxes() for pts in scatterPoints(ax)]
    assert point_sets, (
        "Calling plot_regression draws no scatter plot.\n"
        "Use plt.scatter(xs, ys) inside the function."
    )
    if not any(sorted(pts) == sorted(zip(T_XS, T_YS)) for pts in point_sets):
        raise AssertionError(
            f"plot_regression({T_XS}, {T_YS}, {T_W:g}, {T_B:g}, {T_MSE}) does not draw "
            "the points xs and ys.\nDraw the data you get as parameters, not the apartments."
        )


@passed(definesFunction, timeout=90, hide=False)
def functionLine():
    """plot_regression draws the line f(x) = wx + b over the data"""
    axes = callAxes()
    lines = [line for ax in axes for line in ax.get_lines() if follows(line, T_W, T_B)]
    assert lines, (
        f"plot_regression({T_XS}, {T_YS}, {T_W:g}, {T_B:g}, {T_MSE}) does not draw "
        f"the line f(x) = {T_W:g}x + {T_B:g}.\nUse the w and b you get as parameters."
    )
    xs = [float(x) for line in lines for x in line.get_xdata()]
    assert min(xs) <= min(T_XS) and max(xs) >= max(T_XS), (
        "The line should cover the whole range of xs.\n"
        f"For xs = {T_XS} your line runs from {min(xs):g} to {max(xs):g}."
    )


@passed(definesFunction, timeout=90, hide=False)
def functionLegend():
    """plot_regression adds a legend with the data and the model"""
    legends = [ax.get_legend() for ax in callAxes()]
    legends = [lg for lg in legends if lg is not None]
    assert legends, (
        "plot_regression draws no legend.\n"
        "Give the scatter and the line a label=... and call plt.legend() inside the function."
    )
    texts = [t.get_text() for lg in legends for t in lg.get_texts()]
    if not any("data" in t.lower() for t in texts):
        raise AssertionError("The legend needs an entry 'data' for the scatter plot.")
    assert any(mentions(t, T_W, T_B) for t in texts), (
        f"For w = {T_W:g} and b = {T_B:g} the legend should say f(x) = {T_W:g}x + {T_B:g}.\n"
        f"Your legend says: {texts}\nUse w and b in the label, for example with an f-string."
    )


@passed(definesFunction, timeout=90, hide=False)
def functionTitle():
    """plot_regression shows the MSE in the title"""
    titles = [ax.get_title() for ax in callAxes()]
    assert any(mentions(t, T_MSE) for t in titles), (
        f"plot_regression({T_XS}, {T_YS}, {T_W:g}, {T_B:g}, {T_MSE}) should have the title "
        f"'MSE = {T_MSE:.4f}'.\nYour titles: {titles}\n"
        "Show the mse_value you get as a parameter with plt.title()."
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
    assert point_sets, "No scatter plot found. Use plot_regression to draw the apartments."

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
    """the line f(x) = 8x + 50 is drawn, prices divided by 1000"""
    lines = [line for ax in allAxes() for line in ax.get_lines()]
    assert lines, "No line found. Use plot_regression to draw the regression line."

    for line in lines:
        if follows(line, W / 1000, B / 1000):
            xs = [float(x) for x in line.get_xdata()]
            assert min(xs) <= min(SIZES) and max(xs) >= max(SIZES), (
                "The line should cover the whole range of the data, "
                f"at least from {min(SIZES):g} to {max(SIZES):g} m².\n"
                f"Your line runs from {min(xs):g} to {max(xs):g}."
            )
            return
    if any(follows(line, W, B) for line in lines):
        raise AssertionError(
            "The line shows the prices in euros.\n"
            "With prices in thousands of euros, the model is w = 8 and b = 50."
        )
    raise AssertionError(
        "None of the lines follows f(x) = 8x + 50.\n"
        "Call plot_regression with w = 8 and b = 50."
    )


@passed(showsGraph, timeout=90, hide=False)
def mseTitle():
    """the title shows the MSE of the model, 100.0000"""
    titles = [ax.get_title() for ax in allAxes()]
    if any(mentions(t, MSE_K) for t in titles):
        return
    if any(mentions(t, MSE_K * 1000 ** 2) for t in titles):
        raise AssertionError(
            "The title shows the MSE in euros.\n"
            "Compute the MSE with the prices in thousands of euros, and w = 8, b = 50."
        )
    found = f"Your titles: {titles}" if any(titles) else "Your plot has no title."
    raise AssertionError(
        f"The title should read 'MSE = {MSE_K:.4f}'. {found}\n"
        "Compute the MSE with your mse function and pass it to plot_regression."
    )


@passed(showsGraph, timeout=90, hide=False)
def labels():
    """the axes are labelled"""
    axes = allAxes()
    xlabels = [ax.get_xlabel() for ax in axes]
    ylabels = [ax.get_ylabel() for ax in axes]
    if not any("size" in l.lower() for l in xlabels):
        raise AssertionError("Label the x-axis 'Size (m²)' with plt.xlabel().")
    if not any("price" in l.lower() for l in ylabels):
        raise AssertionError("Label the y-axis 'Price (× €1000)' with plt.ylabel().")
