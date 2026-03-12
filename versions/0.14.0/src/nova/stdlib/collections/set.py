"""
Nova语言标准库集合模块
"""

class Set:
    """
    集合类型
    """
    
    def __init__(self, items=None):
        """
        初始化集合
        
        Args:
            items: 初始项
        """
        self.items = set(items) if items else set()
    
    def __len__(self):
        """
        获取集合长度
        
        Returns:
            int: 集合长度
        """
        return len(self.items)
    
    def __contains__(self, value):
        """
        检查是否包含元素
        
        Args:
            value: 值
        
        Returns:
            bool: 是否包含
        """
        return value in self.items
    
    def add(self, value):
        """
        添加元素
        
        Args:
            value: 值
        """
        self.items.add(value)
    
    def clear(self):
        """
        清空集合
        """
        self.items.clear()
    
    def copy(self):
        """
        复制集合
        
        Returns:
            Set: 复制的集合
        """
        return Set(self.items)
    
    def difference(self, other):
        """
        计算差集
        
        Args:
            other: 另一个集合
        
        Returns:
            Set: 差集
        """
        if isinstance(other, Set):
            return Set(self.items.difference(other.items))
        else:
            return Set(self.items.difference(other))
    
    def difference_update(self, other):
        """
        更新为差集
        
        Args:
            other: 另一个集合
        """
        if isinstance(other, Set):
            self.items.difference_update(other.items)
        else:
            self.items.difference_update(other)
    
    def discard(self, value):
        """
        移除元素
        
        Args:
            value: 值
        """
        self.items.discard(value)
    
    def intersection(self, other):
        """
        计算交集
        
        Args:
            other: 另一个集合
        
        Returns:
            Set: 交集
        """
        if isinstance(other, Set):
            return Set(self.items.intersection(other.items))
        else:
            return Set(self.items.intersection(other))
    
    def intersection_update(self, other):
        """
        更新为交集
        
        Args:
            other: 另一个集合
        """
        if isinstance(other, Set):
            self.items.intersection_update(other.items)
        else:
            self.items.intersection_update(other)
    
    def isdisjoint(self, other):
        """
        检查是否不相交
        
        Args:
            other: 另一个集合
        
        Returns:
            bool: 是否不相交
        """
        if isinstance(other, Set):
            return self.items.isdisjoint(other.items)
        else:
            return self.items.isdisjoint(other)
    
    def issubset(self, other):
        """
        检查是否是子集
        
        Args:
            other: 另一个集合
        
        Returns:
            bool: 是否是子集
        """
        if isinstance(other, Set):
            return self.items.issubset(other.items)
        else:
            return self.items.issubset(other)
    
    def issuperset(self, other):
        """
        检查是否是超集
        
        Args:
            other: 另一个集合
        
        Returns:
            bool: 是否是超集
        """
        if isinstance(other, Set):
            return self.items.issuperset(other.items)
        else:
            return self.items.issuperset(other)
    
    def pop(self):
        """
        弹出元素
        
        Returns:
            Any: 弹出的元素
        """
        return self.items.pop()
    
    def remove(self, value):
        """
        移除元素
        
        Args:
            value: 值
        """
        self.items.remove(value)
    
    def symmetric_difference(self, other):
        """
        计算对称差集
        
        Args:
            other: 另一个集合
        
        Returns:
            Set: 对称差集
        """
        if isinstance(other, Set):
            return Set(self.items.symmetric_difference(other.items))
        else:
            return Set(self.items.symmetric_difference(other))
    
    def symmetric_difference_update(self, other):
        """
        更新为对称差集
        
        Args:
            other: 另一个集合
        """
        if isinstance(other, Set):
            self.items.symmetric_difference_update(other.items)
        else:
            self.items.symmetric_difference_update(other)
    
    def union(self, other):
        """
        计算并集
        
        Args:
            other: 另一个集合
        
        Returns:
            Set: 并集
        """
        if isinstance(other, Set):
            return Set(self.items.union(other.items))
        else:
            return Set(self.items.union(other))
    
    def update(self, other):
        """
        更新为并集
        
        Args:
            other: 另一个集合
        """
        if isinstance(other, Set):
            self.items.update(other.items)
        else:
            self.items.update(other)
    
    def __str__(self):
        """
        获取集合的字符串表示
        
        Returns:
            str: 字符串表示
        """
        return str(self.items)
