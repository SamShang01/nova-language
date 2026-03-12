"""
测试常量折叠详细输出
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.optimizer.optimizer import Optimizer
from nova.compiler.codegen.generator import CodeGenerator

# 测试常量折叠
code = "0.1+0.2;"
print(f"Source code: {code}")

scanner = Scanner(code)
tokens = scanner.scan_tokens()

parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

print("\nBefore optimization:")
print(f"  AST: {ast}")

optimizer = Optimizer()
ast = optimizer.optimize(ast)

print("\nAfter optimization:")
print(f"  AST: {ast}")

codegen = CodeGenerator()
instructions, constants = codegen.generate(ast)

print(f"\nInstructions ({len(instructions)}):")
for offset, instr in enumerate(instructions):
    print(f"  {offset:04X}    {instr}")
    # 检查常量值
    if hasattr(instr, 'args') and len(instr.args) > 0:
        value = instr.args[0]
        print(f"         -> Value: {repr(value)}")
