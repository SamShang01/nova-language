#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Nova高级参数系统
"""

import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

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

# 测试1: 普通参数
test_case("普通参数", """
func add(a: int, b: int) -> int {
    return a + b;
}

add(100, 100);
""")

# 测试2: 默认值参数
test_case("默认值参数", """
func greet(name: int, message: int = 10) -> int {
    return message + name;
}

greet(5);
""")

# 测试3: 可变参数
test_case("可变参数", """
func sum_all(*numbers: int) -> int {
    return 0;
}

sum_all(1, 2, 3, 4, 5);
""")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)
