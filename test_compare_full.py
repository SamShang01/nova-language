#!/usr/bin/env python
"""
测试 compare 方法的完整代码生成
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator

code = """
class Person {
    let name: string;
    let age: int;
    
    fn __init__(name: string, age: int) {
        this.name = name;
        this.age = age;
    }
}

impl Comparable<Person> for Person {
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

scanner = Scanner(code)
tokens = scanner.scan_tokens()
print("\n词法分析完成")

parser = Parser(tokens)
ast = parser.parse()
print("语法分析完成")

gen = CodeGenerator()
instructions, constants = gen.generate(ast)

print("\n主指令列表:")
for i, instr in enumerate(instructions):
    print(f"  {i}: {instr}")
    if instr.opcode == "LOAD_CONST":
        const = instr.args[0]
        if hasattr(const, 'name') and hasattr(const, 'methods'):
            print(f"    类名: {const.name}")
            print(f"    方法:")
            for method in const.methods:
                print(f"      {method}")
                if hasattr(method, '__len__') and len(method) >= 2:
                    method_name = method[0] if isinstance(method[0], str) else getattr(method[0], 'name', '?')
                    method_obj = method[1] if len(method) >= 2 else method[0]
                    if hasattr(method_obj, 'instructions'):
                        print(f"        方法 {method_name} 的指令:")
                        for j, instr2 in enumerate(method_obj.instructions):
                            print(f"          {j}: {instr2}")
                            if 'COMPARE' in str(instr2):
                                print(f"            ^^^ 找到比较指令: {instr2}")
