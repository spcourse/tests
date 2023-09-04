from checkpy import *

import math

only("montecarlo.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

correct_def_montecarlo = test()(declarative
    .function("montecarlo")
    .params("func", "x1", "y1", "x2", "y2")
    .returnType(float)
    .call(lambda x : math.sin(x**2), 0, -1, math.pi, 1)
    .description("correctly defines the montecarlo() function")
)


montecarlo = (declarative.function("montecarlo"))


@passed(correct_def_montecarlo, hide=False)
def correctFunc1():
    """montecarlo() yields the correct value of an integral on [0,1] for the square function"""
    square = monkeypatch.documentFunction(
        lambda x: x**(x + 0.5),
        "lambda x: x**(x + 0.5)"
    )
    montecarlo.call(square, 0, 0, 1, 1).returns(approx(0.525, abs=0.015))()


@passed(correctFunc1, hide=False)
def correctFunc2():
    """montecarlo() yields the correct value when an interval does not start at x=0"""
    tanCosSin = monkeypatch.documentFunction(
        lambda x: math.tan(math.cos(math.sin(x))),
        "lambda x: tan(cos(sin(x)))"
    )
    montecarlo.call(tanCosSin, 0.2, 0, 2.2, 1.5).returns(approx(1.71, abs=0.02))()


@passed(correctFunc1, hide=False)
def correctFunc3():
    """montecarlo() yields the correct value when a function goes below the x-axis"""
    squaredSin = monkeypatch.documentFunction(
        lambda x: math.sin(x**2),
        "lambda x: sin(x**2)"
    )
    montecarlo.call(squaredSin, 0, -1, math.pi, 1).returns(approx(0.77, abs=0.02))()


@test()
def showsGraph():
	"""either saves a graph into a file, or shows a graph on the screen."""
	assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls(), "make sure to either save the graph into a file, or show a graph on the screen, using the plt.savefig() or plt.show() function respectively"