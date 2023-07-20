from checkpy import *

only("histogram.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def hasSomRandomGetallen():
    """defines the function sum_random_numbers()"""
    assert "sum_random_numbers" in static.getFunctionDefinitions()

@passed(hasSomRandomGetallen, hide=False)
def correctBelow40():
    """prints, on the first line, how often the sum is less than 40"""
    firstLine = outputOf().split("\n")[0]

    numbers = []
    for item in firstLine.split():
        try:
            numbers.append(float(item))
        except ValueError:
            pass

    assert approx(5, abs=5) in numbers or approx(0.05, abs=0.05) in numbers,\
        "make sure you output a sentence containing the answer on the first line of output"

    assert '40' in firstLine or 'veertig' in firstLine or 'forty' in firstLine

@passed(hasSomRandomGetallen, hide=False)
def correctAbove60():
    """prints, on the second line, how often the sum is more than 60"""
    lines = outputOf().split("\n")
    assert len(lines) > 1
    secondLine = lines[1]

    numbers = []
    for item in secondLine.split():
        try:
            numbers.append(float(item))
        except ValueError:
            pass

    assert approx(5, abs=5) in numbers or approx(0.05, abs=0.05) in numbers,\
        "make sure you output a sentence containing the answer on the first line of output"

    assert '60' in secondLine or 'zestig' in secondLine or 'sixty' in secondLine
