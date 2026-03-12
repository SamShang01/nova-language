# 调试指针解析
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
func main() {
    let x = 42;
    let ptr = &x;
    let value = *ptr;
    print(value);
}
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("=== Tokens ===")
for token in tokens:
    print(f"{token.type}: {token.lexeme}")

print("\n=== Parsing ===")
try:
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parse successful!")
except Exception as e:
    print(f"Parse error: {e}")
