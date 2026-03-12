"""
测试结构体方法中的self成员访问
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
struct Point {
    x: int;
    y: int;
    func distance() -> int {
        return self.x;
    }
}
"""

scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("Tokens:")
for token in tokens:
    print(f"{token.type}: {token.lexeme}")

print("\n开始解析...")
parser = Parser(tokens)
ast = parser.parse()
print("解析成功！")
