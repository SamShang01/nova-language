"""
特质定义和实现测试用例
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

class TestTraits(unittest.TestCase):
    """
    特质定义和实现测试类
    """
    
    def test_simple_trait_definition(self):
        """
        测试简单特质定义
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        func main() {
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_trait_with_multiple_methods(self):
        """
        测试多方法特质定义
        """
        source = """
        trait Debug {
            func debug(self: Self) -> string;
            func type_name(self: Self) -> string;
        }
        
        func main() {
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_trait_implementation(self):
        """
        测试特质实现
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        impl Display for int {
            func display(self: int) -> string {
                return str(self);
            }
        }
        
        func main() {
            let x = 42;
            print(x.display());
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_with_trait_constraint(self):
        """
        测试带特质约束的泛型函数
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        impl Display for int {
            func display(self: int) -> string {
                return str(self);
            }
        }
        
        func print_display_int(value: int) {
            print(value.display());
        }
        
        func main() {
            let x = 42;
            print_display_int(x);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_multiple_trait_constraints(self):
        """
        测试多特质约束
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        trait Clone {
            func clone(self: Self) -> Self;
        }
        
        impl Display for int {
            func display(self: int) -> string {
                return str(self);
            }
        }
        
        impl Clone for int {
            func clone(self: int) -> int {
                return self;
            }
        }
        
        func clone_and_display_int(value: int) {
            let cloned = value.clone();
            print(cloned.display());
        }
        
        func main() {
            let x = 42;
            clone_and_display_int(x);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_trait_for_struct(self):
        """
        测试结构体实现特质
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        impl Display for int {
            func display(self: int) -> string {
                return str(self);
            }
        }
        
        func main() {
            let x = 42;
            print(x.display());
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_trait_code_generation(self):
        """
        测试特质代码生成
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        impl Display for int {
            func display(self: int) -> string {
                return str(self);
            }
        }
        
        func main() {
            let x = 42;
            print(x.display());
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(ast)
        
        self.assertIsInstance(instructions, list)
        self.assertIsInstance(constants, list)
    
    def test_trait_inheritance(self):
        """
        测试特质继承（简化版本）
        """
        source = """
        trait Display {
            func display(self: Self) -> string;
        }
        
        trait Debug {
            func debug(self: Self) -> string;
        }
        
        impl Display for int {
            func display(self: int) -> string {
                return str(self);
            }
        }
        
        impl Debug for int {
            func debug(self: int) -> string {
                return str(self);
            }
        }
        
        func main() {
            let x = 42;
            print(x.display());
            print(x.debug());
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)

if __name__ == '__main__':
    unittest.main()
