"""
测试优化调试 - 查看优化过程
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.optimizer.optimizer import Optimizer
from nova.compiler.features import get_feature_manager

def print_ast(node, indent=0):
    """
    打印AST结构
    
    Args:
        node: AST节点
        indent: 缩进级别
    """
    prefix = "  " * indent
    if node is None:
        print(f"{prefix}None")
        return
    
    node_type = type(node).__name__
    print(f"{prefix}{node_type}")
    
    for attr_name in dir(node):
        if not attr_name.startswith('_'):
            attr_value = getattr(node, attr_name, None)
            if isinstance(attr_value, (str, int, float, bool)):
                print(f"{prefix}  {attr_name}: {repr(attr_value)}")
            elif isinstance(attr_value, list) and len(attr_value) > 0:
                print(f"{prefix}  {attr_name}:")
                for item in attr_value:
                    print_ast(item, indent + 2)
            elif hasattr(attr_value, 'accept'):
                print(f"{prefix}  {attr_name}:")
                print_ast(attr_value, indent + 2)

source_code = "from __future__ import DeferredOperations;0.1+0.2-0.2;"

print("=" * 60)
print(f"优化前: {source_code}")
print("=" * 60)

scanner = Scanner(source_code)
tokens = scanner.scan_tokens()

parser = Parser(tokens)
ast = parser.parse()

print_ast(ast)

print("\n" + "=" * 60)
print("启用 DeferredOperations 特性")
print("=" * 60)

feature_manager = get_feature_manager()
feature_manager.enable('DeferredOperations')

print("\n" + "=" * 60)
print("优化后")
print("=" * 60)

optimizer = Optimizer()
optimized_ast = optimizer.optimize(ast)

print_ast(optimized_ast)

print("\n" + "=" * 60)
print("禁用 DeferredOperations 特性")
print("=" * 60)

feature_manager.disable('DeferredOperations')
