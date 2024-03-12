from checkpy import *

only("histogram.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

correct_def_sum_random_numbers = test()(declarative
    .function("sum_random_numbers")
    .params()
    .call()
    .description("correctly defines the sum_random_numbers() function")
)


sum_random_numbers = (declarative.function("sum_random_numbers"))


@passed(correct_def_sum_random_numbers, hide=False)
def correctBelow40():
    """prints, on the first line, how often the sum is less than 42"""
    lines = outputOf().split("\n")
    assert 1 < len(lines), "your program doesn't print anything"
    firstLine = lines[0]
    
    numbers = static.getNumbersFrom(firstLine)

    assert approx(0.277, abs=0.05) in numbers or approx(277, abs=50) in numbers,\
        "make sure your program outputs a sentence containing the percentage on the first line of the output"

    assert '42' in firstLine


@passed(correct_def_sum_random_numbers, hide=False)
def correctAbove60():
    """prints, on the second line, how often the sum is more than 58"""
    lines = outputOf().split("\n")
    assert 1 <= len(lines), "your program doesn't print a second line"
    secondLine = lines[1]

    numbers = static.getNumbersFrom(secondLine)

    assert approx(0.277, abs=0.05) in numbers or approx(277, abs=50) in numbers,\
        "make sure your program outputs a sentence containing the percentage on the second line of the output"

    assert '58' in secondLine


@passed(correct_def_sum_random_numbers, hide=False)
def showsGraph():
	"""either saves a graph into a file, or shows a graph on the screen."""
	assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls(), "make sure to either save the graph into a file, or show a graph on the screen, using the plt.savefig() or plt.show() function respectively"
