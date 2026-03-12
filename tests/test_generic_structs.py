"""
泛型结构体测试用例
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

class TestGenericStructs(unittest.TestCase):
    """
    泛型结构体测试类
    """
    
    def test_simple_generic_struct(self):
        """
        测试简单泛型结构体
        """
        source = """
        generic struct Pair<T> {
            first: T;
            second: T;
        }
        
        func main() {
            let pair = Pair<int>(first: 1, second: 2);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_struct_with_multiple_type_params(self):
        """
        测试多类型参数的泛型结构体
        """
        source = """
        generic struct Pair<T, U> {
            first: T;
            second: U;
        }
        
        func main() {
            let pair = Pair<int, string>(first: 1, second: "hello");
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_struct_with_methods(self):
        """
        测试带方法的泛型结构体
        """
        source = """
        generic struct Box<T> {
            value: T;
            
            generic func get(self: Box<T>) -> T {
                return self.value;
            }
            
            generic func set(self: Box<T>, value: T) -> Box<T> {
                self.value = value;
                return self;
            }
        }
        
        func main() {
            let box = Box<int>(value: 42);
            let value = box.get();
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_struct_nested(self):
        """
        测试嵌套泛型结构体
        """
        source = """
        generic struct Pair<T, U> {
            first: T;
            second: U;
        }
        
        generic struct Triple<T, U, V> {
            first: T;
            second: U;
            third: V;
        }
        
        func main() {
            let pair = Pair<int, string>(first: 1, second: "hello");
            let triple = Triple<int, string, float>(first: 1, second: "hello", third: 3.14);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_struct_with_array_field(self):
        """
        测试带数组字段的泛型结构体
        """
        source = """
        generic struct Stack<T> {
            items: [T];
            
            generic func push(self: Stack<T>, item: T) -> Stack<T> {
                self.items.push(item);
                return self;
            }
            
            generic func pop(self: Stack<T>) -> T {
                return self.items.pop();
            }
        }
        
        func main() {
            let stack = Stack<int>(items: []);
            stack.push(1);
            stack.push(2);
            let value = stack.pop();
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_struct_code_generation(self):
        """
        测试泛型结构体代码生成
        """
        source = """
        generic struct Pair<T> {
            first: T;
            second: T;
        }
        
        func main() {
            let pair = Pair<int>(first: 1, second: 2);
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
    
    def test_generic_struct_with_generic_function(self):
        """
        测试泛型结构体与泛型函数结合使用
        """
        source = """
        generic struct Pair<T, U> {
            first: T;
            second: U;
        }
        
        generic func make_pair<T, U>(first: T, second: U) -> Pair<T, U> {
            return Pair<T, U>(first: first, second: second);
        }
        
        func main() {
            let pair = make_pair(1, "hello");
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
