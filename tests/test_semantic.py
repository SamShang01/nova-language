"""
Nova语言语义分析器测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.errors import SemanticError

class TestSemanticAnalyzer(unittest.TestCase):
    """
    语义分析器测试类
    """
    
    def test_analyze_simple_program(self):
        """
        测试分析简单程序
        """
        code = """
        module main;
        
        fn main() {
            let x: int = 1;
            let y: int = 2;
            return x + y;
        }
        """
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_program = analyzer.analyze(program)
        
        self.assertIsNotNone(analyzed_program)
    
    def test_analyze_variable_declaration(self):
        """
        测试分析变量声明
        """
        code = "let x: int = 1;"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_program = analyzer.analyze(program)
        
        self.assertIsNotNone(analyzed_program)
    
    def test_analyze_constant_declaration(self):
        """
        测试分析常量声明
        """
        code = "const PI: float =3.14;"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_program = analyzer.analyze(program)
        
        self.assertIsNotNone(analyzed_program)
    
    def test_analyze_function_definition(self):
        """
        测试分析函数定义
        """
        code = "fn add(a: int, b: int) -> int { return a + b; }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_program = analyzer.analyze(program)
        
        self.assertIsNotNone(analyzed_program)
    
    def test_analyze_if_statement(self):
        """
        测试分析if语句
        """
        code = """
        if x > 0 {
            return x;
        } else {
            return -x;
        }
        """
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 这里会报错，因为x未定义，但我们只是测试分析过程
        with self.assertRaises(SemanticError):
            analyzer.analyze(program)
    
    def test_analyze_for_loop(self):
        """
        测试分析for循环
        """
        code = "for item in items { print(item); }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 这里会报错，因为items未定义，但我们只是测试分析过程
        with self.assertRaises(SemanticError):
            analyzer.analyze(program)
    
    def test_analyze_while_loop(self):
        """
        测试分析while循环
        """
        code = "while x > 0 { x = x - 1; }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 这里会报错，因为x未定义，但我们只是测试分析过程
        with self.assertRaises(SemanticError):
            analyzer.analyze(program)
    
    def test_analyze_loop_statement(self):
        """
        测试分析loop语句
        """
        code = "loop { if done { break; } }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 这里会报错，因为done未定义，但我们只是测试分析过程
        with self.assertRaises(SemanticError):
            analyzer.analyze(program)
    
    def test_analyze_match_statement(self):
        """
        测试分析match语句
        """
        code = """
        match x {
            1 => print("One"),
            2 => print("Two"),
            _ => print("Other"),
        }
        """
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 这里会报错，因为x未定义，但我们只是测试分析过程
        with self.assertRaises(SemanticError):
            analyzer.analyze(program)
    
    def test_analyze_return_statement(self):
        """
        测试分析return语句
        """
        code = "return 42;"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        # 这里会报错，因为return语句不在函数中，但我们只是测试分析过程
        with self.assertRaises(SemanticError):
            analyzer.analyze(program)
    
    def test_analyze_struct_definition(self):
        """
        测试分析结构体定义
        """
        code = """
        struct Point {
            x: int,
            y: int,
        }
        """
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_program = analyzer.analyze(program)
        
        self.assertIsNotNone(analyzed_program)
    
    def test_analyze_enum_definition(self):
        """
        测试分析枚举定义
        """
        code = """
        enum Direction {
            North,
            South,
            East,
            West,
        }
        """
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_program = analyzer.analyze(program)
        
        self.assertIsNotNone(analyzed_program)

if __name__ == '__main__':
    unittest.main()
