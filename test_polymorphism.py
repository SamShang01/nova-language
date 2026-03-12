"""
测试多态 - 方法重写和动态绑定
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试多态
source_code = """
class Animal {
    public var name: string;
    
    init(name: string) {
        this.name = name;
    }
    
    public function make_sound(): string {
        return 'Some sound';
    }
}

class Dog extends Animal {
    public function make_sound(): string {
        return 'Woof!';
    }
}

class Cat extends Animal {
    public function make_sound(): string {
        return 'Meow!';
    }
}

var dog = Dog('Buddy');
var cat = Cat('Whiskers');
dog.make_sound()
"""

print("测试多态 - 方法重写和动态绑定")
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
