from checkpy import *
from shared import noImportSum

only("weighted_average.py")

fun = (
    declarative.function("weighted_average")
    .returnType(float)
    .params("values", "weights")
)

test1 = test()(fun.call([1.0, 2.0, 3.0], [1.0, 1.0, 1.0]).returns(2.0))

test2 = test()(fun.call([4.0, 8.0], [1.0, 3.0]).returns(7.0))

test3 = test()(fun.call([0.0, 10.0], [3.0, 1.0]).returns(2.5))
