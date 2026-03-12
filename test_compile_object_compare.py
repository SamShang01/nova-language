#!/usr/bin/env python
"""
编译 test_object_compare.nova 文件，查看指令序列
"""

import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator

# 读取 test_object_compare.nova 文件
with open('test_object_compare.nova', 'r', encoding='utf-8') as f:
    code = f.read()

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 代码生成
generator = CodeGenerator()
for node in ast.statements:
    node.accept(generator)

# 打印指令序列
print("指令序列:")
for i, instr in enumerate(generator.instructions):
    print(f"{i}: {instr}")

# 打印常量
print("\n常量:")
for i, const in enumerate(generator.constants):
    print(f"{i}: {const}")
