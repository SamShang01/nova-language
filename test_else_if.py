#!/usr/bin/env python
"""
测试 else if 语句的代码生成
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator

# 测试代码 - 测试 else if 语句
code = """
fn test() {
    let a = 35;
    let b = 30;
    if a < b {
        print("a < b");
    } else if a > b {
        print("a > b");
    } else {
        print("a == b");
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

# 检查函数对象
for i, instr in enumerate(instructions):
    if instr.opcode == "LOAD_CONST":
        const = instr.args[0]
        if hasattr(const, 'instructions'):
            print(f"\n函数 {const.name} 的指令:")
            for j, instr2 in enumerate(const.instructions):
                print(f"  {j}: {instr2}")
                if 'COMPARE' in str(instr2):
                    print(f"    ^^^ 找到比较指令: {instr2}")
