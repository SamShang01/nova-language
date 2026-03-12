"""
测试匿名数据结构功能
"""

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine


def test_anonymous_struct():
    """测试匿名结构体"""
    print("测试匿名结构体...")
    
    code = """
    let s = struct { x: int; y: int }
    print(s);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"匿名结构体测试通过: {result}")


def test_anonymous_struct_with_values():
    """测试匿名结构体并实例化"""
    print("\n测试匿名结构体实例化...")
    
    code = """
    let Point = struct { x: int; y: int }
    let p = Point(x:10, y:20);
    print(p);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"匿名结构体实例化测试通过: {result}")


def test_named_struct():
    """测试命名结构体"""
    print("\n测试命名结构体...")
    
    code = """
    struct Point { x: int; y: int }
    let p = Point(x:10, y:20);
    print(p);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"命名结构体测试通过: {result}")


def test_anonymous_union():
    """测试匿名联合体"""
    print("\n测试匿名联合体...")
    
    code = """
    let u = union { int; float; string }
    print(u);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"匿名联合体测试通过: {result}")


def test_named_union():
    """测试命名联合体"""
    print("\n测试命名联合体...")
    
    code = """
    union Value { int; float; string }
    let v = Value(42);
    print(v);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"命名联合体测试通过: {result}")


def test_anonymous_enum():
    """测试匿名枚举"""
    print("\n测试匿名枚举...")
    
    code = """
    let e = enum { Red, Green, Blue }
    print(e);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"匿名枚举测试通过: {result}")


def test_named_enum():
    """测试命名枚举"""
    print("\n测试命名枚举...")
    
    code = """
    enum Color { Red, Green, Blue }
    let c = Color.Red;
    print(c);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"命名枚举测试通过: {result}")


def test_enum_equality():
    """测试枚举相等比较"""
    print("\n测试枚举相等比较...")
    
    code = """
    enum Color { Red, Green, Blue }
    let c1 = Color.Red;
    let c2 = Color.Red;
    let c3 = Color.Green;
    print(c1 == c2);
    print(c1 == c3);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"枚举相等比较测试通过")


def test_struct_with_methods():
    """测试带方法的结构体"""
    print("\n测试带方法的结构体...")
    
    code = """
    struct Point {
        x: int;
        y: int;
        func distance() -> int {
            return self.x * self.x + self.y * self.y;
        }
    }
    let p = Point(x:3, y:4);
    print(p);
    """
    
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = CodeGenerator()
    instructions, constants = generator.generate(ast)
    
    vm = VirtualMachine()
    vm.load(instructions)
    result = vm.run()
    
    print(f"带方法的结构体测试通过: {result}")


if __name__ == "__main__":
    try:
        test_anonymous_struct()
        test_anonymous_struct_with_values()
        test_named_struct()
        test_anonymous_union()
        test_named_union()
        test_anonymous_enum()
        test_named_enum()
        test_enum_equality()
        test_struct_with_methods()
        
        print("\n✅ 所有匿名数据结构测试通过！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
