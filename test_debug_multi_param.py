# 调试多参数泛型结构体实例化
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
template struct Node<T> {
    var value: T;
    var isValid: bool;
}

let n = Node<int>(42, true);
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("=== All Tokens ===")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type}: '{token.lexeme}'")

print("\n=== Parsing ===")
try:
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parse successful!")
except Exception as e:
    print(f"Parse error: {e}")
