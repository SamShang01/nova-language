#!/usr/bin/env python
"""
测试 generator.py 是否正确导入 COMPARE_GE
"""

# 测试从 generator.py 导入
from nova.compiler.codegen.generator import CodeGenerator

# 创建代码生成器实例
gen = CodeGenerator()

# 检查 COMPARE_GE 是否在 operator_map 中
# 我们需要访问 visit_BinaryExpression 方法中的 operator_map
# 由于 operator_map 是局部变量，我们需要通过其他方式检查

# 直接检查导入
from nova.vm.instructions import COMPARE_GE

print("COMPARE_GE 类导入成功")
print(f"COMPARE_GE 类: {COMPARE_GE}")

# 测试创建实例
instr = COMPARE_GE()
print(f"COMPARE_GE 实例创建成功: {instr}")

# 检查 generator.py 中的导入
import nova.compiler.codegen.generator as gen_module

# 检查 COMPARE_GE 是否在模块的命名空间中
if hasattr(gen_module, 'COMPARE_GE'):
    print("COMPARE_GE 在 generator 模块的命名空间中")
else:
    print("COMPARE_GE 不在 generator 模块的命名空间中")

# 检查所有导入的内容
import types
for name in dir(gen_module):
    obj = getattr(gen_module, name)
    if isinstance(obj, type) and issubclass(obj, object):
        if 'COMPARE' in name:
            print(f"找到比较类: {name} = {obj}")
