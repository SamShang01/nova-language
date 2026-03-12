#!/usr/bin/env python
"""
调试 CodeGenerator 类的 visit_ClassDefinition 方法
"""

import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import NovaClass

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

# 检查 NovaClass 对象
for instr in generator.instructions:
    if hasattr(instr, 'args') and len(instr.args) > 0:
        arg = instr.args[0]
        if isinstance(arg, NovaClass):
            print(f"\nNovaClass: {arg.name}")
            print(f"  methods: {arg.methods}")
            for method_item in arg.methods:
                if isinstance(method_item, tuple) and len(method_item) >= 2:
                    method_name = method_item[0]
                    method_func = method_item[1]
                    print(f"  method: {method_name}")
                    print(f"    func: {method_func}")
                    if hasattr(method_func, 'instructions'):
                        print(f"    instructions: {method_func.instructions}")
