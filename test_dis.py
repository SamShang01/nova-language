"""
测试dis模块和常量折叠
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova import dis

print("=" * 60)
print("测试常量折叠（启用优化）")
print("=" * 60)

# 测试1: 整数加法（应该被优化）
dis.dis("1+2+3;")

print("=" * 60)
print("测试常量折叠（禁用优化）")
print("=" * 60)

# 测试2: 整数加法（不应该被优化）
dis.dis("1+2+3;", optimize=False)

print("=" * 60)
print("测试浮点数运算")
print("=" * 60)

# 测试3: 浮点数运算
dis.dis("0.1+0.2;")

print("=" * 60)
print("测试变量运算（不应该被优化）")
print("=" * 60)

# 测试4: 变量运算（不应该被优化）
dis.dis("var x = 1; var y = 2; x+y;")
