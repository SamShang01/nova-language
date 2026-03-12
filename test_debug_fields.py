#!/usr/bin/env python
"""
调试 NovaInstance 的 fields 属性
"""

from nova.vm.machine import NovaInstance, NovaClass

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': 35}

instance2 = NovaInstance(nova_class)
instance2.fields = {'name': 'John', 'age': 30}

print(f"instance1.fields: {instance1.fields}")
print(f"instance2.fields: {instance2.fields}")

print(f"\ninstance1.age: {instance1.age}, type: {type(instance1.age)}")
print(f"instance2.age: {instance2.age}, type: {type(instance2.age)}")

# 测试比较
print("\n测试比较:")
try:
    result = instance1.age < instance2.age
    print(f"instance1.age < instance2.age: {result}")
except Exception as e:
    print(f"Error: {e}")

try:
    result = instance1.age > instance2.age
    print(f"instance1.age > instance2.age: {result}")
except Exception as e:
    print(f"Error: {e}")
