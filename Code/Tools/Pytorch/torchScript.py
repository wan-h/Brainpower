# coding: utf-8
# Author: wanhui0729@gmail.com

import torch

class MyDecisiongate(torch.nn.Module):
    def forward(self, x):
        if x.sum() > 0:
            return x
        else:
            return -x

class MyCell(torch.nn.Module):
    def __init__(self, dg):
        super(MyCell, self).__init__()
        self.dg = dg
        self.linear = torch.nn.Linear(4, 4)

    def forward(self, x, h):
        new_h = torch.tanh(self.dg(self.linear(x)) + h)
        return new_h, new_h

my_cell = MyCell(MyDecisiongate())
x, h = torch.rand(3, 4), torch.rand(3, 4)
traced_cell = torch.jit.trace(my_cell, (x, h))
print("my_cell:\n", my_cell)
print("jit trace my_cell:\n", traced_cell)
print("my_cell output:\n", my_cell(x, h))
print("jit trace my_cell output:\n", traced_cell(x, h))
print("jit graph:\n", traced_cell.graph)
print("jit code:\n", traced_cell.code)

# 判断语句会被解析为运行时的常数, torch.jit.script提供script compilerd分析python逻辑语句
scrpted_gate = torch.jit.script(MyDecisiongate())
my_cell = MyCell(scrpted_gate)
traced_cell = torch.jit.script(my_cell)
print("jit script:\n", traced_cell.code)
print("jit script my_cell output:\n", traced_cell(x, h))


# Mixing Scripting and Tracing
class MyRNNLoop(torch.nn.Module):
    def __init__(self):
        super(MyRNNLoop, self).__init__()
        self.cell = torch.jit.trace(MyCell(scrpted_gate), (x, h))

    def forward(self, xs):
        h, y = torch.zeros(3, 4), torch.zeros(3, 4)
        for i in range(xs.size(0)):
            y, h = self.cell(xs[i], h)
        return y, h
rnn_loop = torch.jit.script(MyRNNLoop())
print("MyRNNLoop jit script:\n", rnn_loop.code)

class WrapRNN(torch.nn.Module):
    def __init__(self):
        super(WrapRNN, self).__init__()
        self.loop = torch.jit.script(MyRNNLoop())

    def forward(self, xs):
        y, h = self.loop(xs)
        return torch.relu(y)

traced = torch.jit.trace(WrapRNN(), (torch.rand(10, 3, 4)))
print("WrapRNN jit trace:\n", traced.code)


# Saving and Loading models
traced.save('wrapped_rnn.zip')
loaded = torch.jit.load('wrapped_rnn.zip')
print("jit loaded:\n", loaded)
print("jit loaded code:\n", loaded.code)