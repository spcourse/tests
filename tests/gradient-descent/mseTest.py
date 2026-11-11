from checkpy import *

import sys

# let students import their own earlier files, as `python file.py` would
if "" not in sys.path:
    sys.path.insert(0, "")

# students may import vector_diff and inner_product from the earlier assignments
only("mse.py", "vec_operations.py", "inner_product.py")

fun = (
    declarative.function("mse")
    .returnType(float)
    .params("predictions", "targets")
)

test1 = test()(fun
    .call(
        [290000.0, 410000.0, 530000.0, 650000.0, 770000.0, 1010000.0],
        [280000.0, 400000.0, 540000.0, 660000.0, 760000.0, 1020000.0],
    )
    .returns(100000000.0)
)

test2 = test()(fun.call([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]).returns(0.0))

test3 = test()(fun.call([1.0, 2.0, 3.0, 4.0], [2.0, 2.0, 5.0, 1.0]).returns(3.5))

test4 = test()(fun.call([0.0], [-3.0]).returns(9.0))
