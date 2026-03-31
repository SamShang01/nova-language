from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.parser.ast import CallExpression, IdentifierExpression, TypeTypeExpression

code = 'type(type);'

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 检查AST结构
print('AST type:', type(ast))
print('Number of statements:', len(ast.statements))

if ast.statements:
    stmt = ast.statements[0]
    print('First statement type:', type(stmt))
    print('Is CallExpression:', isinstance(stmt, CallExpression))
    
    if isinstance(stmt, CallExpression):
        print('Callee type:', type(stmt.callee))
        print('Callee class name:', stmt.callee.__class__.__name__)
        print('Is TypeTypeExpression:', isinstance(stmt.callee, TypeTypeExpression))
        print('Is IdentifierExpression:', isinstance(stmt.callee, IdentifierExpression))
        
        print('Number of arguments:', len(stmt.arguments))
        if stmt.arguments:
            arg = stmt.arguments[0]
            print('First argument type:', type(arg))
            print('Argument class name:', arg.__class__.__name__)
            print('Is TypeTypeExpression:', isinstance(arg, TypeTypeExpression))
            print('Is IdentifierExpression:', isinstance(arg, IdentifierExpression))
            
            if isinstance(arg, IdentifierExpression):
                print('Argument name:', arg.name)