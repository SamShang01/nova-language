# 调试方法参数
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
template class Container<T> {
    var value: T;
    var isValid: bool;
    
    init(v: T) {
        this.value = v;
        this.isValid = true;
    }
    
    func check() {
        if this.isValid {
            print("Valid");
        }
    }
}
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("=== Parsing ===")
parser = Parser(tokens)
ast = parser.parse()

print("\n=== AST Structure ===")
for stmt in ast.statements:
    if hasattr(stmt, 'methods'):
        print(f"Class: {stmt.name}")
        for method, access in stmt.methods:
            print(f"  Method: {method.name}")
            print(f"    Params:")
            for param in method.params:
                print(f"      {param.name}: {param.type_}")
