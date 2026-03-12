#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试struct实例化
"""

import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

def execute(code):
    """执行Nova代码"""
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    ast.accept(analyzer)
    generator = CodeGenerator()
    ast.accept(generator)
    vm = VirtualMachine()
    vm.load(generator.instructions)
    return vm.run()

code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2);
"""

print("代码:")
print(code)
print("\n执行结果:")
result = execute(code)
print(result)
