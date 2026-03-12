"""
测试print函数
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试代码
code = "print(21);"

try:
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    print("Tokens:")
    for token in tokens:
        if token.type.name == 'EOF':
            break
        print(f"  {token.type.name}: '{token.lexeme}'")
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\nAST:")
    print(ast)
    
    analyzer = SemanticAnalyzer()
    analyzed_ast = analyzer.analyze(ast)
    
    print("\nAnalyzed AST:")
    print(analyzed_ast)
    
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(analyzed_ast)
    
    print("\nInstructions:")
    for i, instr in enumerate(instructions):
        print(f"  {i}: {instr}")
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"\nResult: {result}")
    print(f"Environment: {vm.environment}")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
