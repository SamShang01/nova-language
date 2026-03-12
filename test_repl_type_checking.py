"""
在REPL中测试类型检查功能
"""

import sys
sys.path.insert(0, 'e:/nova/src')

from nova.repl import NovaREPL

def test_repl_type_checking():
    """在REPL中测试类型检查"""
    print("=" * 60)
    print("在REPL中测试类型检查功能")
    print("=" * 60)
    
    # 创建REPL实例
    repl = NovaREPL()
    
    # 测试1: 结构体字段类型检查
    print("\n测试1: 结构体字段类型检查")
    print("输入: struct it { a: int; }")
    result = repl.execute("struct it { a: int; }")
    print(f"结果: {result}")
    
    print("\n输入: it(89.87);")
    result = repl.execute("it(89.87);")
    print(f"结果: {result}")
    
    # 测试2: 正确的类型使用
    print("\n测试2: 正确的类型使用")
    print("输入: it(89);")
    result = repl.execute("it(89);")
    print(f"结果: {result}")
    
    # 测试3: 函数参数类型检查
    print("\n测试3: 函数参数类型检查")
    print("输入: func add(a: int, b: int) -> int { return a + b; }")
    result = repl.execute("func add(a: int, b: int) -> int { return a + b; }")
    print(f"结果: {result}")
    
    print("\n输入: add(1, 2.5);")
    result = repl.execute("add(1, 2.5);")
    print(f"结果: {result}")
    
    # 测试4: 正确的函数调用
    print("\n测试4: 正确的函数调用")
    print("输入: add(1, 2);")
    result = repl.execute("add(1, 2);")
    print(f"结果: {result}")
    
    print("\n" + "=" * 60)
    print("REPL类型检查测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_repl_type_checking()
