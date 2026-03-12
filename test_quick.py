import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2);
"""

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
result = vm.run()

print("结果:", result)
