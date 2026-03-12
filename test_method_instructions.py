"""
测试方法指令生成
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

# 测试方法指令生成
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
"""

print("测试方法指令生成")
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
    
    print("\n常量池中的类对象:")
    for i, const in enumerate(constants):
        print(f"{i}: {type(const).__name__} = {const}")
        if hasattr(const, 'methods'):
            print(f"   方法:")
            for method in const.methods:
                if isinstance(method, tuple):
                    name, func, access, is_abstract = method
                    print(f"     - {name}: {type(func).__name__ if func else 'None'}")
                    if func and hasattr(func, 'instructions'):
                        print(f"       指令: {func.instructions}")
    
except Exception as e:
    print(f"\n❌ 测试失败！错误: {e}")
    import traceback
    traceback.print_exc()
