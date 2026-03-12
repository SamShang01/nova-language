"""
Nova语言Token定义
"""

from enum import Enum

class TokenType(Enum):
    """
    Token类型枚举
    """
    # 关键字
    MOD = 'MOD'
    USE = 'USE'
    FROM = 'FROM'
    IMPORT = 'IMPORT'
    FEATURE = 'FEATURE'
    AS = 'AS'
    FUNC = 'FUNC'
    LET = 'LET'
    VAR = 'VAR'
    CONST = 'CONST'
    DEL = 'DEL'
    IF = 'IF'
    ELSE = 'ELSE'
    FOR = 'FOR'
    WHILE = 'WHILE'
    LOOP = 'LOOP'
    MATCH = 'MATCH'
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'
    RETURN = 'RETURN'
    STRUCT = 'STRUCT'
    ENUM = 'ENUM'
    UNION = 'UNION'
    TRAIT = 'TRAIT'
    IMPL = 'IMPL'
    SELF = 'SELF'
    ASYNC = 'ASYNC'
    AWAIT = 'AWAIT'
    ACTOR = 'ACTOR'
    MESSAGE = 'MESSAGE'
    GENERIC = 'GENERIC'
    TEMPLATE = 'TEMPLATE'
    WHERE = 'WHERE'
    IN = 'IN'
    MANDA = 'MANDA'
    DEFAULT = 'DEFAULT'
    
    # 访问修饰符
    PRIVATE = 'PRIVATE'
    PROTECTED = 'PROTECTED'
    PUBLIC = 'PUBLIC'
    
    # 类相关关键字
    CLASS = 'CLASS'
    EXTENDS = 'EXTENDS'
    SUPER = 'SUPER'
    THIS = 'THIS'
    INIT = 'INIT'
    STATIC = 'STATIC'
    ABSTRACT = 'ABSTRACT'
    MUT = 'MUT'  # 可变引用关键字
    
    # 标识符
    IDENTIFIER = 'IDENTIFIER'
    DOUBLE_UNDERSCORE = 'DOUBLE_UNDERSCORE'
    
    # 字面量
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    BOOLEAN = 'BOOLEAN'
    CHARACTER = 'CHARACTER'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    
    # 运算符
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'
    
    # 比较运算符
    EQUALS = 'EQUALS'
    NOT_EQUALS = 'NOT_EQUALS'
    LESS_THAN = 'LESS_THAN'
    LESS_THAN_OR_EQUAL = 'LESS_THAN_OR_EQUAL'
    GREATER_THAN = 'GREATER_THAN'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'
    
    # 逻辑运算符
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    
    # 赋值运算符
    ASSIGN = 'ASSIGN'
    PLUS_ASSIGN = 'PLUS_ASSIGN'
    MINUS_ASSIGN = 'MINUS_ASSIGN'
    MULTIPLY_ASSIGN = 'MULTIPLY_ASSIGN'
    DIVIDE_ASSIGN = 'DIVIDE_ASSIGN'
    
    # 特殊符号
    DOT = 'DOT'
    COMMA = 'COMMA'
    COLON = 'COLON'
    SEMICOLON = 'SEMICOLON'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    ARROW = 'ARROW'
    DOUBLE_ARROW = 'DOUBLE_ARROW'
    QUESTION_MARK = 'QUESTION_MARK'
    EXCLAMATION_MARK = 'EXCLAMATION_MARK'
    LT = 'LT'
    GT = 'GT'
    STAR = 'STAR'
    STAR_STAR = 'STAR_STAR'
    EQUAL = 'EQUAL'
    AT = 'AT'  # 装饰器符号
    
    # 指针相关
    AMPERSAND = 'AMPERSAND'  # 取地址符 &
    AMPERSAND_MUT = 'AMPERSAND_MUT'  # 可变引用 &mut
    POINTER_TYPE = 'POINTER_TYPE'  # 指针类型 *T
    
    # 类型相关
    TYPE = 'TYPE'  # 类型类型关键字
    
    # 新增操作符
    OPTIONAL_CHAIN = 'OPTIONAL_CHAIN'  # 可选链操作符 ?.
    NULL_COALESCING = 'NULL_COALESCING'  # 空值合并操作符 ??
    # 字符串插值相关
    F_STRING_START = 'F_STRING_START'  # f-string开始
    F_STRING_EXPRESSION_START = 'F_STRING_EXPRESSION_START'  # f-string表达式开始
    F_STRING_EXPRESSION_END = 'F_STRING_EXPRESSION_END'  # f-string表达式结束
    
    # 其他
    COMMENT = 'COMMENT'
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'

class Token:
    """
    Token类
    
    Attributes:
        type: Token类型
        lexeme: 词法单元
        literal: 字面量值
        line: 行号
        column: 列号
    """
    
    def __init__(self, type, lexeme, literal, line, column):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.type.name}, '{self.lexeme}', {self.literal}, {self.line}:{self.column})"
    
    def __repr__(self):
        return self.__str__()
