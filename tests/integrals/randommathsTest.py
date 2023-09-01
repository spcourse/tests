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

@test()
def correctAmount(test):
	"""randommaths.py prints the correct answer (does the number ring familiar?)"""
	assert approx(math.e, abs=0.0027) in static.getNumbersFrom(outputOf())