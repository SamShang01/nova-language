"""
Nova字节码反汇编模块

类似于Python的dis模块，用于查看Nova字节码
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.optimizer.optimizer import Optimizer
from nova.compiler.codegen.generator import CodeGenerator

def dis(source_code, optimize=True):
    """
    反汇编Nova源代码，显示字节码
    
    Args:
        source_code: Nova源代码
        optimize: 是否启用优化，默认为True
    """
    print(f"Source code:\n  {source_code.strip()}\n")
    
    # 词法分析
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    # 语法分析
    parser = Parser(tokens)
    ast = parser.parse()
    
    # 语义分析
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # 优化（可选）
    if optimize:
        optimizer = Optimizer()
        ast = optimizer.optimize(ast)
        print("Optimization: ENABLED")
    else:
        print("Optimization: DISABLED")
    
    # 代码生成
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(ast)
    
    print(f"\nConstants ({len(constants)}):")
    for i, const in enumerate(constants):
        print(f"  {i}: {repr(const)}")
    
    print(f"\nInstructions ({len(instructions)}):")
    print("  Offset  Instruction")
    print("  " + "-" * 50)
    
    for offset, instr in enumerate(instructions):
        print(f"  {offset:04X}    {instr}")
    
    print()

def dis_file(filename, optimize=True):
    """
    反汇编Nova文件
    
    Args:
        filename: Nova文件路径
        optimize: 是否启用优化，默认为True
    """
    with open(filename, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    print(f"File: {filename}")
    dis(source_code, optimize)

# 便捷的函数别名
disassemble = dis
