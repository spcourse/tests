from checkpy import *

only("vec_operations.py")

scalar_multiply = (
    declarative.function("scalar_multiply")
    .returnType(list)
    .params("c", "v")
)

vector_add = (
    declarative.function("vector_add")
    .returnType(list)
    .params("a", "b")
)

vector_diff = (
    declarative.function("vector_diff")
    .returnType(list)
    .params("a", "b")
)

test_scalar1 = test()(scalar_multiply.call(3.0, [1.0, 2.0, 3.0]).returns([3.0, 6.0, 9.0]))

test_scalar2 = test()(scalar_multiply.call(0.5, [2.0, 4.0]).returns([1.0, 2.0]))

test_scalar3 = test()(scalar_multiply.call(-2.0, [1.5, 0.0, -4.0, 8.0]).returns([-3.0, 0.0, 8.0, -16.0]))

test_add1 = test()(vector_add.call([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]).returns([5.0, 7.0, 9.0]))

test_add2 = test()(vector_add.call([1.0, -1.0], [1.0, 1.0]).returns([2.0, 0.0]))

test_diff1 = test()(vector_diff.call([4.0, 5.0, 6.0], [1.0, 2.0, 3.0]).returns([3.0, 3.0, 3.0]))

test_diff2 = test()(vector_diff.call([1.0, 1.0], [1.0, -1.0]).returns([0.0, 2.0]))

test_diff3 = test()(vector_diff.call([2.5], [4.0]).returns([-1.5]))


@test()
def newLists():
    """the functions return a new list and leave their inputs unchanged"""
    module = getModule()
    for name, args in [
        ("scalar_multiply", (2.0, [1.0, 2.0])),
        ("vector_add", ([1.0, 2.0], [3.0, 4.0])),
        ("vector_diff", ([1.0, 2.0], [3.0, 4.0])),
    ]:
        assert hasattr(module, name), f"{name} is not defined"
        copies = [list(a) if isinstance(a, list) else a for a in args]
        getattr(module, name)(*args)
        assert list(args) == copies, (
            f"{name} changed one of the lists passed to it.\n"
            "Build a new list for the result and leave the inputs as they were."
        )
