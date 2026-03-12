#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试llvmlite基本功能
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm

# 创建一个简单的模块
module = ir.Module(name="test")

# 创建一个函数：int add(int a, int b)
func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
add_func = ir.Function(module, func_type, name="add")

# 创建基本块
entry_block = add_func.append_basic_block(name="entry")
builder = ir.IRBuilder(entry_block)

# 获取函数参数
a, b = add_func.args

# 执行加法
result = builder.add(a, b)

# 返回结果
builder.ret(result)

# 打印LLVM IR
print("Generated LLVM IR:")
print(str(module))

print("\nTest completed successfully!")