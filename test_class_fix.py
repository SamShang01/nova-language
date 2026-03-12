#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试类系统修复
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
print("测试类系统修复")
print("=" * 60)

print("\n1. 使用位置参数实例化")
print("-" * 60)
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

print("\n2. 使用位置参数实例化（多个参数）")
print("-" * 60)
code = """
struct Point {
    x: int;
    y: int;
}

Point(10, 20);
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")

print("\n3. 部分参数（使用默认值None）")
print("-" * 60)
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

print("\n4. 无参数实例化")
print("-" * 60)
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

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
