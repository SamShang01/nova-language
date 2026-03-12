"""
测试if语句的词法分析
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.lexer.tokens import TokenType

# 测试代码
code = """
if x > 0 {
    return x;
} else {
    return -x;
}
"""

# 创建扫描器
scanner = Scanner(code)

# 扫描Token
tokens = scanner.scan_tokens()

# 打印Token
print("Token列表:")
for token in tokens:
    if token.type == TokenType.EOF:
        break
    print(f"Type: {token.type.name}, Lexeme: '{token.lexeme}', Line: {token.line}, Column: {token.column}")
