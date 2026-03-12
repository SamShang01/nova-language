"""
测试 class 关键字和访问修饰符
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

def print_ast(node, indent=0):
    """
    打印AST结构
    """
    prefix = "  " * indent
    if node is None:
        print(f"{prefix}None")
        return
    
    node_type = type(node).__name__
    print(f"{prefix}{node_type}")
    
    for attr_name in dir(node):
        if not attr_name.startswith('_'):
            attr_value = getattr(node, attr_name, None)
            if isinstance(attr_value, (str, int, float, bool)):
                print(f"{prefix}  {attr_name}: {repr(attr_value)}")
            elif isinstance(attr_value, list) and len(attr_value) > 0:
                print(f"{prefix}  {attr_name}:")
                for item in attr_value:
                    print_ast(item, indent + 2)
            elif hasattr(attr_value, 'accept'):
                print(f"{prefix}  {attr_name}:")
                print_ast(attr_value, indent + 2)

source_code = """
class Person {
    private var _name: string;
    protected var _id: string;
    public var nationality: string;
    
    public func getName(): string {
        return this._name;
    }
}
"""

print("=" * 60)
print(f"测试 class 和访问修饰符")
print("=" * 60)
print(f"\nSource code:\n{source_code}\n")

try:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    print("Tokens:")
    for token in tokens[:20]:  # 只打印前20个token
        print(f"  {token}")
    print("  ...")
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\n" + "=" * 60)
    print("AST:")
    print("=" * 60)
    print_ast(ast)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
