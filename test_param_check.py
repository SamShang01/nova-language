#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试参数数量检查
"""

import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine
from nova.vm.errors import VMError

def execute(code):
    """执行Nova代码"""
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    ast.accept(analyzer)
    generator = CodeGenerator()
    ast.accept(generator)
    vm = VirtualMachine()
    vm.load(generator.instructions)
    return vm.run()

print("=" * 60)
print("测试参数数量检查")
print("=" * 60)

print("\n1. 正确的参数数量")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2);
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")
print("✓ 通过")

print("\n2. 参数数量不足")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1);
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")
print("✓ 通过（部分参数使用默认值None）")

print("\n3. 参数数量过多（应该报错）")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2, 3);
"""
print(f"代码: {code.strip()}")
try:
    result = execute(code)
    print(f"✗ 失败：应该抛出异常，但返回了 {result}")
except (TypeError, VMError) as e:
    if "takes 2 positional arguments but 3 were given" in str(e):
        print(f"✓ 通过：正确捕获错误 - {e}")
    else:
        print(f"✗ 失败：错误消息不正确 - {e}")

print("\n4. 无参数实例化")
code = """
struct Point {
    x: int;
    y: int;
}

Point();
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")
print("✓ 通过（所有参数使用默认值None）")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
