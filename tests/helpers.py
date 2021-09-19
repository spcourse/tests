from collections.abc import Iterable

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

def similar(v1, v2, atol):
    upper, lower =  (v2 + atol), (v2 - atol)
    return v1 < upper and v1 >= lower

# def similar_values(output, expected, atol=0):
#     if isinstance(output, Iterable) != isinstance(expected, Iterable):
#         return False
#     if isinstance(output, Iterable) and isinstance(expected, Iterable):
#         if len(output) != len(expected):
#             return False
#         if isinstance(atol, Iterable):
#             rest = max(0, len(output) - len(atol))
#         else:
#             rest = len(atol)
#         atols = atol + [0] * rest
#         for o, e, tol in zip(output, expected, atols):
#             if not similar(o, e, tol):
#                 return False
#     return True
