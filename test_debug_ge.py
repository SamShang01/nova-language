#!/usr/bin/env python
"""
调试 NovaInstance.__ge__ 方法
"""

import sys
sys.path.insert(0, 'src')

from nova.vm.machine import NovaInstance, NovaClass

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': '35'}  # 使用字符串类型的 age

instance2 = NovaInstance(nova_class)
instance2.fields = {'name': 'John', 'age': '30'}  # 使用字符串类型的 age

# 测试 __ge__ 方法
print("测试 __ge__ 方法:")
try:
    result = instance1 >= instance2
    print(f"instance1 >= instance2: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# 测试 __ge__ 方法与整数比较
print("\n测试 __ge__ 方法与整数比较:")
try:
    result = instance1 >= 30
    print(f"instance1 >= 30: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
