#!/usr/bin/env python3
# 测试Nova代码执行功能

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试代码
code = 'let a = 1; print(a);'
print(f"Testing code: {code}")

try:
    # 词法分析
    print("Step 1: Lexical analysis")
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    print(f"Tokens: {len(tokens)}")
    
    # 语法分析
    print("Step 2: Syntax analysis")
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST created")
    
    # 语义分析
    print("Step 3: Semantic analysis")
    analyzer = SemanticAnalyzer()
    analyzed_ast = analyzer.analyze(ast)
    print("Semantic analysis completed")
    
    # 代码生成
    print("Step 4: Code generation")
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(analyzed_ast)
    print(f"Instructions: {len(instructions)}")
    print(f"Constants: {constants}")
    
    # 执行
    print("Step 5: Execution")
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    print(f"Execution completed. Result: {result}")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    print(f"Traceback: {traceback.format_exc()}")
