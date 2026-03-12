"""
Nova语言标准库流模块
"""

import sys

class Stream:
    """
    流基类
    """
    
    def __init__(self, stream):
        """
        初始化流
        
        Args:
            stream: 底层流对象
        """
        self.stream = stream
    
    def read(self, size=-1):
        """
        读取数据
        
        Args:
            size: 读取大小
        
        Returns:
            str: 读取的内容
        """
        return self.stream.read(size)
    
    def readline(self, size=-1):
        """
        读取一行
        
        Args:
            size: 读取大小
        
        Returns:
            str: 读取的行
        """
        return self.stream.readline(size)
    
    def readlines(self, hint=-1):
        """
        读取所有行
        
        Args:
            hint: 提示大小
        
        Returns:
            list: 读取的行列表
        """
        return self.stream.readlines(hint)
    
    def write(self, data):
        """
        写入数据
        
        Args:
            data: 要写入的数据
        
        Returns:
            int: 写入的字节数
        """
        return self.stream.write(data)
    
    def writelines(self, lines):
        """
        写入多行
        
        Args:
            lines: 要写入的行列表
        """
        return self.stream.writelines(lines)
    
    def flush(self):
        """
        刷新流
        """
        return self.stream.flush()

# 标准输入流
stdin = Stream(sys.stdin)

# 标准输出流
stdout = Stream(sys.stdout)

# 标准错误流
stderr = Stream(sys.stderr)
