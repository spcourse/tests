from checkpy import *

import sys

# let students import their own earlier files, as `python file.py` would
if "" not in sys.path:
    sys.path.insert(0, "")

# students may import their own functions from the earlier vector assignments
only("apply_affine.py", "vec_operations.py", "inner_product.py")

predict = (
    declarative.function("predict")
    .returnType(float)
    .params("x", "w", "b")
)

apply_affine = (
    declarative.function("apply_affine")
    .returnType(list)
    .params("xs", "w", "b")
)

test_predict1 = test()(predict.call(60.0, 8000.0, 50000.0).returns(530000.0))

test_predict2 = test()(predict.call(90.0, 8000.0, 50000.0).returns(770000.0))

test_predict3 = test()(predict.call(4.0, -0.5, 3.0).returns(1.0))

test_apply1 = test()(apply_affine
    .call([30.0, 45.0, 60.0, 75.0, 90.0, 120.0], 8000.0, 50000.0)
    .returns([290000.0, 410000.0, 530000.0, 650000.0, 770000.0, 1010000.0])
)

test_apply2 = test()(apply_affine.call([0.0, 1.0, -2.0], 2.0, 1.0).returns([1.0, 3.0, -3.0]))

test_apply3 = test()(apply_affine.call([5.0], 0.0, 7.0).returns([7.0]))


@test()
def newList():
    """apply_affine returns a new list and leaves its input unchanged"""
    xs = [1.0, 2.0, 3.0]
    getModule().apply_affine(xs, 2.0, 1.0)
    assert xs == [1.0, 2.0, 3.0], (
        "apply_affine changed the list xs that was passed to it.\n"
        "Build a new list for the predictions and leave xs as it was."
    )
