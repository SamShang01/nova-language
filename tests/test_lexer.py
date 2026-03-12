"""
Nova语言词法分析器测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.lexer.tokens import TokenType

class TestLexer(unittest.TestCase):
    """
    词法分析器测试类
    """
    
    def test_scan_keywords(self):
        """
        测试扫描关键字
        """
        code = "let const fn if else for while loop match return break continue"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        token_data = []
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            token_data.append((token.type, token.lexeme))
        
        expected = [
            (TokenType.LET, "let"),
            (TokenType.CONST, "const"),
            (TokenType.FUNC, "fn"),
            (TokenType.IF, "if"),
            (TokenType.ELSE, "else"),
            (TokenType.FOR, "for"),
            (TokenType.WHILE, "while"),
            (TokenType.LOOP, "loop"),
            (TokenType.MATCH, "match"),
            (TokenType.RETURN, "return"),
            (TokenType.BREAK, "break"),
            (TokenType.CONTINUE, "continue"),
        ]
        
        self.assertEqual(token_data, expected)
    
    def test_scan_operators(self):
        """
        测试扫描运算符
        """
        code = "= + - * / % == != < <= > >= && || ! & | ^ ~ << >> >>>"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        token_data = []
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            token_data.append((token.type, token.lexeme))
        
        expected = [
            (TokenType.ASSIGN, "="),
            (TokenType.PLUS, "+"),
            (TokenType.MINUS, "-"),
            (TokenType.MULTIPLY, "*"),
            (TokenType.DIVIDE, "/"),
            (TokenType.MODULO, "%"),
            (TokenType.EQUALS, "=="),
            (TokenType.NOT_EQUALS, "!="),
            (TokenType.LESS_THAN, "<"),
            (TokenType.LESS_THAN_OR_EQUAL, "<="),
            (TokenType.GREATER_THAN, ">"),
            (TokenType.GREATER_THAN_OR_EQUAL, ">="),
            (TokenType.AND, "&&"),
            (TokenType.OR, "||"),
            (TokenType.NOT, "!"),
            (TokenType.AND, "&"),
            (TokenType.OR, "|"),
            (TokenType.ASSIGN, "^"),
            (TokenType.ASSIGN, "~"),
            (TokenType.ASSIGN, "<<"),
            (TokenType.ASSIGN, ">>"),
            (TokenType.ASSIGN, ">>>"),
        ]
        
        self.assertEqual(token_data, expected)
    
    def test_scan_literals(self):
        """
        测试扫描字面量
        """
        code = "123 45.67 \"hello\" true false 'a'"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        token_data = []
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            token_data.append((token.type, token.lexeme))
        
        expected = [
            (TokenType.INTEGER, "123"),
            (TokenType.FLOAT, "45.67"),
            (TokenType.STRING, "\"hello\""),
            (TokenType.BOOLEAN, "true"),
            (TokenType.BOOLEAN, "false"),
            (TokenType.CHARACTER, "'a'"),
        ]
        
        self.assertEqual(token_data, expected)
    
    def test_scan_identifiers(self):
        """
        测试扫描标识符
        """
        code = "x y123 _abc"
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        token_data = []
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            token_data.append((token.type, token.lexeme))
        
        expected = [
            (TokenType.IDENTIFIER, "x"),
            (TokenType.IDENTIFIER, "y123"),
            (TokenType.IDENTIFIER, "_abc"),
        ]
        
        self.assertEqual(token_data, expected)
    
    def test_scan_punctuation(self):
        """
        测试扫描标点符号
        """
        code = "() {} [] , ; : ."
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        token_data = []
        for token in tokens:
            if token.type == TokenType.EOF:
                break
            token_data.append((token.type, token.lexeme))
        
        expected = [
            (TokenType.LPAREN, "("),
            (TokenType.RPAREN, ")"),
            (TokenType.LBRACE, "{"),
            (TokenType.RBRACE, "}"),
            (TokenType.LBRACKET, "["),
            (TokenType.RBRACKET, "]"),
            (TokenType.COMMA, ","),
            (TokenType.SEMICOLON, ";"),
            (TokenType.COLON, ":"),
            (TokenType.DOT, "."),
        ]
        
        self.assertEqual(token_data, expected)

if __name__ == '__main__':
    unittest.main()
