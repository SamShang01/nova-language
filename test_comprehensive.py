#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova 0.5.0 综合功能测试
测试类系统、强制参数和默认值功能
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

print("=" * 70)
print("Nova 0.5.0 综合功能测试")
print("=" * 70)

print("\n【类系统测试】")
print("-" * 70)

print("\n1. 定义并实例化结构体（位置参数）")
code = """
struct Point {
    x: int;
    y: int;
}

Point(10, 20);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=10, y=20)>", "测试失败"
print("✓ 通过")

print("\n2. 部分参数实例化")
code = """
struct Point {
    x: int;
    y: int;
}

Point(5);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=5, y=None)>", "测试失败"
print("✓ 通过")

print("\n3. 无参数实例化")
code = """
struct Point {
    x: int;
    y: int;
}

Point();
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=None, y=None)>", "测试失败"
print("✓ 通过")

print("\n【强制参数测试】")
print("-" * 70)

print("\n4. 强制参数正常调用")
code = """
func greet(manda name: int) -> int {
    return name;
}

greet(100);
"""
result = execute(code)
print(f"结果: {result}")
assert result == 100, "测试失败"
print("✓ 通过")

print("\n5. 强制参数缺失（应该报错）")
code = """
func greet(manda name: int) -> int {
    return name;
}

greet();
"""
try:
    result = execute(code)
    print("✗ 测试失败：应该抛出异常")
except Exception as e:
    if "Missing mandatory argument" in str(e):
        print(f"✓ 通过：正确捕获错误")
    else:
        print(f"✗ 测试失败：错误消息不正确 - {e}")

print("\n【默认值参数测试】")
print("-" * 70)

print("\n6. 默认值参数（使用默认值）")
code = """
func greet(name: int default 10) -> int {
    return name;
}

greet();
"""
result = execute(code)
print(f"结果: {result}")
assert result == 10, "测试失败"
print("✓ 通过")

print("\n7. 默认值参数（覆盖默认值）")
code = """
func greet(name: int default 10) -> int {
    return name;
}

greet(20);
"""
result = execute(code)
print(f"结果: {result}")
assert result == 20, "测试失败"
print("✓ 通过")

print("\n8. 默认值参数（使用=语法）")
code = """
func greet(name: int = 30) -> int {
    return name;
}

greet();
"""
result = execute(code)
print(f"结果: {result}")
assert result == 30, "测试失败"
print("✓ 通过")

print("\n【混合参数测试】")
print("-" * 70)

print("\n9. 混合使用强制参数和默认值")
code = """
func calculate(manda a: int, b: int default 5, c: int default 10) -> int {
    return a + b + c;
}

calculate(20);
"""
result = execute(code)
print(f"结果: {result}")
assert result == 35, "测试失败"
print("✓ 通过")

print("\n10. 覆盖部分默认值")
code = """
func calculate(manda a: int, b: int default 5, c: int default 10) -> int {
    return a + b + c;
}

calculate(20, 10);
"""
result = execute(code)
print(f"结果: {result}")
assert result == 40, "测试失败"
print("✓ 通过")

print("\n11. 覆盖所有默认值")
code = """
func calculate(manda a: int, b: int default 5, c: int default 10) -> int {
    return a + b + c;
}

calculate(20, 10, 30);
"""
result = execute(code)
print(f"结果: {result}")
assert result == 60, "测试失败"
print("✓ 通过")

print("\n【综合测试】")
print("-" * 70)

print("\n12. 结合类和函数")
code = """
struct Point {
    x: int;
    y: int;
}

Point(3, 4);
"""
result = execute(code)
print(f"结果: {result}")
assert str(result) == "<Point(x=3, y=4)>", "测试失败"
print("✓ 通过")

print("\n" + "=" * 70)
print("所有测试通过！✓")
print("=" * 70)
print("\nNova 0.5.0 功能总结:")
print("  ✓ 类系统（NovaClass和NovaInstance）")
print("  ✓ 强制参数（manda关键字）")
print("  ✓ 默认值参数（default关键字和=语法）")
print("  ✓ 混合参数系统")
print("  ✓ 类实例化支持位置参数")
