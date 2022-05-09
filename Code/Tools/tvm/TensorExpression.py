# -*- coding: utf-8 -*-
# @Author  : wanhui

"""
https://tvm.apache.org/docs/tutorial/tensor_expr_get_started.html
Working with Operators Using Tensor Expression
"""

"""
Example 1: Writing and Scheduling Vector Addition in TE for CPU
"""
import tvm
import tvm.testing
from tvm import te
import numpy as np

tgt = tvm.target.Target(target="llvm", host="llvm")

# Describing the Vector Computation
n = te.var("n")
A = te.placeholder((n, ), name="A")
B = te.placeholder((n, ), name="B")
C = te.compute(A.shape, lambda i: A[i] + B[i], name="C")
# Create a Default Schedule for the Computation
s = te.create_schedule(C.op)
# Compile and Evaluate the Default Schedule
fadd = tvm.build(s, [A, B, C], tgt, name="myadd")

dev = tvm.device(tgt.kind.name, 0)
n = 1024
a = tvm.nd.array(np.random.uniform(size=n).astype(A.dtype), dev)
b = tvm.nd.array(np.random.uniform(size=n).astype(B.dtype), dev)
c = tvm.nd.array(np.zeros(n, dtype=C.dtype), dev)
fadd(a, b, c)
print("{} ?= {}".format(c.numpy(), a.numpy() + b.numpy()))

tvm.testing.assert_allclose(c.numpy(), a.numpy() + b.numpy())

import timeit
np_repeat = 100
np_running_time = timeit.timeit(
    setup="import numpy\n"
    "n = 32768\n"
    'dtype = "float32"\n'
    "a = numpy.random.rand(n, 1).astype(dtype)\n"
    "b = numpy.random.rand(n, 1).astype(dtype)\n",
    stmt="answer = a + b",
    number=np_repeat,
)
print("Numpy running time: %f" % (np_running_time / np_repeat))

def evaluate_addition(func, target, optimization, log):
    dev = tvm.device(target.kind.name, 0)
    n = 32768
    a = tvm.nd.array(np.random.uniform(size=n).astype(A.dtype), dev)
    b = tvm.nd.array(np.random.uniform(size=n).astype(B.dtype), dev)
    c = tvm.nd.array(np.zeros(n, dtype=C.dtype), dev)

    evaluator = func.time_evaluator(func.entry_name, dev, number=10)
    mean_time = evaluator(a, b, c).mean
    print("%s: %f" % (optimization, mean_time))

    log.append((optimization, mean_time))


log = [("numpy", np_running_time / np_repeat)]
evaluate_addition(fadd, tgt, "naive", log=log)