"""
测试 super 关键字
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

# 测试 super 关键字
source_code = """
class Animal {
    public var name: string;
    
    init(name: string) {
        this.name = name;
    }
    
    public function make_sound(): string {
        return 'Some sound';
    }
    
    public function describe(): string {
        return 'I am ' + this.name;
    }
}

class Dog extends Animal {
    public function make_sound(): string {
        return super.make_sound() + ' but actually Woof!';
    }
    
    public function describe(): string {
        return super.describe() + ' and I am a dog';
    }
}

var dog = Dog('Buddy');
dog.describe()
"""

print("测试 super 关键字")
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
