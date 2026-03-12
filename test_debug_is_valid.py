# 调试泛型实例化检测
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
let n = Node<int>(42, true);
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("=== All Tokens ===")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type}: '{token.lexeme}'")

print("\n=== Testing _is_valid_generic_instantiation ===")
parser = Parser(tokens)

# 手动调用 _is_valid_generic_instantiation
# 跳过前面的tokens，到达 Node
while parser.peek().lexeme != 'Node':
    parser.advance()

print(f"Current token: {parser.peek().type}: '{parser.peek().lexeme}'")

# 检查是否是有效的泛型实例化
result = parser._is_valid_generic_instantiation()
print(f"Is valid generic instantiation: {result}")

print("\n=== Parsing ===")
try:
    parser2 = Parser(tokens)
    ast = parser2.parse()
    print("Parse successful!")
except Exception as e:
    print(f"Parse error: {e}")
