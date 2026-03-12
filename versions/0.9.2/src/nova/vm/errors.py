"""
Nova语言虚拟机错误
"""

class VMError(Exception):
    """
    虚拟机错误
    """
    
    def __init__(self, message):
        """
        初始化虚拟机错误
        
        Args:
            message: 错误信息
        """
        super().__init__(message)

class MemoryError(VMError):
    """
    内存错误
    """
    
    def __init__(self, message):
        """
        初始化内存错误
        
        Args:
            message: 错误信息
        """
        super().__init__(f"Memory error: {message}")

class StackError(VMError):
    """
    栈错误
    """
    
    def __init__(self, message):
        """
        初始化栈错误
        
        Args:
            message: 错误信息
        """
        super().__init__(f"Stack error: {message}")

class InstructionError(VMError):
    """
    指令错误
    """
    
    def __init__(self, message):
        """
        初始化指令错误
        
        Args:
            message: 错误信息
        """
        super().__init__(f"Instruction error: {message}")

class EnvironmentError(VMError):
    """
    环境错误
    """
    
    def __init__(self, message):
        """
        初始化环境错误
        
        Args:
            message: 错误信息
        """
        super().__init__(f"Environment error: {message}")
