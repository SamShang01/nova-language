#!/usr/bin/env python
"""
测试 compare 方法的代码生成
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator

# 测试代码 - 直接测试 compare 方法
code = """
class Person {
    let name: string;
    let age: int;
    
    fn __init__(name: string, age: int) {
        this.name = name;
        this.age = age;
    }
    
    fn compare(other: Person): int {
        if this.age < other.age {
            return -1;
        } else if this.age > other.age {
            return 1;
        } else {
            return 0;
        }
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

# 检查常量中的类对象
print("\n常量列表:")
for i, const in enumerate(constants):
    print(f"  {i}: {const}")
    # 检查是否是类对象
    if hasattr(const, 'name') and hasattr(const, 'methods'):
        print(f"    类名: {const.name}")
        print(f"    方法:")
        for method in const.methods:
            print(f"      {method}")
            # 检查方法是否是函数对象
            if hasattr(method, '__len__'):
                # 方法是元组
                if len(method) >= 2:
                    method_name = method[0] if isinstance(method[0], str) else getattr(method[0], 'name', '?')
                    method_obj = method[1] if len(method) >= 2 else method[0]
                    print(f"        方法名: {method_name}")
                    if hasattr(method_obj, 'instructions'):
                        print(f"        方法体指令:")
                        for j, instr in enumerate(method_obj.instructions):
                            print(f"          {j}: {instr}")
                            if 'COMPARE' in str(instr):
                                print(f"            ^^^ 找到比较指令: {instr}")
