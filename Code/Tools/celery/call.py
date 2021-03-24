# coding: utf-8
# Author: wanhui0729@gmail.com

'''
调用任务
'''


from proj.task import add


result = add.delay(4, 4)
# 检查是否处理完成
print("task done: ", result.ready())
# 同步阻塞等待结果
print("result: ", result.get(timeout=1))

# 参数签名
s1 = add.s(2, 2)
res = s1.delay()
print("signature result: ", res.get())