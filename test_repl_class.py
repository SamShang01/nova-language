"""
测试REPL中类定义和实例化
"""

import sys
import os
from io import StringIO

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
    
    # 测试实例化（没有分号）
    print("\n测试2: 实例化类（没有分号）")
    code2 = "Person()"
    repl._execute_code(code2)
    
    # 测试实例化（有分号）
    print("\n测试3: 实例化类（有分号）")
    code3 = "Person();"
    repl._execute_code(code3)
    
    # 测试存储到变量
    print("\n测试4: 存储到变量")
    code4 = "var p = Person();"
    repl._execute_code(code4)
    
    print("\n测试5: 访问变量")
    code5 = "p"
    repl._execute_code(code5)

if __name__ == "__main__":
    test_repl()
