#!/usr/bin/env python3
# Nova IDLE 诊断脚本

import sys
import os

print("=" * 60)
print("Nova IDLE 诊断信息")
print("=" * 60)

# 1. Python 版本
print(f"\n1. Python 版本: {sys.version}")
print(f"   Python 路径: {sys.executable}")

# 2. 检查 nova 模块
try:
    import nova
    print(f"\n2. Nova 模块信息:")
    print(f"   版本: {nova.__version__}")
    print(f"   路径: {nova.__file__}")
except Exception as e:
    print(f"\n2. 错误: 无法导入 nova 模块 - {e}")
    sys.exit(1)

# 3. 检查 analyzer 模块
try:
    import nova.compiler.semantic.analyzer as analyzer
    print(f"\n3. Analyzer 模块信息:")
    print(f"   路径: {analyzer.__file__}")

    # 检查是否包含修复
    import inspect
    source = inspect.getsource(analyzer.SemanticAnalyzer.visit_CallExpression)
    has_int_fix = 'elif node.callee.name == "int":' in source
    print(f"   包含 int 修复: {'✓' if has_int_fix else '✗'}")

    if not has_int_fix:
        print("   警告: analyzer.py 不包含最新的修复！")
except Exception as e:
    print(f"\n3. 错误: 无法检查 analyzer 模块 - {e}")

# 4. 检查 main 模块
try:
    import nova.cli.main as main
    print(f"\n4. CLI 主模块信息:")
    print(f"   路径: {main.__file__}")

    # 检查是否有 start_idle 函数
    has_start_idle = hasattr(main, 'start_idle')
    print(f"   包含 start_idle 函数: {'✓' if has_start_idle else '✗'}")
except Exception as e:
    print(f"\n4. 错误: 无法检查 CLI 主模块 - {e}")

# 5. 检查 nova 命令
print(f"\n5. nova 命令检查:")
try:
    import subprocess
    result = subprocess.run(['nova', '--version'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"   nova 命令可用: ✓")
        print(f"   输出: {result.stdout.strip()}")
    else:
        print(f"   nova 命令错误: {result.stderr}")
except Exception as e:
    print(f"   nova 命令不可用: {e}")

# 6. 建议
print(f"\n" + "=" * 60)
print("建议:")
print("=" * 60)
print("1. 如果使用 'python -m nova idle' 不工作，请尝试:")
print("   python test_idle_source.py")
print("")
print("2. 如果 nova 命令不工作，请尝试:")
print("   python -m nova.cli idle")
print("")
print("3. 如果模块路径不正确，请重新安装:")
print("   python setup.py install --force")
print("=" * 60)
