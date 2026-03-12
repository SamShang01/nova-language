"""
Nova语言组件验证脚本
"""

import sys
import os

# 添加根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

def verify_imports():
    """
    验证各个模块是否能正常导入
    """
    print("=== 验证Nova语言组件 ===")
    
    # 测试词法分析器
    try:
        from src.nova.compiler.lexer.scanner import Scanner
        from src.nova.compiler.lexer.tokens import TokenType
        print("✓ 词法分析器导入成功")
        
        # 测试词法分析器基本功能
        scanner = Scanner("let x = 1;")
        token = scanner.next_token()
        print("✓ 词法分析器基本功能正常")
    except Exception as e:
        print(f"✗ 词法分析器导入失败: {e}")
    
    # 测试语法分析器
    try:
        from src.nova.compiler.parser.parser import Parser
        print("✓ 语法分析器导入成功")
    except Exception as e:
        print(f"✗ 语法分析器导入失败: {e}")
    
    # 测试语义分析器
    try:
        from src.nova.compiler.semantic.analyzer import SemanticAnalyzer
        print("✓ 语义分析器导入成功")
    except Exception as e:
        print(f"✗ 语义分析器导入失败: {e}")
    
    # 测试虚拟机
    try:
        from src.nova.vm.machine import VirtualMachine
        from src.nova.vm.instructions import LOAD_CONST, RETURN_VALUE
        print("✓ 虚拟机导入成功")
        
        # 测试虚拟机基本功能
        vm = VirtualMachine()
        instructions = [LOAD_CONST(42), RETURN_VALUE()]
        result = vm.execute(instructions)
        print("✓ 虚拟机基本功能正常")
    except Exception as e:
        print(f"✗ 虚拟机导入失败: {e}")
    
    # 测试标准库
    try:
        from src.nova.stdlib.core.types import Int, Float, String, Bool, Char
        from src.nova.stdlib.collections.list import List
        from src.nova.stdlib.collections.dict import Dict
        from src.nova.stdlib.collections.set import Set
        from src.nova.stdlib.io.file import File
        from src.nova.stdlib.io.streams import stdin, stdout, stderr
        from src.nova.stdlib.asynchronous.future import Future
        from src.nova.stdlib.asynchronous.task import Task
        print("✓ 标准库导入成功")
    except Exception as e:
        print(f"✗ 标准库导入失败: {e}")
    
    # 测试版本管理
    try:
        from nova.version import __version__, version_greater_or_equal
        print(f"✓ 版本管理导入成功，当前版本: {__version__}")
    except Exception as e:
        print(f"✗ 版本管理导入失败: {e}")
    
    print("=== 验证完成 ===")

if __name__ == '__main__':
    verify_imports()
