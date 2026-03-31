import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator

code = 'type(type);'

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 代码生成
codegen = CodeGenerator()
instructions, constants = codegen.generate(ast)

print('Constants:', constants)
print('Instructions:')
for i, instr in enumerate(instructions):
    print(f'{i:04X}: {instr}')