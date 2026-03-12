"""
Nova语言标准库文件操作模块
"""

class File:
    """
    文件类
    """
    
    def __init__(self, path, mode='r'):
        """
        初始化文件
        
        Args:
            path: 文件路径
            mode: 打开模式
        """
        self.path = path
        self.mode = mode
        self.file = None
        self._open()
    
    def _open(self):
        """
        打开文件
        """
        self.file = open(self.path, self.mode)
    
    def read(self, size=-1):
        """
        读取文件
        
        Args:
            size: 读取大小
        
        Returns:
            str: 读取的内容
        """
        if not self.file:
            raise ValueError("File not opened")
        return self.file.read(size)
    
    def readline(self, size=-1):
        """
        读取一行
        
        Args:
            size: 读取大小
        
        Returns:
            str: 读取的行
        """
        if not self.file:
            raise ValueError("File not opened")
        return self.file.readline(size)
    
    def readlines(self, hint=-1):
        """
        读取所有行
        
        Args:
            hint: 提示大小
        
        Returns:
            list: 读取的行列表
        """
        if not self.file:
            raise ValueError("File not opened")
        return self.file.readlines(hint)
    
    def write(self, data):
        """
        写入数据
        
        Args:
            data: 要写入的数据
        
        Returns:
            int: 写入的字节数
        """
        if not self.file:
            raise ValueError("File not opened")
        return self.file.write(data)
    
    def writelines(self, lines):
        """
        写入多行
        
        Args:
            lines: 要写入的行列表
        """
        if not self.file:
            raise ValueError("File not opened")
        self.file.writelines(lines)
    
    def seek(self, offset, whence=0):
        """
        移动文件指针
        
        Args:
            offset: 偏移量
            whence: 参考位置
        """
        if not self.file:
            raise ValueError("File not opened")
        self.file.seek(offset, whence)
    
    def tell(self):
        """
        获取文件指针位置
        
        Returns:
            int: 文件指针位置
        """
        if not self.file:
            raise ValueError("File not opened")
        return self.file.tell()
    
    def close(self):
        """
        关闭文件
        """
        if self.file:
            self.file.close()
            self.file = None
    
    def __enter__(self):
        """
        进入上下文
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文
        """
        self.close()

# 便捷函数
def open(path, mode='r'):
    """
    打开文件
    
    Args:
        path: 文件路径
        mode: 打开模式
    
    Returns:
        File: 文件对象
    """
    return File(path, mode)

def read(path, size=-1):
    """
    读取文件
    
    Args:
        path: 文件路径
        size: 读取大小
    
    Returns:
        str: 读取的内容
    """
    with open(path, 'r') as f:
        return f.read(size)

def write(path, data):
    """
    写入文件
    
    Args:
        path: 文件路径
        data: 要写入的数据
    """
    with open(path, 'w') as f:
        f.write(data)

def close(file):
    """
    关闭文件
    
    Args:
        file: 文件对象
    """
    if file:
        file.close()
