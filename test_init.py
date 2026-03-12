"""
测试构造函数
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试构造函数
source_code = """
class Person {
    public var name: string;
    public var age: int;
    
    init(name: string, age: int) {
        this.name = name;
        this.age = age;
    }
    
    public function greet(): string {
        return 'Hello, I am ' + this.name;
    }
}

var p = Person('Alice', 25);
p.name
"""

print("测试构造函数")
print("=" * 60)
print("\nSource code:")
print(source_code)
print("\n" + "=" * 60)

try:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens, repl_mode=True)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    
    print(f"\n✅ 测试通过！结果: {result}")
    
except Exception as e:
    print(f"\n❌ 测试失败！错误: {e}")
    import traceback
    traceback.print_exc()
