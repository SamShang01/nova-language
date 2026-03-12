#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试强制参数和默认值功能
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

# 测试1: 强制参数
test_case("强制参数", """
func greet(manda name: int) -> int {
    return name;
}

greet(10);
""")

# 测试2: 强制参数缺失
test_case("强制参数缺失", """
func greet(manda name: int) -> int {
    return name;
}

greet();
""")

# 测试3: 默认值参数（使用default关键字）
test_case("默认值参数（default关键字）", """
func greet(name: int default 10) -> int {
    return name;
}

greet();
""")

# 测试4: 默认值参数（使用=）
test_case("默认值参数（=）", """
func greet(name: int = 10) -> int {
    return name;
}

greet();
""")

# 测试5: 混合使用
test_case("混合使用强制参数和默认值", """
func calculate(manda a: int, b: int default 5, c: int default 10) -> int {
    return a + b + c;
}

calculate(20);
""")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)
