#!/usr/bin/env python
"""
调试测试 - 追踪 '>=' 错误
"""

import sys
import traceback

# 补丁 COMPARE_GT 指令，添加更多调试信息
from nova.vm import instructions

original_compare_gt_execute = instructions.COMPARE_GT.execute

def patched_compare_gt_execute(self, vm):
    print("[PATCHED COMPARE_GT] 被调用!")
    right = vm.stack.pop()
    left = vm.stack.pop()
    print(f"[PATCHED COMPARE_GT] left: {left!r}, type: {type(left)}")
    print(f"[PATCHED COMPARE_GT] right: {right!r}, type: {type(right)}")
    
    # 打印调用栈
    print("[PATCHED COMPARE_GT] 调用栈:")
    for line in traceback.format_stack():
        print(line.strip())
    
    vm.stack.append(left)
    vm.stack.append(right)
    return original_compare_gt_execute(self, vm)

instructions.COMPARE_GT.execute = patched_compare_gt_execute

# 现在运行测试
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

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

fn main() {
    let bob = Person("Bob", 35);
    let john = Person("John", 30);
    let result = bob.compare(john);
    print("Result: " + str(result));
}
"""

print("测试代码:")
print(code)
print("\n" + "="*50 + "\n")

scanner = Scanner(code)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
gen = CodeGenerator()
instructions_list, constants = gen.generate(ast)

print("生成的指令:")
for i, instr in enumerate(instructions_list):
    print(f"  {i}: {instr}")

print("\n" + "="*50 + "\n")

vm = VirtualMachine()
vm.load(instructions_list)

try:
    result = vm.run()
    print(f"\n最终结果: {result}")
except Exception as e:
    print(f"\n错误: {e}")
    traceback.print_exc()
