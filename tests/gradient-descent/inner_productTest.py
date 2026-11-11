from checkpy import *

only("inner_product.py")

fun = (
    declarative.function("inner_product")
    .returnType(float)
    .params("a", "b")
)

test1 = test()(fun.call([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]).returns(32.0))

test2 = test()(fun.call([2.0, 3.0], [2.0, 3.0]).returns(13.0))

test3 = test()(fun.call([1.0, 0.0], [0.0, 1.0]).returns(0.0))

test4 = test()(fun.call([5.0], [-2.0]).returns(-10.0))

test5 = test()(fun.call([1.0, -2.0, 0.5, 4.0], [2.0, 1.0, 4.0, -0.25]).returns(1.0))
