#!/usr/bin/env python
"""
调试 getattr 函数的返回值
"""

import sys
sys.path.insert(0, 'src')

from nova.vm.machine import NovaInstance, NovaClass

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': 35}

instance2 = NovaInstance(nova_class)
instance2.fields = {'name': 'John', 'age': 30}

# 测试 getattr 函数
print("测试 getattr 函数:")
left_age = getattr(instance1, 'age', 0)
right_age = getattr(instance2, 'age', 0)
print(f"left_age: {left_age}, type: {type(left_age)}")
print(f"right_age: {right_age}, type: {type(right_age)}")

# 测试比较
print("\n测试比较:")
try:
    result = left_age < right_age
    print(f"left_age < right_age: {result}")
except Exception as e:
    print(f"Error: {e}")

try:
    result = left_age > right_age
    print(f"left_age > right_age: {result}")
except Exception as e:
    print(f"Error: {e}")

# 测试 NovaInstance 对象的比较
print("\n测试 NovaInstance 对象的比较:")
try:
    result = instance1 < instance2
    print(f"instance1 < instance2: {result}")
except Exception as e:
    print(f"Error: {e}")

try:
    result = instance1 > instance2
    print(f"instance1 > instance2: {result}")
except Exception as e:
    print(f"Error: {e}")
