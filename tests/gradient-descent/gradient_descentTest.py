from checkpy import *

import math
import re

only("gradient_descent.py")
download("emissions.csv", "https://github.com/spcourse/gradient-descent/raw/main/gradient-descent/emissions.csv")
monkeypatch.patchMatplotlib()

import matplotlib.pyplot as plt

TARGET_MSE = 0.0167
LEARNING_TITLES = [0.2445, 0.1379, 0.0889]   # visualize_learning(emissions, warming, 0, 0, 0.001)

# a small case to call fit with directly
S_XS = [1.0, 2.0, 3.0, 4.0]
S_YS = [3.0, 5.0, 8.0, 9.0]
S_ARGS = (S_XS, S_YS, 0, 0, 3, 0.01)


def readData():
    xs, ys = [], []
    with open("emissions.csv") as f:
        f.readline()
        for line in f:
            _, x, y = line.split(",")
            xs.append(float(x))
            ys.append(float(y))
    return xs, ys


def referenceFit(xs, ys, w, b, n, lr, mistake=None):
    """Gradient descent as on the page, or with one of the common mistakes."""
    N = len(xs)
    mses = []

    def mse(w, b):
        return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / N

    for _ in range(n):
        if mistake == "before":
            mses.append(mse(w, b))
        errors = [y - (w * x + b) for x, y in zip(xs, ys)]
        grad_w = -sum(e * x for e, x in zip(errors, xs))
        grad_b = -sum(errors)
        if mistake == "mean":
            grad_w, grad_b = grad_w / N, grad_b / N
        elif mistake == "mse":
            grad_w, grad_b = 2 * grad_w / N, 2 * grad_b / N
        elif mistake == "sign":
            grad_w, grad_b = -grad_w, -grad_b
        elif mistake == "no_x":
            grad_w = grad_b
        w = w - lr * grad_w
        if mistake == "new_w":
            grad_b = -sum(y - (w * x + b) for x, y in zip(xs, ys))
        b = b - lr * grad_b
        if mistake != "before":
            mses.append(mse(w, b))
    return w, b, mses


MISTAKES = {
    "before": "The MSE list holds the MSE *before* each update.\n"
              "Append the MSE after updating w and b, so the last value belongs to the final line.",
    "mean": "Your gradients are divided by the number of points (an average).\n"
            "The gradients on the page are sums: no division by N.",
    "mse": "Your gradients look like the derivative of the MSE (with 2/N in front).\n"
           "Use the gradients of the loss on the page: ½ Σ, so no 2/N.",
    "sign": "w and b move the wrong way, so the MSE goes up.\n"
            "Check the minus signs: the gradient is -(y - ŷ)·x, and the update is w := w - α · gradient.",
    "no_x": "The gradient for w is the same as the gradient for b.\n"
            "For w, multiply every error by its x: -(y - ŷ)·x.",
    "new_w": "b is updated with a gradient computed from the new w.\n"
             "Compute both gradients first, with the old w and b, and only then update w and b.",
}


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(b))


def sameFit(got, want):
    w, b, mses = got
    return (close(w, want[0]) and close(b, want[1]) and len(mses) == len(want[2])
            and all(close(m, n) for m, n in zip(mses, want[2])))


def checkFitResult(result, args):
    call = "fit({}, {}, {}, {}, {}, {})".format(*["emissions" if len(a) > 10 else a for a in args[:2]], *args[2:])
    if not (isinstance(result, tuple) and len(result) == 3):
        raise AssertionError(f"{call} should return three values: w, b, mse_list.\nIt returned: {result!r}")
    w, b, mses = result
    if not isinstance(mses, list):
        raise AssertionError(f"The third value fit returns should be a list of MSEs, not {type(mses).__name__}.")
    n = args[4]
    if len(mses) != n:
        raise AssertionError(f"{call} runs {n} steps, so mse_list should have {n} values. It has {len(mses)}.")

    want = referenceFit(*args)
    if sameFit(result, want):
        return
    for mistake, message in MISTAKES.items():
        if sameFit(result, referenceFit(*args, mistake=mistake)):
            raise AssertionError(message)
    raise AssertionError(
        f"{call} returns w = {w:.6f}, b = {b:.6f}.\n"
        f"Expected w = {want[0]:.6f}, b = {want[1]:.6f}."
    )


def numbersIn(text):
    return [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", text)]


def figureTitles(fig):
    return " ".join(ax.get_title() for ax in fig.axes)


def allAxes():
    """Run the student's file and return every axes it drew on."""
    getModule()
    return [ax for num in plt.get_fignums() for ax in plt.figure(num).axes]


@test(timeout=60)
def definesFit():
    """defines the function fit(xs, ys, w_start, b_start, n_iterations, learning_rate)"""
    if "fit" not in static.getFunctionDefinitions():
        raise AssertionError("Define a function called fit.")
    n = len(getFunction("fit").arguments)
    if n != 6:
        raise AssertionError(
            f"fit should take 6 parameters (xs, ys, w_start, b_start, n_iterations, learning_rate), yours takes {n}."
        )


@passed(definesFit, timeout=60, hide=False)
def fitSmallCase():
    """fit computes the right w, b and MSEs for a small data set"""
    xs, ys = list(S_XS), list(S_YS)
    result = getFunction("fit")(xs, ys, *S_ARGS[2:])
    if xs != S_XS or ys != S_YS:
        raise AssertionError("fit changes the lists xs or ys it gets. Leave them as they are.")
    checkFitResult(result, S_ARGS)


@passed(fitSmallCase, timeout=60, hide=False)
def fitEmissions():
    """fit(emissions, warming, 0, 0, 50, 1e-4) gives w = 0.250811, b = 0.096327"""
    xs, ys = readData()
    checkFitResult(getFunction("fit")(xs, ys, 0, 0, 50, 1e-4), (xs, ys, 0, 0, 50, 1e-4))


@passed(fitEmissions, timeout=60, hide=False)
def printsFirstRun():
    """prints the result of fit(emissions, warming, 0, 0, 50, 1e-4)"""
    output = outputOf()
    for line in ["w = 0.250811", "b = 0.096327", "MSE = 0.0496"]:
        if line not in output:
            raise AssertionError(
                f"The output should contain the line '{line}'.\n"
                "Print the result of fit(emissions, warming, 0, 0, 50, 1e-4) as shown on the page."
            )


@passed(fitEmissions, timeout=120, hide=False)
def printsConverged():
    """prints a converged fit with MSE = 0.0167"""
    values = re.findall(r"MSE\s*=\s*(\S+)", outputOf())
    numbers = []
    for v in values:
        try:
            numbers.append(float(v))
        except ValueError:
            pass
    # the data starts at an MSE of 0.2445 for w = b = 0; anything above 1 has blown up
    if any(not math.isfinite(m) or m > 1 for m in numbers):
        raise AssertionError(
            "One of your fits printed nan or a huge MSE: the learning rate is too large.\n"
            "Try a smaller learning rate."
        )
    if not any(m <= TARGET_MSE + 0.00005 for m in numbers):
        lowest = f" The lowest MSE you print is {min(numbers):.4f}." if numbers else ""
        raise AssertionError(
            f"Print the result of a fit that gets the MSE down to {TARGET_MSE}.{lowest}\n"
            "Increase the learning rate first, then the number of iterations."
        )


@test(timeout=60)
def definesVisualizeLearning():
    """defines the function visualize_learning(xs, ys, w_start, b_start, learning_rate)"""
    if "visualize_learning" not in static.getFunctionDefinitions():
        raise AssertionError("Define a function called visualize_learning.")
    n = len(getFunction("visualize_learning").arguments)
    if n != 5:
        raise AssertionError(
            f"visualize_learning should take 5 parameters (xs, ys, w_start, b_start, learning_rate), yours takes {n}."
        )
    if "plot_regression" not in static.getFunctionCalls():
        raise AssertionError("Use your plot_regression function to draw the plots.")


@passed(definesVisualizeLearning, timeout=60, hide=False)
def visualizeLearningPlots():
    """visualize_learning(emissions, warming, 0, 0, 0.001) shows three plots with MSE 0.2445, 0.1379, 0.0889"""
    getModule()
    xs, ys = readData()

    shown = []
    def recordShow(*args, **kwargs):
        shown.append(figureTitles(plt.gcf()))

    original_show = plt.show
    first = plt.figure().number
    plt.show = recordShow
    try:
        getFunction("visualize_learning")(xs, ys, 0, 0, 0.001)
    finally:
        plt.show = original_show

    titles = shown
    if len(titles) < 3:
        titles = [figureTitles(plt.figure(num)) for num in plt.get_fignums() if num >= first]
        titles = [t for t in titles if t]
    msesShown = [numbersIn(t) for t in titles]
    msesShown = [nums[0] for nums in msesShown if nums]

    want = ", ".join(f"{m:.4f}" for m in LEARNING_TITLES)
    if len(msesShown) != 3:
        raise AssertionError(
            f"visualize_learning should show three plots, with the MSE in each title ({want}).\n"
            f"Found {len(msesShown)} plots with an MSE in the title.\n"
            "Call plot_regression and plt.show() once per iteration."
        )
    if all(close(a, b, 0.001) for a, b in zip(msesShown, LEARNING_TITLES)):
        return
    if all(close(a, b, 0.001) for a, b in zip(msesShown, LEARNING_TITLES[1:] + [0.0653])):
        raise AssertionError(
            "The plots show the MSE after each update, so the starting line is never shown.\n"
            "Compute the MSE and plot the line first, and only then update w and b."
        )
    got = ", ".join(f"{m:.4f}" for m in msesShown)
    raise AssertionError(f"The titles should show the MSEs {want}, yours show {got}.")


@passed(definesVisualizeLearning, timeout=60, hide=False)
def callsVisualizeLearning():
    """the program calls visualize_learning"""
    if "visualize_learning" not in static.getFunctionCalls():
        raise AssertionError(
            "Your program never calls visualize_learning.\n"
            "Keep the call visualize_learning(emissions, warming, 0, 0, 0.001) in your file."
        )


@test(timeout=120)
def showsGraph():
    """the program shows the graphs or saves them to a file"""
    calls = static.getFunctionCalls()
    if not any(c.endswith("show") or c.endswith("savefig") for c in calls):
        raise AssertionError("Show the graphs with plt.show(), or save them with plt.savefig().")


@passed(showsGraph, printsConverged, timeout=120, hide=False)
def plotsConvergedFit():
    """the converged fit is plotted on top of the data"""
    data = sorted(zip(*readData()))
    for ax in allAxes():
        has_data = any(
            sorted((float(x), float(y)) for x, y in c.get_offsets()) == data for c in ax.collections
        )
        mses = numbersIn(ax.get_title())
        if has_data and mses and mses[0] <= TARGET_MSE + 0.00005:
            return
    raise AssertionError(
        "No plot found of the data with the converged line.\n"
        "Call plot_regression with the emissions, the warming, your final w and b, and the last MSE."
    )


@passed(showsGraph, printsConverged, timeout=120, hide=False)
def plotsMseCurve():
    """the MSE of the converged run is plotted over the iterations"""
    for ax in allAxes():
        for line in ax.get_lines():
            ys = [float(y) for y in line.get_ydata()]
            if (len(ys) >= 10 and all(math.isfinite(y) for y in ys)
                    and all(a >= b - 1e-12 for a, b in zip(ys, ys[1:]))
                    and ys[-1] <= TARGET_MSE + 0.00005):
                return
    raise AssertionError(
        "No plot found of the MSE over the iterations of your converged run.\n"
        "Plot the mse_list of that run with plt.plot(mse_list)."
    )
