"""
Nova语言语义分析器错误
"""

class SemanticError(Exception):
    """
    语义分析错误
    
    Attributes:
        line: 错误行号
        column: 错误列号
        message: 错误信息
    """
    
    def __init__(self, line, column, message):
        """
        初始化语义分析错误
        
        Args:
            line: 错误行号
            column: 错误列号
            message: 错误信息
        """
        self.line = line
        self.column = column
        self.message = message
        super().__init__(f"Semantic error at {line}:{column}: {message}")
