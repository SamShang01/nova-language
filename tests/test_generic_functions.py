"""
泛型函数测试用例
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

class TestGenericFunctions(unittest.TestCase):
    """
    泛型函数测试类
    """
    
    def test_simple_generic_function(self):
        """
        测试简单泛型函数
        """
        source = """
        generic func identity<T>(value: T) -> T {
            return value;
        }
        
        func main() {
            let x = identity(42);
            let y = identity("hello");
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_with_multiple_params(self):
        """
        测试多参数泛型函数
        """
        source = """
        generic func swap<T>(a: T, b: T) -> (T, T) {
            return (b, a);
        }
        
        func main() {
            let x = 1;
            let y = 2;
            let (new_x, new_y) = swap(x, y);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_with_where_clause(self):
        """
        测试带where子句的泛型函数
        """
        source = """
        generic func max<T>(a: T, b: T) -> T
            where T: Comparable
        {
            if a > b {
                return a;
            } else {
                return b;
            }
        }
        
        func main() {
            let result = max(10, 20);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_with_multiple_type_params(self):
        """
        测试多类型参数的泛型函数
        """
        source = """
        generic func pair<T, U>(first: T, second: U) -> (T, U) {
            return (first, second);
        }
        
        func main() {
            let p = pair(1, "hello");
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_return_type(self):
        """
        测试泛型函数返回类型
        """
        source = """
        generic func first<T>(items: [T]) -> T {
            return items[0];
        }
        
        func main() {
            let nums = [1, 2, 3];
            let first_num = first(nums);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_with_nested_generics(self):
        """
        测试嵌套泛型函数
        """
        source = """
        generic func map<T, U>(items: [T], f: func(T) -> U) -> [U] {
            let result = [];
            for item in items {
                result.push(f(item));
            }
            return result;
        }
        
        func main() {
            let nums = [1, 2, 3];
            let doubled = map(nums, func(x: int) -> int { return x * 2; });
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_generic_function_code_generation(self):
        """
        测试泛型函数代码生成
        """
        source = """
        generic func identity<T>(value: T) -> T {
            return value;
        }
        
        func main() {
            let x = identity(42);
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

if __name__ == '__main__':
    unittest.main()
