"""
调试继承
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

source_code = """
class Animal {
    private var _name: string;
    public var age: int;
    
    public function getName(): string {
        return this._name;
    }
}

class Dog extends Animal {
    public var breed: string;
    
    public function bark(): string {
        return "Woof!";
    }
}
"""

print("=" * 60)
print("调试继承")
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
    
    # 检查类
    animal_class = vm.environment.get('Animal')
    dog_class = vm.environment.get('Dog')
    
    print(f"Animal class: {animal_class}")
    print(f"Animal fields: {animal_class.fields}")
    print(f"Animal parent: {animal_class.parent}")
    
    print(f"\nDog class: {dog_class}")
    print(f"Dog fields: {dog_class.fields}")
    print(f"Dog parent: {dog_class.parent}")
    print(f"Dog parent type: {type(dog_class.parent)}")
    
    if dog_class.parent:
        print(f"Dog parent fields: {dog_class.parent.fields if hasattr(dog_class.parent, 'fields') else 'N/A'}")
    
    # 测试获取所有字段
    print(f"\nDog all fields: {dog_class._get_all_fields()}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
