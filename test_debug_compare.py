#!/usr/bin/env python
"""
调试 compare 方法
"""

import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer import Scanner
from nova.compiler.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

# 读取测试文件
with open('test_object_compare.nova', 'r', encoding='utf-8') as f:
    source = f.read()

print("=" * 60)
print("源代码:")
print("=" * 60)
print(source)
print()

# 词法分析
print("=" * 60)
print("词法分析...")
print("=" * 60)
lexer = Scanner(source)
tokens = lexer.scan_tokens()
print(f"Token 数量: {len(tokens)}")
print()

# 语法分析
print("=" * 60)
print("语法分析...")
print("=" * 60)
parser = Parser(tokens)
ast = parser.parse()
print(f"AST 类型: {type(ast)}")
if hasattr(ast, 'statements'):
    print(f"AST 语句数量: {len(ast.statements)}")
elif hasattr(ast, 'body'):
    print(f"AST 语句数量: {len(ast.body)}")
else:
    print(f"AST 属性: {dir(ast)}")
print()

# 语义分析
print("=" * 60)
print("语义分析...")
print("=" * 60)
analyzer = SemanticAnalyzer()
try:
    analyzer.analyze(ast)
    print("语义分析通过!")
except Exception as e:
    print(f"语义分析错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# 代码生成
print("=" * 60)
print("代码生成...")
print("=" * 60)
generator = CodeGenerator()
instructions = generator.generate(ast)
print(f"指令数量: {len(instructions)}")
print()

# 打印指令
print("=" * 60)
print("指令列表:")
print("=" * 60)
for i, instr in enumerate(instructions):
    print(f"{i}: {instr}")
print()

# 查找 compare 方法的指令
print("=" * 60)
print("查找 compare 方法的指令...")
print("=" * 60)
for i, instr in enumerate(instructions):
    if 'compare' in str(instr).lower():
        print(f"{i}: {instr}")
print()
