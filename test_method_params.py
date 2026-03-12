#!/usr/bin/env python
"""
测试方法参数
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

code = """
class Person {
    let name: string;
    let age: int;
    
    fn __init__(name: string, age: int) {
        this.name = name;
        this.age = age;
    }
}

impl Comparable<Person> for Person {
    fn compare(other: Person): int {
        if this.age < other.age {
            return -1;
        } else if this.age > other.age {
            return 1;
        } else {
            return 0;
        }
    }
}
"""

print("测试代码:")
print(code)
print("\n" + "="*50 + "\n")

scanner = Scanner(code)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()

# 遍历AST，找到 ImplBlock 节点
def find_impl_blocks(node, depth=0):
    indent = "  " * depth
    node_type = type(node).__name__
    print(f"{indent}{node_type}")
    
    if node_type == 'ImplBlock':
        print(f"{indent}  methods:")
        for method in node.methods:
            print(f"{indent}    {method}")
            if hasattr(method, 'name'):
                print(f"{indent}      name: {method.name}")
            if hasattr(method, 'params'):
                print(f"{indent}      params: {method.params}")
                for param in method.params:
                    print(f"{indent}        {param}")
                    if hasattr(param, 'name'):
                        print(f"{indent}          name: {param.name}")
    
    if hasattr(node, '__dict__'):
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, '__dict__'):
                        find_impl_blocks(item, depth + 1)
            elif hasattr(value, '__dict__'):
                find_impl_blocks(value, depth + 1)

find_impl_blocks(ast)
