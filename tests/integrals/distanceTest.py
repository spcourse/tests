from checkpy import *

only("distance.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

correct_def_square = test()(declarative
    .function("square")
    .returnType(float)
    .params("n")
    .call(1)
    .description("correctly defines the square() function")
)


square = (declarative.function("square"))


@passed(correct_def_square, hide=False)
def correctAnswer():
	"""square() yields the correct distance for n = 10000"""
	square.call(10000).returns(approx(0.525, abs=0.015))()