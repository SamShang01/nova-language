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
            'function': TokenType.FUNC,
            'let': TokenType.LET,
            'var': TokenType.VAR,
            'const': TokenType.CONST,
            'del': TokenType.DEL,
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
            'union': TokenType.UNION,
            'trait': TokenType.TRAIT,
            'impl': TokenType.IMPL,
            'self': TokenType.SELF,
            'async': TokenType.ASYNC,
            'await': TokenType.AWAIT,
            'actor': TokenType.ACTOR,
            'generic': TokenType.GENERIC,
            'template': TokenType.TEMPLATE,
            'where': TokenType.WHERE,
            'in': TokenType.IN,
            'manda': TokenType.MANDA,
            'default': TokenType.DEFAULT,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
            'int': TokenType.IDENTIFIER,
            'float': TokenType.IDENTIFIER,
            'double': TokenType.IDENTIFIER,
            'string': TokenType.IDENTIFIER,
            'bool': TokenType.IDENTIFIER,
            'char': TokenType.IDENTIFIER,
            'void': TokenType.IDENTIFIER,
            # 访问修饰符
            'private': TokenType.PRIVATE,
            'protected': TokenType.PROTECTED,
            'public': TokenType.PUBLIC,
            # 类相关关键字
            'class': TokenType.CLASS,
            'extends': TokenType.EXTENDS,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            # 构造函数
            'init': TokenType.INIT,
            # 静态关键字
            'static': TokenType.STATIC,
            # 抽象关键字
            'abstract': TokenType.ABSTRACT,
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
        elif c == 'f' and self.peek() == '"':
            # 处理f-string
            self.advance()  # 消耗 'f'
            self.scan_f_string()
        elif c == '"':
            self.scan_string()
        elif c == "'":
            # 检查是否是字符字面量还是字符串
            # 如果下一个字符是字母或数字，且再下一个字符是单引号，则是字符字面量
            # 否则，视为字符串
            if not self.is_at_end() and self.peek() != '\n' and not self.is_at_end() and self.peek_next() == "'":
                self.scan_character()
            else:
                # 单引号字符串
                self.scan_string_with_quote("'")
        
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
            elif self.match('*'):
                self.add_token(TokenType.STAR_STAR)
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
            if self.match('.'):
                self.add_token(TokenType.OPTIONAL_CHAIN)
            elif self.match('?'):
                self.add_token(TokenType.NULL_COALESCING)
            else:
                self.add_token(TokenType.QUESTION_MARK)
        elif c == '!':
            self.add_token(TokenType.EXCLAMATION_MARK)
        elif c == '^':
            self.add_token(TokenType.ASSIGN)
        elif c == '~':
            self.add_token(TokenType.ASSIGN)
        elif c == '@':
            self.add_token(TokenType.AT)
        else:
            self.error(f"Unexpected character '{c}'")
    
    def scan_string(self):
        """
        扫描字符串字面量（双引号）
        """
        self.scan_string_with_quote('"')
    
    def scan_string_with_quote(self, quote_char):
        """
        扫描字符串字面量（通用）
        
        Args:
            quote_char: 引号字符
        """
        while self.peek() != quote_char and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            self.advance()
        
        if self.is_at_end():
            self.error(f"Unterminated string with quote '{quote_char}'")
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
        支持不同进制：
        - 十进制：默认
        - 十六进制：0x或0X前缀
        - 八进制：0o或0O前缀，或0前缀
        - 二进制：0b或0B前缀
        支持浮点数：
        - 普通浮点数：123.456
        - 双精度浮点数：123.456D或123.456d
        """
        # 检查是否有进制前缀
        base = 10
        is_float = False
        has_d_suffix = False
        
        # 检查是否是0开头的特殊进制
        if self.source[self.start] == '0' and self.current > self.start:
            if self.current - self.start == 1:
                next_char = self.peek().lower()
                if next_char == 'x':
                    # 十六进制
                    base = 16
                    self.advance()  # 消耗 'x' 或 'X'
                    # 十六进制数字：0-9, a-f, A-F
                    while self.peek().isdigit() or ('a' <= self.peek().lower() <= 'f'):
                        self.advance()
                elif next_char == 'o':
                    # 八进制（0o前缀）
                    base = 8
                    self.advance()  # 消耗 'o' 或 'O'
                    # 八进制数字：0-7
                    while self.peek().isdigit() and int(self.peek()) < 8:
                        self.advance()
                elif next_char == 'b':
                    # 二进制
                    base = 2
                    self.advance()  # 消耗 'b' 或 'B'
                    # 二进制数字：0-1
                    while self.peek().isdigit() and int(self.peek()) < 2:
                        self.advance()
                elif next_char == 'f':
                    # 斐波那契进制（0f或0F前缀）
                    base = 'fibonacci'
                    self.advance()  # 消耗 'f' 或 'F'
                    # 斐波那契进制数字：0和1，且没有连续的1
                    while self.peek().isdigit() and int(self.peek()) in [0, 1]:
                        self.advance()
                elif self.peek().isdigit():
                    # 八进制（0前缀）
                    base = 8
                    while self.peek().isdigit() and int(self.peek()) < 8:
                        self.advance()
                elif self.peek() == '.':
                    # 浮点数，如0.123
                    is_float = True
                    self.advance()  # 消耗 '.'
                    while self.peek().isdigit():
                        self.advance()
                else:
                    # 单独的0
                    pass
        else:
            # 十进制数字
            while self.peek().isdigit():
                self.advance()
            
            # 检查是否是浮点数
            if self.peek() == '.' and self.peek_next().isdigit():
                is_float = True
                self.advance()  # 消耗 '.'
                while self.peek().isdigit():
                    self.advance()
        
        # 检查是否有D后缀（双精度浮点数）
        if self.peek().upper() == 'D':
            has_d_suffix = True
            is_float = True
            self.advance()  # 消耗 'D' 或 'd'
        
    def _fibonacci_to_decimal(self, fib_str):
        """
        将斐波那契进制字符串转换为十进制整数
        斐波那契进制规则：
        - 数字只包含0和1
        - 没有连续的1
        - 基数是斐波那契数列：1, 2, 3, 5, 8, 13, ...
        
        Args:
            fib_str: 斐波那契进制字符串（不包含前缀）
            
        Returns:
            int: 转换后的十进制整数
        """
        # 检查是否有连续的1
        for i in range(len(fib_str) - 1):
            if fib_str[i] == '1' and fib_str[i+1] == '1':
                raise ValueError(f"Invalid Fibonacci number: consecutive 1s in {fib_str}")
        
        # 计算斐波那契数列
        fib = [1, 2]  # 从F(2)=1, F(3)=2开始
        while len(fib) < len(fib_str):
            fib.append(fib[-1] + fib[-2])
        
        # 反转字符串，从最低位开始计算
        fib_str_reversed = fib_str[::-1]
        decimal = 0
        
        for i, bit in enumerate(fib_str_reversed):
            if bit == '1':
                decimal += fib[i]
        
        return decimal

    def scan_number(self):
        """
        扫描数字字面量
        支持不同进制：
        - 十进制：默认
        - 十六进制：0x或0X前缀
        - 八进制：0o或0O前缀，或0前缀
        - 二进制：0b或0B前缀
        - 斐波那契进制：0f或0F前缀
        支持浮点数：
        - 普通浮点数：123.456
        - 双精度浮点数：123.456D或123.456d
        """
        # 检查是否有进制前缀
        base = 10
        is_float = False
        has_d_suffix = False
        
        # 检查是否是0开头的特殊进制
        if self.source[self.start] == '0' and self.current > self.start:
            if self.current - self.start == 1:
                next_char = self.peek().lower()
                if next_char == 'x':
                    # 十六进制
                    base = 16
                    self.advance()  # 消耗 'x' 或 'X'
                    # 十六进制数字：0-9, a-f, A-F
                    while self.peek().isdigit() or ('a' <= self.peek().lower() <= 'f'):
                        self.advance()
                elif next_char == 'o':
                    # 八进制（0o前缀）
                    base = 8
                    self.advance()  # 消耗 'o' 或 'O'
                    # 八进制数字：0-7
                    while self.peek().isdigit() and int(self.peek()) < 8:
                        self.advance()
                elif next_char == 'b':
                    # 二进制
                    base = 2
                    self.advance()  # 消耗 'b' 或 'B'
                    # 二进制数字：0-1
                    while self.peek().isdigit() and int(self.peek()) < 2:
                        self.advance()
                elif next_char == 'f':
                    # 斐波那契进制（0f或0F前缀）
                    base = 'fibonacci'
                    self.advance()  # 消耗 'f' 或 'F'
                    # 斐波那契进制数字：0和1，且没有连续的1
                    while self.peek().isdigit() and int(self.peek()) in [0, 1]:
                        self.advance()
                elif self.peek().isdigit():
                    # 八进制（0前缀）
                    base = 8
                    while self.peek().isdigit() and int(self.peek()) < 8:
                        self.advance()
                elif self.peek() == '.':
                    # 浮点数，如0.123
                    is_float = True
                    self.advance()  # 消耗 '.'
                    while self.peek().isdigit():
                        self.advance()
                else:
                    # 单独的0
                    pass
        else:
            # 十进制数字
            while self.peek().isdigit():
                self.advance()
            
            # 检查是否是浮点数
            if self.peek() == '.' and self.peek_next().isdigit():
                is_float = True
                self.advance()  # 消耗 '.'
                while self.peek().isdigit():
                    self.advance()
        
        # 检查是否有D后缀（双精度浮点数）
        if self.peek().upper() == 'D':
            has_d_suffix = True
            is_float = True
            self.advance()  # 消耗 'D' 或 'd'
        
        # 转换为适当的类型
        value_str = self.source[self.start:self.current]
        if is_float:
            # 对于浮点数，去掉D后缀后转换
            if has_d_suffix:
                value_str = value_str[:-1]  # 去掉末尾的D
            value = float(value_str)
            self.add_token(TokenType.FLOAT, value)
        else:
            # 对于整数，根据进制转换
            if base == 10:
                value = int(value_str)
            elif base == 'fibonacci':
                # 斐波那契进制转换
                fib_str = value_str[2:]  # 去掉 '0f' 前缀
                value = self._fibonacci_to_decimal(fib_str)
            else:
                # 对于其他进制，使用int(value_str, base)转换
                # 注意：需要去掉前缀
                if base == 16:
                    value = int(value_str[2:], 16)  # 去掉 '0x' 前缀
                elif base == 8:
                    if value_str.startswith('0o') or value_str.startswith('0O'):
                        value = int(value_str[2:], 8)  # 去掉 '0o' 前缀
                    else:
                        value = int(value_str, 8)  # 直接使用0前缀
                elif base == 2:
                    value = int(value_str[2:], 2)  # 去掉 '0b' 前缀
                else:
                    value = int(value_str)
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
    
    def scan_f_string(self):
        """
        扫描f-string字面量
        """
        self.add_token(TokenType.F_STRING_START)
        
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            elif self.peek() == '{':
                # 处理f-string中的表达式
                self.add_token(TokenType.F_STRING_EXPRESSION_START)
                self.advance()  # 消耗 '{'
                # 这里需要递归扫描表达式内容
                # 简化处理，直接扫描到对应的 '}'
                brace_count = 1
                while brace_count > 0 and not self.is_at_end():
                    if self.peek() == '{':
                        brace_count += 1
                    elif self.peek() == '}':
                        brace_count -= 1
                    elif self.peek() == '\n':
                        self.line += 1
                        self.column = 1
                    self.advance()
                if brace_count > 0:
                    self.error("Unterminated expression in f-string")
                    return
                self.add_token(TokenType.F_STRING_EXPRESSION_END)
            else:
                self.advance()
        
        if self.is_at_end():
            self.error("Unterminated f-string")
            return
        
        # 消耗 closing quote
        self.advance()
        
        # 这里可以添加f-string结束的token
        # 但为了简化，我们暂时不添加
    
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
