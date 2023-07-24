from collections.abc import Iterable
from uuid import uuid4

import checkpy.assertlib as assertlib
import checkpy.lib as lib
import checkpy

from typing import Any, Callable, Dict, Tuple, Union

class InvalidFunctionApplication(Exception):
    def __init__(self, message):
        self.message = message

ORDINALS = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
            '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
            '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
            '29th', '30th', '31st']

def apply_function(fn, input, output_descr, check_none=True):
    number_of_return_values = len(output_descr)
    _output = fn(*input)
    fname = fn.name
    if len(output_descr) == 1:
        if number_of_return_values != 1:
            raise InvalidFunctionApplication("Make sure to return only one value.")
        if check_none and _output == None:
            raise InvalidFunctionApplication("Function returns None. Tips: Does your function have a return? Do you try to return a print statement?")
        if type(_output) != output_descr[0]:
            raise InvalidFunctionApplication(f"Make sure the function {fname} returns a value of type {output_descr[0].__name__}.")
    else:
        if (type(_output) != tuple) or len(_output) != number_of_return_values:
            raise InvalidFunctionApplication(f"Make sure to return exactly {number_of_return_values} values.")
        for i, (expected_type, actual_value) in enumerate(zip(output_descr, _output)):
            if check_none and actual_value == None:
                raise InvalidFunctionApplication(f"The {ORDINALS[i]} return value is None.")
            if type(actual_value) != expected_type:
                raise InvalidFunctionApplication(f"Make sure the {ORDINALS[i]} return value is of type {expected_type.__name__}")

    return _output


def fn_string(fname, args):
    return f"{fname}({', '.join(args)})"

def has_function(test, file_name, function_name, expected_args):
    def testMethod():
        if assertlib.fileContainsFunctionDefinitions(file_name, function_name):
            fn = lib.getFunction(function_name, file_name)
            provided_args = fn.arguments
            if len(provided_args) == len(expected_args):
                return True, ""
            else:
                if len(expected_args) == 1:
                    m1 = f"Expected a single argument: {fn_string(function_name, expected_args)}"
                else:
                    m1 = f"Expected {len(expected_args)} arguments: {fn_string(function_name, expected_args)}"
                if len(provided_args) == 1:
                    m2 = f"Your function takes a single argument: {fn_string(function_name, provided_args)}"
                else:
                    m2 = f"Your function takes {len(provided_args)} arguments: {fn_string(function_name, provided_args)}"

                return False, f"Incorrect number of arguments:\n\t{m1}\n\t{m2}"
        else:
            return False, "Function not defined"

    test.test = testMethod
    test.description = lambda : f"Defines the function `{function_name}()`"



def similar(v1, v2, atol):
    upper, lower =  (v2 + atol), (v2 - atol)
    return v1 < upper and v1 >= lower


def assertDefFactory(
    function: str,
    parameters: Tuple[Any]=(),
    before: Callable[[], None]=lambda: None,
    timeout=10,
) -> checkpy.tests.Test:
    """
    Generates a test to assert a function definition is present with set parameters.
    For instance:

    testDef1 = helpers.assertDefFactory(
        name="simulate_apple1",
        parameters=["x", "dt"], 
        before=lambda: notAllowedCode({"break": "break"})
    )
    """
    def foo():
        before()

        assert function in checkpy.static.getFunctionDefinitions(),\
            "make sure the function is defined with the correct name"

        f = checkpy.getFunction(function)

        assert f.parameters == list(parameters),\
            "make sure the function has the correct parameters"

    foo.__name__ == str(uuid4())
    foo.__doc__ = f"Defines the function `{function}()`"
    return checkpy.test(timeout=timeout)(foo)


def assertFuncFactory(
    function: str,
    input: Union[Tuple[Any], Dict[str, Any]],
    output: Any,
    outputType: type=Any,
    hint: Callable[[Any], None]=lambda output: None,
    timeout=10,
) -> checkpy.tests.Test:
    """
    Generates a test to assert the outcome of a function call. For instance:

    testApple2 = helpers.assertFuncFactory(
        funcName="simulate_apple2",
        input=(0.01,),
        output=approx(2.84, abs=0.02),
        outputType=float
    )

    or something more complex:

    def apple1Hint(output):
        t, v = output
        if v == approx(4.52, abs=0.1) or t == approx(159.47, abs=1):
            assert False, "Did you mix up the order of the return values?"
        
        if v == approx(44.3, abs=0.3):
            assert False, "Did you forget to convert to km/h?"

    testApple1 = passed(testDef1, timeout=90, hide=False)(
        helpers.assertFuncFactory(
            funcName="simulate_apple1",
            input=(100, 0.01),
            output=(approx(159.47, abs=0.1), approx(4.52, abs=0.1)),
            outputType=Tuple[float, float],
            hint=apple1Hint
        )
    )
    """
    def foo():
        f = checkpy.getFunction(function)

        if isinstance(input, dict):
            inputStr = ", ".join([f"{k}={v}" for k, v in input.items()])
        else:
            inputStr = ", ".join(str(v) for v in input)

        if isinstance(input, dict):
            realOutput = f(**input)
        else:
            realOutput = f(*input)

        assert realOutput == checkpy.Type(outputType),\
            "make sure the function returns the correct type"

        hint(realOutput)

        assert realOutput == output,\
            f"Did not expect output {realOutput} (with input {inputStr})"

    foo.__name__ == str(uuid4())
    parameterStr = ", ".join(str(p) for p in input)
    foo.__doc__ = f"Testing {function}({parameterStr})"
    return checkpy.test(timeout=timeout)(foo)

