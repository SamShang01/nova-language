#!/usr/bin/env python
"""
测试 COMPARE_GE 指令
"""

# 测试导入
from nova.vm.instructions import COMPARE_GE

print("COMPARE_GE 类导入成功")

# 测试创建实例
instr = COMPARE_GE()
print(f"COMPARE_GE 实例创建成功: {instr}")

# 测试虚拟机
from nova.vm.machine import VirtualMachine

vm = VirtualMachine()
vm.stack.append(35)  # left
vm.stack.append(30)  # right

print(f"栈内容: {vm.stack}")

# 执行指令
instr.execute(vm)

print(f"结果: {vm.stack[-1]}")

# 测试字符串和整数混合
vm2 = VirtualMachine()
vm2.stack.append("35")  # left (字符串)
vm2.stack.append(30)   # right (整数)

print(f"\n栈内容 (字符串+整数): {vm2.stack}")

# 执行指令
instr.execute(vm2)

print(f"结果: {vm2.stack[-1]}")
