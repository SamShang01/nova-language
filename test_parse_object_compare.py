#!/usr/bin/env python
"""
解析 test_object_compare.nova 文件，查看 AST
"""

import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

# 读取 test_object_compare.nova 文件
with open('test_object_compare.nova', 'r', encoding='utf-8') as f:
    code = f.read()

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 打印 AST
print("AST:")
for stmt in ast.statements:
    print(f"  {type(stmt).__name__}: {getattr(stmt, 'name', None)}")
    if hasattr(stmt, 'methods'):
        print(f"    methods: {stmt.methods}")
        for method_info in stmt.methods:
            if isinstance(method_info, tuple):
                method, access_modifier = method_info
                print(f"      method: {method.name}, access: {access_modifier}")
                if hasattr(method, 'body'):
                    print(f"        body: {method.body}")
            else:
                print(f"      method: {method_info}")
    if hasattr(stmt, 'init_method') and stmt.init_method:
        print(f"    init_method: {stmt.init_method.name}")
