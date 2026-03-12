#!/usr/bin/env python
"""
调试 COMPARE_LT 指令的实现
"""

import sys
sys.path.insert(0, 'src')

from nova.vm.machine import NovaInstance, NovaClass, VirtualMachine
from nova.vm.instructions import COMPARE_LT, COMPARE_GT

# 创建 NovaInstance 对象
fields = [('name', 'string', 'public'), ('age', 'int', 'public')]
nova_class = NovaClass('Person', fields, [])
instance1 = NovaInstance(nova_class)
instance1.fields = {'name': 'Bob', 'age': 35}

instance2 = NovaInstance(nova_class)
instance2.fields = {'name': 'John', 'age': 30}

# 创建虚拟机
vm = VirtualMachine()

# 测试 COMPARE_LT 指令
print("测试 COMPARE_LT 指令:")
vm.stack.append(instance1)
vm.stack.append(instance2)
print(f"Stack before: {vm.stack}")

# 手动执行 COMPARE_LT 指令
left = vm.stack.pop()
right = vm.stack.pop()
print(f"left: {left}, type: {type(left)}")
print(f"right: {right}, type: {type(right)}")

# 处理NovaInstance对象的属性访问
if hasattr(left, 'fields') and isinstance(left.fields, dict):
    # 使用getattr访问属性，触发__getattribute__方法中的类型转换
    try:
        left_age = getattr(left, 'age', 0)
        print(f"left_age: {left_age}, type: {type(left_age)}")
        # 如果right也是NovaInstance，获取其age属性
        if hasattr(right, 'fields') and isinstance(right.fields, dict):
            right_age = getattr(right, 'age', 0)
            print(f"right_age: {right_age}, type: {type(right_age)}")
            result = left_age < right_age
        else:
            # right不是NovaInstance，直接比较
            result = left_age < right
        print(f"result: {result}")
    except Exception as ex:
        print(f"Exception: {ex}")
