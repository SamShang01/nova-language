"""
测试常量折叠优化
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.optimizer.optimizer import Optimizer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

def test_constant_folding(code, description):
    """
    测试常量折叠
    
    Args:
        code: Nova代码
        description: 描述
    """
    print(f"\n测试: {description}")
    print(f"代码: {code}")
    
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # 优化
        optimizer = Optimizer()
        ast = optimizer.optimize(ast)
        
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(ast)
        
        vm = VirtualMachine()
        vm.load(instructions, constants)
        result = vm.run()
        
        print(f"结果: {result}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("测试常量折叠优化")
    print("=" * 60)
    
    # 测试1: 整数加法
    test_constant_folding("1+2+3;", "整数加法: 1+2+3")
    
    # 测试2: 整数乘法
    test_constant_folding("2*3*4;", "整数乘法: 2*3*4")
    
    # 测试3: 混合运算
    test_constant_folding("1+2*3;", "混合运算: 1+2*3")
    
    # 测试4: 浮点数运算
    test_constant_folding("0.1+0.2;", "浮点数运算: 0.1+0.2")
    
    # 测试5: 变量运算（不应该被优化）
    test_constant_folding("var x = 1; var y = 2; x+y;", "变量运算: x+y（不应该被优化）")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
