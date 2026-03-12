"""
Nova语言词法分析器扫描器
"""

from .tokens import Token, TokenType
from .errors import LexerError

class Scanner:
    """
    词法分析器扫描器
    
    负责将源代码文本转换为Token序列
    """
    
    def __init__(self, source):
        """
        初始化扫描器
        
        Args:
            source: 源代码文本
        """
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        
        # 关键字映射
        self.keywords = {
            'mod': TokenType.MOD,
            'module': TokenType.MOD,
            'use': TokenType.USE,
            'from': TokenType.FROM,
            'import': TokenType.IMPORT,
            'feature': TokenType.FEATURE,
            'as': TokenType.AS,
            'func': TokenType.FUNC,
            'fn': TokenType.FUNC,
            'let': TokenType.LET,
            'var': TokenType.VAR,
            'const': TokenType.CONST,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'loop': TokenType.LOOP,
            'match': TokenType.MATCH,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'struct': TokenType.STRUCT,
            'enum': TokenType.ENUM,
            'trait': TokenType.TRAIT,
            'impl': TokenType.IMPL,
            'self': TokenType.SELF,
            'async': TokenType.ASYNC,
            'await': TokenType.AWAIT,
            'actor': TokenType.ACTOR,
            'generic': TokenType.GENERIC,
            'where': TokenType.WHERE,
            'in': TokenType.IN,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
        }
    
    def scan_tokens(self):
        """
        扫描所有Token
        
        Returns:
            list: Token列表
        
        Raises:
            LexerError: 词法分析错误
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        # 添加EOF Token
        self.tokens.append(Token(TokenType.EOF, '', None, self.line, self.column))
        return self.tokens
    
    def scan_token(self):
        """
        扫描单个Token
        """
        c = self.advance()
        
        # 处理空白字符
        if c in [' ', '\t', '\r']:
            self.column += 1
            return
        elif c == '\n':
            self.line += 1
            self.column = 1
            return
        
        # 处理注释
        elif c == '/':
            if self.match('/'):
                # 单行注释
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
                return
            elif self.match('*'):
                # 多行注释
                self.scan_multiline_comment()
                return
            else:
                self.add_token(TokenType.DIVIDE)
        
        # 处理字符串
        elif c == '"':
            self.scan_string()
        
        # 处理字符
        elif c == "'":
            self.scan_character()
        
        # 处理数字
        elif c.isdigit():
            self.scan_number()
        # 处理标识符和关键字（包括以双下划线开头的标识符）
        elif c.isalpha() or c == '_':
            self.scan_identifier()
        

        elif c == '!':
            if self.match('='):
                self.add_token(TokenType.NOT_EQUALS)
            else:
                self.add_token(TokenType.NOT)
        elif c == '<':
            if self.match('<'):
                if self.match('<'):
                    self.add_token(TokenType.ASSIGN)
                else:
                    self.add_token(TokenType.ASSIGN)
            elif self.match('='):
                self.add_token(TokenType.LESS_THAN_OR_EQUAL)
            else:
                self.add_token(TokenType.LESS_THAN)
        elif c == '>':
            if self.match('>'):
                if self.match('>'):
                    self.add_token(TokenType.ASSIGN)
                else:
                    self.add_token(TokenType.ASSIGN)
            elif self.match('='):
                self.add_token(TokenType.GREATER_THAN_OR_EQUAL)
            else:
                self.add_token(TokenType.GREATER_THAN)
        elif c == '+':
            if self.match('='):
                self.add_token(TokenType.PLUS_ASSIGN)
            else:
                self.add_token(TokenType.PLUS)
        elif c == '-':
            if self.match('='):
                self.add_token(TokenType.MINUS_ASSIGN)
            elif self.match('>'):
                self.add_token(TokenType.ARROW)
            else:
                self.add_token(TokenType.MINUS)
        elif c == '=':
            if self.match('>'):
                self.add_token(TokenType.DOUBLE_ARROW)
            elif self.match('='):
                self.add_token(TokenType.EQUALS)
            else:
                self.add_token(TokenType.ASSIGN)
        elif c == '*':
            if self.match('='):
                self.add_token(TokenType.MULTIPLY_ASSIGN)
            else:
                self.add_token(TokenType.MULTIPLY)
        elif c == '/':
            if self.match('='):
                self.add_token(TokenType.DIVIDE_ASSIGN)
            else:
                self.add_token(TokenType.DIVIDE)
        elif c == '%':
            self.add_token(TokenType.MODULO)
        elif c == '&':
            if self.match('&'):
                self.add_token(TokenType.AND)
            else:
                self.add_token(TokenType.AND)
        elif c == '|':
            if self.match('|'):
                self.add_token(TokenType.OR)
            else:
                self.add_token(TokenType.OR)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == ':':
            if self.match(':'):
                self.add_token(TokenType.DOT)
            else:
                self.add_token(TokenType.COLON)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '(': 
            self.add_token(TokenType.LPAREN)
        elif c == ')':
            self.add_token(TokenType.RPAREN)
        elif c == '{':
            self.add_token(TokenType.LBRACE)
        elif c == '}':
            self.add_token(TokenType.RBRACE)
        elif c == '[':
            self.add_token(TokenType.LBRACKET)
        elif c == ']':
            self.add_token(TokenType.RBRACKET)
        elif c == '?':
            self.add_token(TokenType.QUESTION_MARK)
        elif c == '!':
            self.add_token(TokenType.EXCLAMATION_MARK)
        elif c == '^':
            self.add_token(TokenType.ASSIGN)
        elif c == '~':
            self.add_token(TokenType.ASSIGN)
        else:
            self.error(f"Unexpected character '{c}'")
    
    def scan_string(self):
        """
        扫描字符串字面量
        """
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            self.advance()
        
        if self.is_at_end():
            self.error("Unterminated string")
            return
        
        # 消耗 closing quote
        self.advance()
        
        # 获取字符串值
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
    
    def scan_character(self):
        """
        扫描字符字面量
        """
        if self.is_at_end():
            self.error("Unterminated character")
            return
        
        # 消耗字符
        self.advance()
        
        # 检查是否有 closing quote
        if self.peek() != "'":
            self.error("Character must be a single character")
            return
        
        # 消耗 closing quote
        self.advance()
        
        # 获取字符值
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.CHARACTER, value)
    
    def scan_number(self):
        """
        扫描数字字面量
        """
        while self.peek().isdigit():
            self.advance()
        
        # 检查是否是浮点数
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()  # 消耗 '.'
            while self.peek().isdigit():
                self.advance()
            value = float(self.source[self.start:self.current])
            self.add_token(TokenType.FLOAT, value)
        else:
            value = int(self.source[self.start:self.current])
            self.add_token(TokenType.INTEGER, value)
    
    def scan_identifier(self):
        """
        扫描标识符
        """
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        
        text = self.source[self.start:self.current]
        
        # 检查是否是特殊的双下划线标识符
        if text == "__future__":
            self.add_token(TokenType.IDENTIFIER)
            return
        
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        
        # 处理布尔值
        if token_type in [TokenType.TRUE, TokenType.FALSE]:
            value = text == 'true'
            self.add_token(token_type, value)
        else:
            self.add_token(token_type)
    
    def scan_multiline_comment(self):
        """
        扫描多行注释
        """
        while not (self.peek() == '*' and self.peek_next() == '/') and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            self.advance()
        
        if self.is_at_end():
            self.error("Unterminated comment")
            return
        
        # 消耗 closing */
        self.advance()
        self.advance()
    
    def advance(self):
        """
        前进一个字符
        
        Returns:
            str: 当前字符
        """
        c = self.source[self.current]
        self.current += 1
        return c
    
    def match(self, expected):
        """
        匹配下一个字符
        
        Args:
            expected: 期望的字符
        
        Returns:
            bool: 是否匹配
        """
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True
    
    def peek(self):
        """
        查看下一个字符
        
        Returns:
            str: 下一个字符
        """
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self):
        """
        查看下下个字符
        
        Returns:
            str: 下下个字符
        """
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def is_at_end(self):
        """
        是否到达文件末尾
        
        Returns:
            bool: 是否到达文件末尾
        """
        return self.current >= len(self.source)
    
    def add_token(self, type, literal=None):
        """
        添加Token
        
        Args:
            type: Token类型
            literal: 字面量值
        """
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line, self.column - len(text)))
    
    def error(self, message):
        """
        报告错误
        
        Args:
            message: 错误信息
        
        Raises:
            LexerError: 词法分析错误
        """
        raise LexerError(self.line, self.column, message)
