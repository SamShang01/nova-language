#!/usr/bin/env python
"""
调试 CodeGenerator 类的 visit_ClassDefinition 方法
"""

import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator

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

# 找到 ClassDefinition 节点
for node in ast.statements:
    if hasattr(node, 'methods'):
        print(f"ClassDefinition: {node.name}")
        print(f"  methods: {node.methods}")
        for method_info in node.methods:
            if isinstance(method_info, tuple):
                method, access_modifier = method_info
                print(f"  method: {method.name}, access: {access_modifier}")
                print(f"    params: {method.params}")
                print(f"    body: {method.body}")
                
                # 生成方法指令
                method_instructions = []
                old_instructions = generator.instructions
                generator.instructions = method_instructions
                
                if method.body:
                    for stmt in method.body:
                        stmt.accept(generator)
                
                generator.instructions = old_instructions
                print(f"    instructions: {method_instructions}")
