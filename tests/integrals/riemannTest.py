from checkpy import *

only("riemann.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

correct_def_riemann = test()(declarative
    .function("riemann")
    .returnType(float)
    .params("a", "b", "c", "begin_x", "end_x", "n")
    .call(1, 1, 1, 0, 2, 1000)
    .description("correctly defines the riemann() function")
)


correct_def_plot_riemann = test()(declarative
    .function("plot_riemann")
    .params("a", "b", "c", "begin_x", "end_x", "n")
    .description("correctly defines the plot_riemann() function")
)


riemann = (declarative.function("riemann"))


@passed(correct_def_riemann, hide=False)
def correctFunc1():
	"""riemann() yields the correct value for x^2 + x + 1"""
	riemann.call(1, 1, 1, 0, 2, 1000).returns(approx(6.665, abs=0.005))()


@passed(correct_def_riemann, hide=False)
def correctFunc2():
	"""riemann() yields the correct value when an interval does not start at x=0"""
	riemann.call(1, 0, 0, -2, -1, 1000).returns(approx(2.335, abs=0.005))()
	assert getFunction("riemann")(1, 0, 0, -2, -1, 1000) == approx(2.335, abs=0.005)


@passed(correct_def_riemann, hide=False)
def correctFunc3():
	"""riemann() yields the correct value when a function goes below the x-axis"""
	riemann.call(1, 0, -2, -1, 1, 1000).returns(approx(-3.335, abs=0.005))()


@passed(correct_def_riemann, hide=False)
def correctFunc4():
	"""riemann() yields the correct value of an integral on [-2, 3], with n = 10, for the function -x^2 + 4x + 15"""
	riemann.call(-1, 4, 15, -2, 3, 10).returns(approx(73.5, abs=0.5))()


@passed(correct_def_plot_riemann, hide=False)
def showsGraph():
	"""either saves a graph into a file, or shows a graph on the screen."""
	assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls(), "make sure to either save the graph into a file, or show a graph on the screen, using the plt.savefig() or plt.show() function respectively"