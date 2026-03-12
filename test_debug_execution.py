"""
测试 __add__ 方法执行调试
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试 __add__ 方法执行调试
source_code = """
class Vector2D {
    public var x: float;
    public var y: float;

    init(x: float, y: float) {
        this.x = x;
        this.y = y;
    }

    public function __add__(other: Vector2D): Vector2D {
        return Vector2D(this.x + other.x, this.y + other.y);
    }
}

var v1 = Vector2D(1.0, 2.0);
var v2 = Vector2D(3.0, 4.0);
"""

print("测试 __add__ 方法执行调试")
print("=" * 60)

try:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens, repl_mode=True)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions, constants)
    vm.run()
    
    # 获取 v1 和 v2
    v1 = vm.environment.get('v1')
    v2 = vm.environment.get('v2')
    
    print(f"v1 = {v1}")
    print(f"v1.fields = {v1.fields}")
    print(f"v2 = {v2}")
    print(f"v2.fields = {v2.fields}")
    
    # 手动调用 __add__ 方法
    print("\n手动调用 v1.__add__(v2):")
    result = v1.__add__(v2)
    print(f"result = {result}")
    print(f"result.fields = {result.fields}")
    
except Exception as e:
    print(f"\n❌ 测试失败！错误: {e}")
    import traceback
    traceback.print_exc()
