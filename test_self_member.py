"""
测试self成员访问
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
func test() {
    return self.x;
}
"""

scanner = Scanner(code)
tokens = scanner.scan_tokens()

for token in tokens:
    print(f"{token.type}: {token.lexeme}")

print("\n开始解析...")
parser = Parser(tokens)
ast = parser.parse()
print("解析成功！")
