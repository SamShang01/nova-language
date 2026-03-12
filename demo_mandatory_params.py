#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示强制参数和默认值功能
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
print("Nova 0.5.0 - 强制参数和默认值功能演示")
print("=" * 60)

print("\n1. 强制参数（manda）")
print("-" * 60)
code = """
func greet(manda name: int) -> int {
    return name;
}

greet(10);
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")

print("\n2. 默认值参数（default关键字）")
print("-" * 60)
code = """
func greet(name: int default 10) -> int {
    return name;
}

greet();
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")

print("\n3. 默认值参数（=）")
print("-" * 60)
code = """
func greet(name: int = 10) -> int {
    return name;
}

greet();
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")

print("\n4. 混合使用强制参数和默认值")
print("-" * 60)
code = """
func calculate(manda a: int, b: int default 5, c: int default 10) -> int {
    return a + b + c;
}

calculate(20);
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")

print("\n5. 覆盖默认值")
print("-" * 60)
code = """
func greet(name: int default 10) -> int {
    return name;
}

greet(20);
"""
print(f"代码: {code.strip()}")
result = execute(code)
print(f"结果: {result}")

print("\n6. 强制参数缺失（应该报错）")
print("-" * 60)
code = """
func greet(manda name: int) -> int {
    return name;
}

greet();
"""
print(f"代码: {code.strip()}")
try:
    result = execute(code)
    print(f"结果: {result}")
except Exception as e:
    print(f"✓ 正确捕获错误: {e}")

print("\n" + "=" * 60)
print("演示完成！")
print("=" * 60)
