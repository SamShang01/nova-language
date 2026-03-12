"""
测试 LOAD_CONST 指令内容
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

# 测试 LOAD_CONST 指令内容
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
"""

print("测试 LOAD_CONST 指令内容")
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
    
    print("\n指令列表:")
    for i, inst in enumerate(instructions):
        print(f"  {i}: {inst}")
        if hasattr(inst, 'args') and inst.args:
            for j, arg in enumerate(inst.args):
                print(f"     args[{j}]: {type(arg).__name__} = {arg}")
                if hasattr(arg, 'methods'):
                    print(f"       methods:")
                    for method in arg.methods:
                        if isinstance(method, tuple):
                            name, func, access, is_abstract = method
                            print(f"         - {name}: {type(func).__name__}")
                            if hasattr(func, 'instructions'):
                                for k, inst2 in enumerate(func.instructions):
                                    print(f"           {k}: {inst2}")
    
except Exception as e:
    print(f"\n❌ 测试失败！错误: {e}")
    import traceback
    traceback.print_exc()
