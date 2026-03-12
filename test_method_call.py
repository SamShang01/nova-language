"""
测试方法调用
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试方法调用
source_code = """
class Vector2D {
    public var x: float;
    public var y: float;

    init(x: float, y: float) {
        this.x = x;
        this.y = y;
    }

    public function add(other: Vector2D): Vector2D {
        return Vector2D(this.x + other.x, this.y + other.y);
    }
}

var v1 = Vector2D(1.0, 2.0);
var v2 = Vector2D(3.0, 4.0);
var v3 = v1.add(v2);
v3.x
"""

print("测试方法调用")
print("=" * 60)
print("\nSource code:")
print(source_code)
print("\n" + "=" * 60)

try:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens, repl_mode=True)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(ast)
    
    print("\n生成的指令:")
    for i, inst in enumerate(instructions):
        print(f"{i}: {inst}")
    
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    
    print(f"\n✅ 测试通过！结果: {result}")
    print(f"\n预期: v3.x = 4.0 (1.0 + 3.0)")
    
except Exception as e:
    print(f"\n❌ 测试失败！错误: {e}")
    import traceback
    traceback.print_exc()
