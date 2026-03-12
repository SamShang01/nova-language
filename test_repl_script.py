import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine
from nova.vm.errors import VMError

code = """
struct Point {
    x: int;
    y: int;
}

Point(1, 2);
Point(1);
Point();
Point(1, 2, 3);
"""

print("代码:")
print(code)
print("\n开始执行...")

try:
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
    print(f"\n执行结果: {result}")
except VMError as e:
    print(f"\n✓ 正确捕获错误: {e}")
except Exception as e:
    print(f"\n✗ 意外错误: {e}")
    import traceback
    traceback.print_exc()
