#!/usr/bin/env python
"""
测试 >= 操作符
"""

from nova.vm.machine import NovaInstance, NovaClass

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': 35}

instance2 = NovaInstance(nova_class)
instance2.fields = {'name': 'John', 'age': 30}

print(f"instance1: {instance1}")
print(f"instance2: {instance2}")

# 测试 >= 操作符
print("\n测试 >= 操作符:")
try:
    result = instance1 >= instance2
    print(f"instance1 >= instance2: {result}")
except Exception as e:
    print(f"Error: {e}")

# 测试 age 字段
print("\n测试 age 字段:")
print(f"instance1.age: {instance1.age}, type: {type(instance1.age)}")
print(f"instance2.age: {instance2.age}, type: {type(instance2.age)}")

# 测试 age 字段的比较
print("\n测试 age 字段的比较:")
try:
    result = instance1.age >= instance2.age
    print(f"instance1.age >= instance2.age: {result}")
except Exception as e:
    print(f"Error: {e}")
