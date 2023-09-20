from checkpy import *

only("car_ride.py")
download("CarRideData.csv", "https://raw.githubusercontent.com/spcourse/bigdata/main/data/en/CarRideData.csv")

monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def correctDistance():
	"""prints the distance traveled"""
	output = outputOf(overwriteAttributes=[("__name__", "__main__")])
	numbers = static.getNumbersFrom(output)
	assert approx(10.86, abs=0.02) in numbers or approx(10860, abs=20) in numbers

@test()
def showsGraph():
    """either saves a graph into a file, or shows a graph on the screen"""
    assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls()
