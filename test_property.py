"""
测试属性访问器 - getter 和 setter
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试属性访问器
source_code = """
class Rectangle {
    private var width: float;
    private var height: float;
    
    init(width: float, height: float) {
        this.width = width;
        this.height = height;
    }
    
    public function get_area(): float {
        return this.width * this.height;
    }
    
    public function set_width(w: float) {
        this.width = w;
    }
    
    public function get_width(): float {
        return this.width;
    }
}

var rect = Rectangle(5.0, 3.0);
rect.get_area()
"""

print("测试属性访问器 - getter 和 setter")
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
    
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    
    print(f"\n✅ 测试通过！结果: {result}")
    
except Exception as e:
    print(f"\n❌ 测试失败！错误: {e}")
    import traceback
    traceback.print_exc()
