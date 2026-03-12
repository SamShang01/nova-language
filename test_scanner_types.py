"""
测试scanner对类型关键字的识别
"""

from nova.compiler.lexer.scanner import Scanner

code = """
union { int; float; string }
"""

scanner = Scanner(code)
tokens = scanner.scan_tokens()

for token in tokens:
    print(f"{token.type}: {token.lexeme}")
