#!/usr/bin/env python
"""
调试 test_object_compare.nova 的编译结果
"""

import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 读取源代码
with open('test_object_compare.nova', 'r', encoding='utf-8') as f:
    source_code = f.read()

# 词法分析
scanner = Scanner(source_code)
tokens = scanner.scan_tokens()

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 代码生成
generator = CodeGenerator()
generator.generate(ast)

# 打印生成的指令
print("生成的全局指令:")
for i, instr in enumerate(generator.instructions):
    print(f"{i}: {instr}")
    print(f"   type: {type(instr)}")
    print(f"   args: {instr.args}")
    if instr.args:
        value = instr.args[0]
        print(f"   value: {value}")
        print(f"   value type: {type(value)}")
        if hasattr(value, 'methods'):
            print(f"   methods: {value.methods}")
            for method_name, method, access_modifier, is_abstract in value.methods:
                print(f"     {method_name}: {method}")
                if hasattr(method, 'instructions'):
                    print(f"       instructions:")
                    for j, mi in enumerate(method.instructions):
                        print(f"         {j}: {mi}")
