"""
Nova语言标准库列表模块
"""

class List:
    """
    列表类型
    """
    
    def __init__(self, items=None):
        """
        初始化列表
        
        Args:
            items: 初始项
        """
        self.items = items or []
    
    def __len__(self):
        """
        获取列表长度
        
        Returns:
            int: 列表长度
        """
        return len(self.items)
    
    def __getitem__(self, index):
        """
        获取指定索引的元素
        
        Args:
            index: 索引
        
        Returns:
            Any: 元素
        """
        return self.items[index]
    
    def __setitem__(self, index, value):
        """
        设置指定索引的元素
        
        Args:
            index: 索引
            value: 值
        """
        self.items[index] = value
    
    def append(self, value):
        """
        添加元素到列表末尾
        
        Args:
            value: 值
        """
        self.items.append(value)
    
    def extend(self, other):
        """
        扩展列表
        
        Args:
            other: 另一个列表
        """
        if isinstance(other, List):
            self.items.extend(other.items)
        else:
            self.items.extend(other)
    
    def insert(self, index, value):
        """
        在指定位置插入元素
        
        Args:
            index: 索引
            value: 值
        """
        self.items.insert(index, value)
    
    def remove(self, value):
        """
        移除指定值的元素
        
        Args:
            value: 值
        """
        self.items.remove(value)
    
    def pop(self, index=-1):
        """
        弹出指定索引的元素
        
        Args:
            index: 索引
        
        Returns:
            Any: 弹出的元素
        """
        return self.items.pop(index)
    
    def clear(self):
        """
        清空列表
        """
        self.items.clear()
    
    def index(self, value, start=0, end=None):
        """
        获取指定值的索引
        
        Args:
            value: 值
            start: 开始索引
            end: 结束索引
        
        Returns:
            int: 索引
        """
        return self.items.index(value, start, end)
    
    def count(self, value):
        """
        统计指定值的出现次数
        
        Args:
            value: 值
        
        Returns:
            int: 出现次数
        """
        return self.items.count(value)
    
    def sort(self, key=None, reverse=False):
        """
        排序列表
        
        Args:
            key: 排序键
            reverse: 是否反转
        """
        self.items.sort(key=key, reverse=reverse)
    
    def reverse(self):
        """
        反转列表
        """
        self.items.reverse()
    
    def copy(self):
        """
        复制列表
        
        Returns:
            List: 复制的列表
        """
        return List(self.items.copy())
    
    def __str__(self):
        """
        获取列表的字符串表示
        
        Returns:
            str: 字符串表示
        """
        return str(self.items)
