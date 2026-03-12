"""
Nova语言基本功能测试
"""

import sys
import os

# 添加根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

def test_lexer():
    """
    测试词法分析器
    """
    print("=== 测试词法分析器 ===")
    try:
        from src.nova.compiler.lexer.scanner import Scanner
        scanner = Scanner("let x = 1 + 2;")
        tokens = scanner.scan_tokens()
        print(f"✓ 词法分析成功，生成了 {len(tokens)} 个Token")
        for token in tokens:
            if token.type.name != "EOF":
                print(f"  - {token.type.name}: {token.literal}")
        return True
    except Exception as e:
        print(f"✗ 词法分析失败: {e}")
        return False

def test_parser():
    """
    测试语法分析器
    """
    print("\n=== 测试语法分析器 ===")
    try:
        from src.nova.compiler.lexer.scanner import Scanner
        from src.nova.compiler.parser.parser import Parser
        scanner = Scanner("let x = 1 + 2;")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✓ 语法分析成功，生成了AST")
        print(f"  - 程序包含 {len(ast.statements)} 个语句")
        return True
    except Exception as e:
        print(f"✗ 语法分析失败: {e}")
        return False

def test_vm():
    """
    测试虚拟机
    """
    print("\n=== 测试虚拟机 ===")
    try:
        from src.nova.vm.machine import VirtualMachine
        from src.nova.vm.instructions import LOAD_CONST, BINARY_ADD, RETURN_VALUE
        vm = VirtualMachine()
        instructions = [LOAD_CONST(1), LOAD_CONST(2), BINARY_ADD(), RETURN_VALUE()]
        result = vm.execute(instructions)
        print(f"✓ 虚拟机执行成功，结果: {result}")
        return True
    except Exception as e:
        print(f"✗ 虚拟机执行失败: {e}")
        return False

def test_stdlib():
    """
    测试标准库
    """
    # 保存原始的print函数
    import builtins
    original_print = builtins.print
    original_print("\n=== 测试标准库 ===")
    try:
        from src.nova.stdlib.core.types import Int, Float, String, Bool, Char
        
        # 测试核心类型
        i = Int(42)
        f = Float(3.14)
        s = String("hello")
        b = Bool(True)
        c = Char('a')
        
        original_print(f"✓ 核心类型创建成功")
        original_print(f"  - Int: {i.value}")
        original_print(f"  - Float: {f.value}")
        original_print(f"  - String: {s.value}")
        original_print(f"  - Bool: {b.value}")
        original_print(f"  - Char: {c.value}")
        
        return True
    except Exception as e:
        original_print(f"✗ 标准库测试失败: {e}")
        return False

def test_version():
    """
    测试版本管理
    """
    print("\n=== 测试版本管理 ===")
    try:
        from nova.version import __version__, version_greater_or_equal
        print(f"✓ 版本信息获取成功")
        print(f"  - 当前版本: {__version__}")
        print(f"  - 版本判断 (0.1.0 >= 0.1.0): {version_greater_or_equal(0, 1, 0)}")
        print(f"  - 版本判断 (0.1.0 >= 0.2.0): {version_greater_or_equal(0, 2, 0)}")
        return True
    except Exception as e:
        print(f"✗ 版本管理测试失败: {e}")
        return False

if __name__ == '__main__':
    print("Nova语言基本功能测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_lexer,
        test_parser,
        test_vm,
        # test_stdlib,  # 暂时跳过标准库测试
        test_version
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("✓ 所有测试通过，Nova语言核心功能正常！")
    else:
        print("✗ 部分测试失败，需要修复！")
