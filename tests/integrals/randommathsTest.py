from checkpy import *

import math

only("randommaths.py")

correct_def_random_math = test()(declarative
    .function("random_math")
    .returnType(float)
    .params()
    .call()
    .description("correctly defines the random_math() function")
)


random_math = (declarative.function("random_math"))


@passed(correct_def_random_math, hide=False)
def correctAnswer():
	"""randommaths.py prints the correct answer (does the number ring familiar?)"""
	random_math.call().returns(approx(math.e, abs=0.0027))()