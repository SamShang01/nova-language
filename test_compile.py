from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.compiler.parser.ast import TypeTypeExpression

code = 'type(123);'

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
    print('Callee type:', type(stmt.callee))
    print('Callee class name:', stmt.callee.__class__.__name__)
    print('Is TypeTypeExpression:', isinstance(stmt.callee, TypeTypeExpression))

# 代码生成
codegen = CodeGenerator()
print('CodeGenerator has visit_TypeTypeExpression:', hasattr(codegen, 'visit_TypeTypeExpression'))
instructions, constants = codegen.generate(ast)

print('Constants:', constants)
print('Instructions:')
for i, instr in enumerate(instructions):
    print(f'{i:04X}: {instr}')