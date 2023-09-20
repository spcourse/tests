from checkpy import *

import typing

only("roots.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

correct_def_roots = test()(declarative
    .function("roots")
    .returnType(typing.List[float])
    .params("a", "b", "c")
    .call(1, 2, -10)
    .description("correctly defines the roots() function")
)


correct_def_plot_roots = test()(declarative
    .function("plot_roots")
    .params("a", "b", "c")
    .description("correctly defines the plot_roots() function")
)


roots = (declarative.function("roots"))


@passed(correct_def_roots, hide=False)
def correctTwoRoots():
    """roots() yields the two correct roots for a=1, b=2, c=-10"""
    roots.call(1, 2, -10).returns([-4.3166247903554, 2.3166247903554])()

    returned = roots.call(1, 2, -10)().returned
    
    assert len(returned) == 2
    assert approx(-4.32, abs=0.01) in returned
    assert approx(2.32, abs=0.01) in returned


@passed(correct_def_roots, hide=False)
def correctRoot():
    """roots() yields the same correct roots for a=1, b=4, c=4"""
    roots.call(1, 4, 4).returns([-2.0, -2.0])()


@passed(correct_def_roots, hide=False)
def correctNone():
    """roots() yields no roots for a=3, b=6, c=9"""
    roots.call(3, 6, 9).returns([])()


@passed(correct_def_plot_roots, hide=False)
def showsGraph():
	"""either saves a graph into a file, or shows a graph on the screen."""
	assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls(), "make sure to either save the graph into a file, or show a graph on the screen, using the plt.savefig() or plt.show() function respectively"
