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
if ast.statements:
    stmt = ast.statements[0]
    
    if isinstance(stmt, CallExpression):
        print('Callee TypeTypeExpression:')
        callee = stmt.callee
        print('  Type:', type(callee))
        print('  Has wrapped_type:', hasattr(callee, 'wrapped_type'))
        if hasattr(callee, 'wrapped_type'):
            print('  wrapped_type:', callee.wrapped_type)
            print('  wrapped_type type:', type(callee.wrapped_type))
            if hasattr(callee.wrapped_type, 'name'):
                print('  wrapped_type.name:', callee.wrapped_type.name)
        
        print('\nArgument TypeTypeExpression:')
        arg = stmt.arguments[0]
        print('  Type:', type(arg))
        print('  Has wrapped_type:', hasattr(arg, 'wrapped_type'))
        if hasattr(arg, 'wrapped_type'):
            print('  wrapped_type:', arg.wrapped_type)
            print('  wrapped_type type:', type(arg.wrapped_type))
            if hasattr(arg.wrapped_type, 'name'):
                print('  wrapped_type.name:', arg.wrapped_type.name)