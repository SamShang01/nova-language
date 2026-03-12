"""
Nova语言语法分析器错误
"""

class ParserError(Exception):
    """
    语法分析错误
    
    Attributes:
        line: 错误行号
        column: 错误列号
        message: 错误信息
    """
    
    def __init__(self, line, column, message):
        """
        初始化语法分析错误
        
        Args:
            line: 错误行号
            column: 错误列号
            message: 错误信息
        """
        self.line = line
        self.column = column
        self.message = message
        super().__init__(f"Parser error at {line}:{column}: {message}")
