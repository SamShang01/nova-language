#!/usr/bin/env python
"""
调试 getattr 函数的实现 - 检查是否调用了 __ge__ 方法
"""

import sys
sys.path.insert(0, 'src')

from nova.vm.machine import NovaInstance, NovaClass

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': '35'}  # 使用字符串类型的 age

# 测试 getattr 函数
print("测试 getattr 函数:")
print(f"instance1.fields: {instance1.fields}")

# 模拟 CALL_FUNCTION 指令的栈操作
stack = []

# 模拟指令 0-3: 加载 getattr 函数、this、age，然后调用 getattr(this, 'age')
stack.append(lambda obj, attr: getattr(obj, attr))  # getattr 函数
stack.append(instance1)  # this
stack.append('age')  # age

print(f"Stack before: {stack}")

# 执行 CALL_FUNCTION 2 [] 指令
positional_count = 2
args = []
for _ in range(positional_count):
    args.insert(0, stack.pop())
func = stack.pop()

print(f"args: {args}")
print(f"func: {func}")

# 调用函数
result = func(*args)
print(f"result: {result}, type: {type(result)}")

# 将结果压入栈
stack.append(result)
print(f"Stack after: {stack}")
