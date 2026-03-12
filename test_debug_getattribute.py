#!/usr/bin/env python
"""
调试 NovaInstance.__getattribute__ 方法
"""

import sys
sys.path.insert(0, 'src')

from nova.vm.machine import NovaInstance, NovaClass

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': '35'}  # 使用字符串类型的 age

# 测试 __getattribute__ 方法
print("测试 __getattribute__ 方法:")
print(f"instance1.fields: {instance1.fields}")

# 测试获取 age 字段
age = instance1.age
print(f"instance1.age: {age}, type: {type(age)}")

# 测试获取 name 字段
name = instance1.name
print(f"instance1.name: {name}, type: {type(name)}")

# 测试 __ge__ 方法
print("\n测试 __ge__ 方法:")
instance2 = NovaInstance(nova_class)
instance2.fields = {'name': 'John', 'age': '30'}  # 使用字符串类型的 age

result = instance1 >= instance2
print(f"instance1 >= instance2: {result}")

# 测试 __gt__ 方法
print("\n测试 __gt__ 方法:")
result = instance1 > instance2
print(f"instance1 > instance2: {result}")
