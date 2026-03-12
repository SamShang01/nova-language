#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试关键字参数功能
"""

import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

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
print("测试关键字参数功能")
print("=" * 60)

print("\n1. 单个关键字参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(y:1);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=None, y=1)>", "测试失败"
print("✓ 通过")

print("\n2. 多个关键字参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(x:10, y:20);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=10, y=20)>", "测试失败"
print("✓ 通过")

print("\n3. 混合位置参数和关键字参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1, y:2);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=1, y=2)>", "测试失败"
print("✓ 通过")

print("\n4. 关键字参数顺序不影响结果")
code = """
struct Point {
    x: int;
    y: int;
}

Point(y:20, x:10);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=10, y=20)>", "测试失败"
print("✓ 通过")

print("\n5. 部分关键字参数")
code = """
struct Point {
    x: int;
    y: int;
    z: int;
}

Point(x:1, z:3);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=1, y=None, z=3)>", "测试失败"
print("✓ 通过")

print("\n" + "=" * 60)
print("所有测试通过！")
print("=" * 60)
