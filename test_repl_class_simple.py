"""
测试在REPL中使用 class 和访问修饰符（简化版）
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

source_code = """
class Person {
    private var _name: string;
    protected var _id: string;
    public var nationality: string;
    
    public func getName(): string {
        return this._name;
    }
}

print("Class Person defined successfully");
"""

print("=" * 60)
print("测试 class 和访问修饰符在 REPL 中")
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
