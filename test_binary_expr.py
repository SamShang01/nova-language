#!/usr/bin/env python
"""
测试二元表达式代码生成
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.instructions import COMPARE_GE, COMPARE_LT

# 测试代码
code = """
fn test() {
    let a = 35;
    let b = 30;
    if a >= b {
        print("a >= b");
    }
}
"""

print("测试代码:")
print(code)

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()
print("\n词法分析完成")

# 语法分析
parser = Parser(tokens)
ast = parser.parse()
print("语法分析完成")

# 代码生成
gen = CodeGenerator()
instructions, constants = gen.generate(ast)

print("\n生成的指令:")
for i, instr in enumerate(instructions):
    print(f"  {i}: {instr}")
    if 'COMPARE' in str(instr):
        print(f"    ^^^ 找到比较指令: {instr}")

# 检查是否有 COMPARE_GE 指令
has_compare_ge = any('COMPARE_GE' in str(instr) for instr in instructions)
has_compare_lt = any('COMPARE_LT' in str(instr) for instr in instructions)

print(f"\n包含 COMPARE_GE 指令: {has_compare_ge}")
print(f"包含 COMPARE_LT 指令: {has_compare_lt}")
