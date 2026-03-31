# 测试Nova命令行执行
echo 'Testing Nova command line execution...'

# 测试1: 基本赋值和输出
echo 'Test 1: let a = 1; print(a);'
python -c '
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

code = "let a = 1; print(a);"
scanner = Scanner(code)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzed_ast = analyzer.analyze(ast)
codegen = CodeGenerator()
instructions, constants = codegen.generate(analyzed_ast)
vm = VirtualMachine()
vm.load(instructions, constants)
vm.run()
'

# 测试2: 复杂表达式
echo '
Test 2: let b = 2; print(b * 2);'
python -c '
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

code = "let b = 2; print(b * 2);"
scanner = Scanner(code)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzed_ast = analyzer.analyze(ast)
codegen = CodeGenerator()
instructions, constants = codegen.generate(analyzed_ast)
vm = VirtualMachine()
vm.load(instructions, constants)
vm.run()
'
