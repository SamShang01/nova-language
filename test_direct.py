#!/usr/bin/env python3
# 直接测试execute_nova_code方法

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试代码
code_samples = [
    'let a = 1;',
    'a;',
    'print(1);',
    'let b = 2; print(b);'
]

for code in code_samples:
    print(f"\nTesting code: '{code}'")
    try:
        # 词法分析
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        print(f'Tokens: {len(tokens)}')
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        print('AST created')
        
        # 语义分析
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        print('Semantic analysis completed')
        
        # 代码生成
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(analyzed_ast)
        print(f'Instructions: {len(instructions)}')
        
        # 执行
        vm = VirtualMachine()
        vm.load(instructions, constants)
        result = vm.run()
        print(f'Execution completed. Result: {result}')
        
    except Exception as e:
        import traceback
        print(f'Error: {e}')
        print(f'Traceback: {traceback.format_exc()}')
