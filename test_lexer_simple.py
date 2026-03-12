import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.lexer.tokens import TokenType

code = """template func test<T, U>(a: T, b: U): U {
    return b;
}"""

scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("Tokens:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type} = '{token.lexeme}' (line {token.line}, col {token.column})")
