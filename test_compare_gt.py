#!/usr/bin/env python
"""
测试 COMPARE_GT 指令
"""

from nova.vm.instructions import COMPARE_GT
from nova.vm.machine import VirtualMachine

vm = VirtualMachine()

# 测试1: 整数比较
vm.stack.append(35)  # left
vm.stack.append(30)  # right

print("测试1: 整数比较")
print(f"栈内容: {vm.stack}")

instr = COMPARE_GT()
instr.execute(vm)

print(f"结果: {vm.stack[-1]}")

# 测试2: 字符串和整数混合
vm2 = VirtualMachine()
vm2.stack.append("35")  # left (字符串)
vm2.stack.append(30)   # right (整数)

print("\n测试2: 字符串和整数混合")
print(f"栈内容: {vm2.stack}")

instr2 = COMPARE_GT()
instr2.execute(vm2)

print(f"结果: {vm2.stack[-1]}")
