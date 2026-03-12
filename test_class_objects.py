#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Nova类对象和Feature系统
"""

import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine
from nova.compiler.features import get_feature_class

def test_case(name, code):
    print(f"\n测试: {name}")
    print("=" * 50)
    print("代码:")
    print(code)
    print("=" * 50)
    
    try:
        # 词法分析
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()

        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()

        # 语义分析
        analyzer = SemanticAnalyzer()
        ast.accept(analyzer)

        # 代码生成
        generator = CodeGenerator()
        ast.accept(generator)

        # 执行
        vm = VirtualMachine()
        vm.load(generator.instructions)
        result = vm.run()

        print(f"✓ 执行成功，结果: {result}")
        return True
    except Exception as e:
        print(f"✗ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False

# 测试1: Feature类对象
print("\n" + "=" * 50)
print("测试Feature类对象")
print("=" * 50)

feature_class = get_feature_class()
print(f"Feature类: {feature_class}")
print(f"所有特性数量: {len(feature_class.list_all())}")
print(f"启用的特性数量: {len(feature_class.list_enabled())}")

print("\n启用的特性:")
for feature in feature_class.list_enabled():
    print(f"  - {feature.name}: {feature.description}")

print("\n可用特性:")
for feature in feature_class.list_available((0, 5, 0)):
    status = "✓" if feature.enabled else "✗"
    print(f"  {status} {feature.name}: {feature.description}")

# 测试2: 简单的struct定义
test_case("简单的struct定义", """
struct Point {
    x: int;
    y: int;
}

Point();
""")

# 测试3: struct实例化（简化版）
test_case("struct实例化", """
struct Point {
    x: int;
    y: int;
}

let p = Point();
p.x = 10;
p.y = 20;
p;
""")

# 测试4: 带方法的struct（简化版）
test_case("带方法的struct", """
struct Counter {
    count: int;
}

Counter(count=0);
""")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)
