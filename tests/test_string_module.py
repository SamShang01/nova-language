"""
字符串模块测试用例
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

class TestStringModule(unittest.TestCase):
    """
    字符串模块测试类
    """
    
    def test_case_conversion(self):
        """
        测试大小写转换
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello World";
            let upper = to_upper(text);
            let lower = to_lower(text);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_operations(self):
        """
        测试字符串操作
        """
        source = """
        use std::string;
        
        func main() {
            let text = "  Hello World  ";
            let trimmed = trim(text);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_split_and_join(self):
        """
        测试字符串分割和连接
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello,World,Nova";
            let parts = split(text, ",");
            let joined = join(parts, " ");
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_replace(self):
        """
        测试字符串替换
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello World";
            let replaced = replace(text, "World", "Nova");
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_substring(self):
        """
        测试字符串子串
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello World";
            let sub = substring(text, 0, 5);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_checks(self):
        """
        测试字符串检查函数
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello World";
            let has_hello = contains(text, "Hello");
            let starts_with_hello = starts_with(text, "Hello");
            let ends_with_world = ends_with(text, "World");
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_palindrome_check(self):
        """
        测试回文检查
        """
        source = """
        use std::string;
        
        func is_palindrome(text: string) -> bool {
            let reversed_text = reverse(text);
            return text == reversed_text;
        }
        
        func main() {
            let word1 = "racecar";
            let word2 = "hello";
            let is_pal1 = is_palindrome(word1);
            let is_pal2 = is_palindrome(word2);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_module_code_generation(self):
        """
        测试字符串模块代码生成
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello World";
            let upper = to_upper(text);
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
    
    def test_string_concatenation(self):
        """
        测试字符串连接
        """
        source = """
        use std::string;
        
        func main() {
            let greeting = "Hello";
            let name = "World";
            let message = greeting + " " + name;
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_string_length(self):
        """
        测试字符串长度
        """
        source = """
        use std::string;
        
        func main() {
            let text = "Hello World";
            let length = len(text);
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
