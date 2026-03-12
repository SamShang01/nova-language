#!/usr/bin/env python
"""
测试二元表达式代码生成 - 检查函数体内部指令
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

print("\n主指令列表:")
for i, instr in enumerate(instructions):
    print(f"  {i}: {instr}")

# 检查常量中的函数对象
print("\n常量列表:")
for i, const in enumerate(constants):
    print(f"  {i}: {const}")
    # 检查是否是函数对象
    if hasattr(const, 'name') and hasattr(const, 'instructions'):
        print(f"    函数名: {const.name}")
        print(f"    函数体指令:")
        for j, instr in enumerate(const.instructions):
            print(f"      {j}: {instr}")
            if 'COMPARE' in str(instr):
                print(f"        ^^^ 找到比较指令: {instr}")

# 检查是否有 COMPARE_GE 指令
all_instructions = list(instructions)
for const in constants:
    if hasattr(const, 'instructions'):
        all_instructions.extend(const.instructions)

has_compare_ge = any('COMPARE_GE' in str(instr) for instr in all_instructions)
has_compare_lt = any('COMPARE_LT' in str(instr) for instr in all_instructions)

print(f"\n包含 COMPARE_GE 指令: {has_compare_ge}")
print(f"包含 COMPARE_LT 指令: {has_compare_lt}")
