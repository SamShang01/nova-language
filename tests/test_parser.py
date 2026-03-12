"""
Nova语言语法分析器测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser

class TestParser(unittest.TestCase):
    """
    语法分析器测试类
    """
    
    def test_parse_program(self):
        """
        测试解析程序
        """
        code = """
        module main;
        
        fn main() {
            let x = 1;
            let y = 2;
            return x + y;
        }
        """
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 2)  # 模块声明和函数定义
    
    def test_parse_variable_declaration(self):
        """
        测试解析变量声明
        """
        code = "let x: int = 1;"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertEqual(stmt.name, "x")
        # 检查类型名称，而不是类型对象
        if hasattr(stmt.var_type, 'name'):
            self.assertEqual(stmt.var_type.name, "int")
        else:
            self.assertEqual(stmt.var_type, "int")
    
    def test_parse_constant_declaration(self):
        """
        测试解析常量声明
        """
        code = "const PI: float = 3.14;"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertEqual(stmt.name, "PI")
        # 检查类型名称，而不是类型对象
        if hasattr(stmt.const_type, 'name'):
            self.assertEqual(stmt.const_type.name, "float")
        else:
            self.assertEqual(stmt.const_type, "float")
    
    def test_parse_function_definition(self):
        """
        测试解析函数定义
        """
        code = "fn add(a: int, b: int) -> int { return a + b; }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertEqual(stmt.name, "add")
        self.assertEqual(len(stmt.params), 2)
        # 检查类型名称，而不是类型对象
        if hasattr(stmt.return_type, 'name'):
            self.assertEqual(stmt.return_type.name, "int")
        else:
            self.assertEqual(stmt.return_type, "int")
    
    def test_parse_if_statement(self):
        """
        测试解析if语句
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
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsNotNone(stmt.condition)
        self.assertIsNotNone(stmt.then_branch)
        self.assertIsNotNone(stmt.else_branch)
    
    def test_parse_for_loop(self):
        """
        测试解析for循环
        """
        code = "for item in items { print(item); }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertEqual(stmt.variable, "item")
        self.assertIsNotNone(stmt.iterable)
        self.assertIsNotNone(stmt.body)
    
    def test_parse_while_loop(self):
        """
        测试解析while循环
        """
        code = "while x < 10 { x = x + 1; }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsNotNone(stmt.condition)
        self.assertIsNotNone(stmt.body)
    
    def test_parse_loop_statement(self):
        """
        测试解析loop语句
        """
        code = "loop { if done { break; } }"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsNotNone(stmt.body)
    
    def test_parse_match_statement(self):
        """
        测试解析match语句
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
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsNotNone(stmt.expression)
        self.assertGreater(len(stmt.cases), 0)
    
    def test_parse_return_statement(self):
        """
        测试解析return语句
        """
        code = "return 42;"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsNotNone(stmt.value)

if __name__ == '__main__':
    unittest.main()
