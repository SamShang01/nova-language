"""
测试REPL中类实例化带参数
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.repl import NovaREPL

def test_repl():
    """
    测试REPL
    """
    repl = NovaREPL()
    
    # 测试类定义
    print("测试1: 定义类")
    code1 = """class Person {
    private var _name: string;
    public var nationality: string;
    protected var _id: string;
    
    public function getName(): string {
        return this._name;
    }
}"""
    repl._execute_code(code1)
    
    # 测试实例化（带参数）
    print("\n测试2: 实例化类（带参数）")
    code2 = "Person('John', 'USA', '123')"
    repl._execute_code(code2)
    
    # 测试实例化（带参数和分号）
    print("\n测试3: 实例化类（带参数和分号）")
    code3 = "Person('Jane', 'UK', '456');"
    repl._execute_code(code3)
    
    # 测试存储到变量
    print("\n测试4: 存储到变量")
    code4 = "var p = Person('Bob', 'Canada', '789');"
    repl._execute_code(code4)
    
    print("\n测试5: 访问变量")
    code5 = "p"
    repl._execute_code(code5)

if __name__ == "__main__":
    test_repl()
