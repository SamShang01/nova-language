#!/usr/bin/env python3
# 测试两种启动方式的差异

import sys
import os

# 方式 1: 直接导入（test_idle_source.py 使用的方式）
print("=" * 60)
print("方式 1: 直接导入")
print("=" * 60)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.cli.main import NovaIDLE
print("✓ 直接导入成功")

# 方式 2: 使用模块方式（python -m nova idle 使用的方式）
print("\n" + "=" * 60)
print("方式 2: 使用模块方式")
print("=" * 60)

# 模拟 python -m nova idle 的调用
import nova.cli
print(f"✓ 导入 nova.cli 成功")
print(f"  nova.cli 模块路径: {nova.cli.__file__}")

# 检查 cli_main 函数
from nova.cli import cli_main
print(f"✓ 导入 cli_main 成功")

# 检查 start_idle 函数
from nova.cli.main import start_idle
print(f"✓ 导入 start_idle 成功")

# 比较两种方式创建的 NovaIDLE 实例
print("\n" + "=" * 60)
print("比较两种方式")
print("=" * 60)

idle1 = NovaIDLE()
print(f"方式 1 创建的 NovaIDLE: {idle1}")

idle2 = NovaIDLE()
print(f"方式 2 创建的 NovaIDLE: {idle2}")

print(f"\n两种方式创建的实例类型相同: {type(idle1) == type(idle2)}")
print(f"两种方式创建的实例类相同: {idle1.__class__ == idle2.__class__}")

# 检查关键方法
print(f"\n方式 1 有 execute_nova_code: {hasattr(idle1, 'execute_nova_code')}")
print(f"方式 2 有 execute_nova_code: {hasattr(idle2, 'execute_nova_code')}")

print(f"\n方式 1 有 on_shell_return: {hasattr(idle1, 'on_shell_return')}")
print(f"方式 2 有 on_shell_return: {hasattr(idle2, 'on_shell_return')}")
