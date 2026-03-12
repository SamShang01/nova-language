#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Nova类对象和Feature系统（简化版）
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

print("\n0.5.0版本新增特性:")
print(f"  - AdvancedParameters: {feature_class.get('AdvancedParameters').description}")
print(f"  - ClassObjects: {feature_class.get('ClassObjects').description}")

# 测试2: 简单的struct定义和实例化
test_case("简单的struct定义", """
struct Point {
    x: int;
    y: int;
}

Point();
""")

# 测试3: 测试NovaClass和NovaInstance
print("\n" + "=" * 50)
print("测试NovaClass和NovaInstance")
print("=" * 50)

from nova.vm.machine import NovaClass, NovaInstance

# 创建一个简单的类
point_class = NovaClass("Point", [("x", "int"), ("y", "int")], [])
print(f"NovaClass: {point_class}")

# 实例化
point_instance = point_class()
print(f"NovaInstance: {point_instance}")
print(f"point_instance.x = {point_instance.x}")
print(f"point_instance.y = {point_instance.y}")

# 设置字段值
point_instance.x = 10
point_instance.y = 20
print(f"设置后: point_instance.x = {point_instance.x}, point_instance.y = {point_instance.y}")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)
