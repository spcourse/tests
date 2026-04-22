from checkpy import *
from shared import noImportSum

only("average_variance_fn.py")

avg = declarative.function("average").returnType(float).params("numbers")

var = declarative.function("variance").returnType(float).params("numbers")

test_avg1 = test()(avg.call([1.0, 2.0, 3.0]).returns(2.0))

test_avg2 = test()(avg.call([10.0, 20.0, 30.0, 40.0]).returns(25.0))

test_avg3 = test()(avg.call([7.0]).returns(7.0))

test_var1 = test()(var.call([2.0, 4.0, 4.0, 6.0]).returns(2.0))

test_var2 = test()(var.call([1.0, 3.0]).returns(1.0))

test_var3 = test()(var.call([5.0, 5.0, 5.0]).returns(0.0))
