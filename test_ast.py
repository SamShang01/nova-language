from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.parser.ast import CallExpression, IdentifierExpression, LiteralExpression

code = 'type(123);'
scanner = Scanner(code)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()

print('AST type:', type(ast))
print('Number of statements:', len(ast.statements))

if ast.statements:
    stmt = ast.statements[0]
    print('First statement type:', type(stmt))
    print('Is CallExpression:', isinstance(stmt, CallExpression))
    
    if isinstance(stmt, CallExpression):
        print('Callee type:', type(stmt.callee))
        print('Is IdentifierExpression:', isinstance(stmt.callee, IdentifierExpression))
        
        if isinstance(stmt.callee, IdentifierExpression):
            print('Callee name:', stmt.callee.name)
            
        print('Number of arguments:', len(stmt.arguments))
        if stmt.arguments:
            arg = stmt.arguments[0]
            print('First argument type:', type(arg))
            print('Is LiteralExpression:', isinstance(arg, LiteralExpression))
            
            if isinstance(arg, LiteralExpression):
                print('Literal value:', arg.value)
                print('Literal type:', arg.literal_type)