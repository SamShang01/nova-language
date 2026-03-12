"""
测试DeferredOperations特性的行为
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

def test_expression(code, description):
    """
    测试表达式
    
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
        analyzed_ast = analyzer.analyze(ast)
        
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(analyzed_ast)
        
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
    print("测试浮点数运算行为")
    print("=" * 60)
    
    # 测试1: 未启用DeferredOperations时，0.1+0.2应该返回0.30000000000000004
    test_expression("0.1+0.2;", "未启用DeferredOperations: 0.1+0.2")
    
    # 测试2: 未启用DeferredOperations时，0.1+0.2-0.2应该返回0.10000000000000003
    test_expression("0.1+0.2-0.2;", "未启用DeferredOperations: 0.1+0.2-0.2")
    
    # 测试3: 启用DeferredOperations后，0.1+0.2-0.2应该返回0.1
    test_expression("from __future__ import DeferredOperations; 0.1+0.2-0.2;", "启用DeferredOperations: 0.1+0.2-0.2")
    
    # 测试4: 启用DeferredOperations后，0.1+0.2应该返回0.30000000000000004（保留浮点数精度问题）
    test_expression("from __future__ import DeferredOperations; 0.1+0.2;", "启用DeferredOperations: 0.1+0.2")
    
    # 测试5: 三个操作的抵消模式
    test_expression("from __future__ import DeferredOperations; 0.1+0.2+0.3-0.2;", "启用DeferredOperations: 0.1+0.2+0.3-0.2 (应该返回0.4)")
    test_expression("from __future__ import DeferredOperations; 0.1+0.2-0.3-0.2;", "启用DeferredOperations: 0.1+0.2-0.3-0.2 (应该返回-0.2)")
    test_expression("from __future__ import DeferredOperations; 0.1-0.2+0.3+0.2;", "启用DeferredOperations: 0.1-0.2+0.3+0.2 (应该返回0.4)")
    test_expression("from __future__ import DeferredOperations; 0.1-0.2-0.3+0.2;", "启用DeferredOperations: 0.1-0.2-0.3+0.2 (应该返回-0.2)")
    
    # 测试6: 四个操作的抵消模式
    test_expression("from __future__ import DeferredOperations; 0.1+0.2+0.3+0.4-0.2;", "启用DeferredOperations: 0.1+0.2+0.3+0.4-0.2 (应该返回0.8)")
    test_expression("from __future__ import DeferredOperations; 0.1+0.2+0.3-0.4+0.4;", "启用DeferredOperations: 0.1+0.2+0.3-0.4+0.4 (应该返回0.6)")
    test_expression("from __future__ import DeferredOperations; 0.1-0.2+0.3-0.4+0.2;", "启用DeferredOperations: 0.1-0.2+0.3-0.4+0.2 (应该返回0.0)")
    
    # 测试7: 多个抵消对
    test_expression("from __future__ import DeferredOperations; 0.1+0.2-0.2+0.3-0.3;", "启用DeferredOperations: 0.1+0.2-0.2+0.3-0.3 (应该返回0.1)")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
