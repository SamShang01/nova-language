"""
测试类型检查功能

这个文件测试Nova语言的类型检查功能，包括：
1. 结构体字段赋值的类型兼容性检查
2. 函数参数的类型匹配检查
3. 函数返回值的类型匹配检查
"""

import sys
sys.path.insert(0, 'e:/nova/src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.errors import SemanticError

def test_struct_field_type_check():
    """测试结构体字段赋值的类型检查"""
    print("测试1: 结构体字段赋值的类型检查")
    
    # 测试代码：定义一个int字段的结构体，然后传入float值
    code = """
struct it {
    a: int;
}
it(89.87);
"""
    
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        print("  ❌ 测试失败：应该抛出类型错误")
        return False
    except SemanticError as e:
        print(f"  ✓ 测试通过：正确捕获类型错误 - {e}")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败：意外错误 - {e}")
        return False

def test_function_param_type_check():
    """测试函数参数的类型检查"""
    print("\n测试2: 函数参数的类型检查")
    
    # 测试代码：定义一个接受int参数的函数，然后传入float值
    code = """
func add(a: int, b: int) -> int {
    return a + b;
}
add(1, 2.5);
"""
    
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        print("  ❌ 测试失败：应该抛出类型错误")
        return False
    except SemanticError as e:
        print(f"  ✓ 测试通过：正确捕获类型错误 - {e}")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败：意外错误 - {e}")
        return False

def test_function_return_type_check():
    """测试函数返回值的类型检查"""
    print("\n测试3: 函数返回值的类型检查")
    
    # 测试代码：定义一个返回int的函数，但返回float值
    code = """
func get_value() -> int {
    return 3.14;
}
"""
    
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        print("  ❌ 测试失败：应该抛出类型错误")
        return False
    except SemanticError as e:
        print(f"  ✓ 测试通过：正确捕获类型错误 - {e}")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败：意外错误 - {e}")
        return False

def test_correct_types():
    """测试正确的类型使用"""
    print("\n测试4: 正确的类型使用")
    
    # 测试代码：使用正确的类型
    code = """
struct it {
    a: int;
}
it(89);

func add(a: int, b: int) -> int {
    return a + b;
}
add(1, 2);
"""
    
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        print("  ✓ 测试通过：正确的类型使用没有错误")
        return True
    except SemanticError as e:
        print(f"  ❌ 测试失败：不应该抛出类型错误 - {e}")
        return False
    except Exception as e:
        print(f"  ❌ 测试失败：意外错误 - {e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Nova语言类型检查功能测试")
    print("=" * 60)
    
    results = []
    results.append(test_struct_field_type_check())
    results.append(test_function_param_type_check())
    results.append(test_function_return_type_check())
    results.append(test_correct_types())
    
    print("\n" + "=" * 60)
    print(f"测试结果: {sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    if all(results):
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
