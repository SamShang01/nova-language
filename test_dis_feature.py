"""
测试dis函数 - 特性支持
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试dis函数 - DeferredOperations特性
source_code = """
dis('from __future__ import DeferredOperations;0.1+0.2-0.2;');
"""

print("=" * 60)
print("测试dis函数 - DeferredOperations特性")
print("=" * 60)
print(f"\nSource code:\n{source_code}\n")

try:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    
    print(f"\nResult: {result}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
