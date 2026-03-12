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
print(f"instance1.age: {instance1.age}, type: {type(instance1.age)}")

# 测试直接使用 getattr 函数
print("\n测试直接使用 getattr 函数:")
left_age = getattr(instance1, 'age', 0)
print(f"left_age: {left_age}, type: {type(left_age)}")
