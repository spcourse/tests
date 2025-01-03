from checkpy import *
from shared import disallow, collect_function_names
import ast
import re

import numpy as np

only("plot1.py")
monkeypatch.patchMatplotlib()
monkeypatch.patchNumpy()

@test()
def noBreak():
    """Checking for disallowed code."""
    not_allowed = [ast.Break]
    disallow(not_allowed)


@passed(noBreak, timeout=90, hide=False)
def showsGraph():
	"""either saves a graph into a file, or shows a graph on the screen."""
	assert "plt.savefig" in static.getFunctionCalls() or "plt.show" in static.getFunctionCalls(), "make sure to either save the graph into a file, or show a graph on the screen, using the plt.savefig() or plt.show() function respectively"


@test(timeout=90)
def variablesExist():
    """checks if the variables x_values and y_values are defined"""
    # This test checks if the variables x_values and y_values are defined in the code.
    assert hasattr(getModule(), "x_values"), "The variable 'x_values' should be defined in your code."
    assert hasattr(getModule(), "y_values"), "The variable 'y_values' should be defined in your code."


@passed(variablesExist, timeout=90, hide=False)
def correctXValues():
    """checks if the x_values are correctly generated"""
    # This test checks if x_values start from 0, end at 4 and are in steps of 0.01.
    numbers = getModule().x_values

    assert len(numbers) == 400 or len(numbers) == 401, "The length of x_values seems incorrect. Make sure you generate x_values from 0 to 3.99 in steps of 0.01."
    assert approx(numbers[0], abs=0.005) == 0, "x_values should start from 0."
    assert approx(numbers[-1], abs=0.01) == 3.99, "x_values should end at 3.99."
    assert approx(numbers[1] - numbers[0], abs=0.005) == 0.01, "The step size between x_values should be 0.01."

@passed(variablesExist, timeout=90, hide=False)
def correctYValues():
    """checks if the y_values are correctly generated"""
    # This test checks if y_values are correctly calculated for each x_value based on the given polynomial.
    x_values = getModule().x_values
    y_values = getModule().y_values
    assert len(y_values) == 400 or len(y_values) == 401, "The length of y_values seems incorrect. Make sure you calculate y_values for each x_value."

    for x, y in zip(x_values, y_values):
        expected_y = 12.38 * x**4 - 84.38 * x**3 + 165.19 * x**2 - 103.05 * x
        assert approx(expected_y, abs=0.005) == y, f"For x = {x}, expected y = {expected_y}, but got {y}. Check your polynomial calculation."
