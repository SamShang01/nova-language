import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.parser.ast import GenericFunctionDefinition

code = """template func apply<T, U>(value: T, fn: func(T): U): U {
    return fn(value);
}"""

print("=== Lexer Output ===")
scanner = Scanner(code)
tokens = scanner.scan_tokens()
for i, token in enumerate(tokens):
    print(f"{i}: {token.type} = '{token.lexeme}' (line {token.line}, col {token.column})")

print("\n=== Parser Output ===")
parser = Parser(tokens)
try:
    ast = parser.parse()
    print("Parse successful!")
    for stmt in ast.statements:
        print(f"Statement type: {type(stmt).__name__}")
        if isinstance(stmt, GenericFunctionDefinition):
            print(f"  Function name: {stmt.name}")
            print(f"  Type params: {[tp.name for tp in stmt.type_params]}")
            print(f"  Params:")
            for param in stmt.params:
                print(f"    - {param.name}: {param.param_type}")
except Exception as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()
