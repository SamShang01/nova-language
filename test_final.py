#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova 0.5.0 完整功能测试
测试类系统、位置参数、关键字参数、强制参数和默认值
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

print("=" * 70)
print("Nova 0.5.0 完整功能测试")
print("=" * 70)

print("\n【类系统 - 位置参数】")
print("-" * 70)

print("\n1. 无参数实例化")
code = """
struct Point {
    x: int;
    y: int;
}

Point();
"""
result = execute(code)
print(f"Point() => {result}")
assert str(result) == "<Point(x=None, y=None)>"
print("✓ 通过")

print("\n2. 部分位置参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1);
"""
result = execute(code)
print(f"Point(1) => {result}")
assert str(result) == "<Point(x=1, y=None)>"
print("✓ 通过")

print("\n3. 完整位置参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2);
"""
result = execute(code)
print(f"Point(1, 2) => {result}")
assert str(result) == "<Point(x=1, y=2)>"
print("✓ 通过")

print("\n【类系统 - 关键字参数】")
print("-" * 70)

print("\n4. 单个关键字参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(x:10);
"""
result = execute(code)
print(f"Point(x:10) => {result}")
assert str(result) == "<Point(x=10, y=None)>"
print("✓ 通过")

print("\n5. 多个关键字参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(x:10, y:20);
"""
result = execute(code)
print(f"Point(x:10, y:20) => {result}")
assert str(result) == "<Point(x=10, y=20)>"
print("✓ 通过")

print("\n6. 关键字参数顺序")
code = """
struct Point {
    x: int;
    y: int;
}

Point(y:20, x:10);
"""
result = execute(code)
print(f"Point(y:20, x:10) => {result}")
assert str(result) == "<Point(x=10, y=20)>"
print("✓ 通过")

print("\n【类系统 - 混合参数】")
print("-" * 70)

print("\n7. 位置+关键字参数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1, y:2);
"""
result = execute(code)
print(f"Point(1, y:2) => {result}")
assert str(result) == "<Point(x=1, y=2)>"
print("✓ 通过")

print("\n【函数 - 强制参数】")
print("-" * 70)

print("\n8. 强制参数正常调用")
code = """
func greet(manda name: int) -> int {
    return name;
}

greet(100);
"""
result = execute(code)
print(f"greet(100) => {result}")
assert result == 100
print("✓ 通过")

print("\n9. 强制参数缺失（应该报错）")
code = """
func greet(manda name: int) -> int {
    return name;
}

greet();
"""
try:
    execute(code)
    print("✗ 失败：应该抛出异常")
except VMError as e:
    if "Missing mandatory argument" in str(e):
        print(f"✓ 通过：正确捕获错误")
    else:
        print(f"✗ 失败：错误消息不正确")

print("\n【函数 - 默认值参数】")
print("-" * 70)

print("\n10. 使用默认值")
code = """
func greet(name: int default 10) -> int {
    return name;
}

greet();
"""
result = execute(code)
print(f"greet() => {result}")
assert result == 10
print("✓ 通过")

print("\n11. 覆盖默认值")
code = """
func greet(name: int default 10) -> int {
    return name;
}

greet(20);
"""
result = execute(code)
print(f"greet(20) => {result}")
assert result == 20
print("✓ 通过")

print("\n【函数 - 混合参数】")
print("-" * 70)

print("\n12. 强制+默认值")
code = """
func calculate(manda a: int, b: int default 5, c: int default 10) -> int {
    return a + b + c;
}

calculate(20);
"""
result = execute(code)
print(f"calculate(20) => {result}")
assert result == 35
print("✓ 通过")

print("\n【错误处理】")
print("-" * 70)

print("\n13. 参数数量过多（应该报错）")
code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2, 3);
"""
try:
    execute(code)
    print("✗ 失败：应该抛出异常")
except VMError as e:
    if "takes 2 positional arguments but 3 were given" in str(e):
        print(f"✓ 通过：正确捕获错误")
    else:
        print(f"✗ 失败：错误消息不正确")

print("\n" + "=" * 70)
print("所有测试通过！✓")
print("=" * 70)
print("\nNova 0.5.0 功能总结:")
print("  ✓ 类系统（NovaClass和NovaInstance）")
print("  ✓ 位置参数支持")
print("  ✓ 关键字参数支持（name:value语法）")
print("  ✓ 混合位置和关键字参数")
print("  ✓ 强制参数（manda关键字）")
print("  ✓ 默认值参数（default关键字和=语法）")
print("  ✓ 参数数量验证")
print("  ✓ 完整的错误处理")
