#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Nova函数参数系统
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试代码
code = """
func add(a: int, b: int) -> int {
    return a + b;
}

add(100, 100);
"""

print("测试Nova函数参数系统")
print("=" * 50)
print("代码:")
print(code)
print("=" * 50)

# 词法分析
print("1. 词法分析...")
scanner = Scanner(code)
tokens = scanner.scan_tokens()
print(f"   Token数量: {len(tokens)}")

# 语法分析
print("2. 语法分析...")
parser = Parser(tokens)
ast = parser.parse()
print(f"   AST节点数量: {len(ast.body)}")

# 语义分析
print("3. 语义分析...")
analyzer = SemanticAnalyzer()
ast.accept(analyzer)
print("   语义分析完成")

# 代码生成
print("4. 代码生成...")
generator = CodeGenerator()
ast.accept(generator)
print(f"   指令数量: {len(generator.instructions)}")

# 执行
print("5. 执行...")
vm = VirtualMachine()
vm.load(generator.instructions)
result = vm.run()

print("=" * 50)
print(f"执行结果: {result}")
print("=" * 50)
