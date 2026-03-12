"""
调试方法调用
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

source_code = """
class Person {
    private var _name: string;
    public var nationality: string;
    protected var _id: string;
    
    public function getName(): string {
        return this._name;
    }
}

var p = Person('John', 'USA', '123');
"""

print("=" * 60)
print("调试方法调用")
print("=" * 60)

try:
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens, repl_mode=True)
    ast = parser.parse()
    
    codegen = CodeGenerator()
    instructions, constants = codegen.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions, constants)
    result = vm.run()
    
    # 检查类的方法
    person_class = vm.environment.get('Person')
    print(f"Person class: {person_class}")
    print(f"Person methods: {person_class.methods}")
    
    # 检查实例
    p = vm.environment.get('p')
    print(f"Instance p: {p}")
    print(f"Instance p.nova_class: {p.nova_class}")
    print(f"Instance p.nova_class.methods: {p.nova_class.methods}")
    
    # 尝试获取方法
    method = p.nova_class.get_method('getName')
    print(f"Method getName: {method}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
