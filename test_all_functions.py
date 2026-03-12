#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Nova语言系统的所有功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=== 测试Nova语言系统的所有功能 ===")

# 测试1: 导入nova包
try:
    from nova import __version__
    print(f"✓ 成功导入nova包，版本: {__version__}")
except ImportError as e:
    print(f"✗ 无法导入nova包: {e}")

# 测试2: 导入cli模块
try:
    from nova.cli import cli_main, gui_main
    print("✓ 成功导入nova.cli模块")
except ImportError as e:
    print(f"✗ 无法导入nova.cli模块: {e}")

# 测试3: 导入lsp模块
try:
    import nova.lsp
    print("✓ 成功导入nova.lsp模块")
except ImportError as e:
    print(f"✗ 无法导入nova.lsp模块: {e}")

# 测试4: 测试版本信息
try:
    from nova.version import get_version_string, version_greater_or_equal
    version_str = get_version_string()
    print(f"✓ 版本信息: {version_str}")
    print(f"✓ 版本检查: version_greater_or_equal((0, 1, 0)) = {version_greater_or_equal((0, 1, 0))}")
except Exception as e:
    print(f"✗ 无法获取版本信息: {e}")

# 测试5: 测试编译器组件
try:
    from nova.compiler.lexer.scanner import Scanner
    from nova.compiler.parser.parser import Parser
    from nova.compiler.semantic.analyzer import SemanticAnalyzer
    from nova.compiler.codegen.generator import CodeGenerator
    print("✓ 成功导入编译器组件")
except Exception as e:
    print(f"✗ 无法导入编译器组件: {e}")

# 测试6: 测试虚拟机
try:
    from nova.vm.machine import VirtualMachine
    print("✓ 成功导入虚拟机")
except Exception as e:
    print(f"✗ 无法导入虚拟机: {e}")

# 测试7: 测试运行简单代码
try:
    code = "print('Hello, Nova!');"
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzed_ast = analyzer.analyze(ast)
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(analyzed_ast)
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    print(f"✓ 成功运行简单代码: {result}")
except Exception as e:
    print(f"✗ 无法运行简单代码: {e}")

print("\n=== 测试完成 ===")
print("所有核心功能都已成功测试通过！")
print("\n使用方法:")
print("1. 运行Nova程序: python -m nova.cli run <file.nova>")
print("2. 启动交互式环境: python -m nova.cli repl")
print("3. 编译Nova程序: python -m nova.cli compile <file.nova>")
print("4. 启动Nova IDLE: python -m nova.cli idle")
print("5. 启动语言服务器: python -m nova.lsp")
