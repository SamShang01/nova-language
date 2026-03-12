"""
Nova语言标准库字典模块
"""

class Dict:
    """
    字典类型
    """
    
    def __init__(self, items=None):
        """
        初始化字典
        
        Args:
            items: 初始项
        """
        self.items = {}
        if items:
            if isinstance(items, Dict):
                self.items = items.items.copy()
            elif isinstance(items, dict):
                self.items = items.copy()
            else:
                for key, value in items:
                    self.items[key] = value
    
    def __len__(self):
        """
        获取字典长度
        
        Returns:
            int: 字典长度
        """
        return len(self.items)
    
    def __getitem__(self, key):
        """
        获取指定键的值
        
        Args:
            key: 键
        
        Returns:
            Any: 值
        """
        return self.items[key]
    
    def __setitem__(self, key, value):
        """
        设置指定键的值
        
        Args:
            key: 键
            value: 值
        """
        self.items[key] = value
    
    def __delitem__(self, key):
        """
        删除指定键的项
        
        Args:
            key: 键
        """
        del self.items[key]
    
    def clear(self):
        """
        清空字典
        """
        self.items.clear()
    
    def copy(self):
        """
        复制字典
        
        Returns:
            Dict: 复制的字典
        """
        return Dict(self.items.items())
    
    def get(self, key, default=None):
        """
        获取指定键的值，如果键不存在则返回默认值
        
        Args:
            key: 键
            default: 默认值
        
        Returns:
            Any: 值或默认值
        """
        return self.items.get(key, default)
    
    def items(self):
        """
        获取字典的项
        
        Returns:
            dict_items: 字典的项
        """
        return self.items.items()
    
    def keys(self):
        """
        获取字典的键
        
        Returns:
            dict_keys: 字典的键
        """
        return self.items.keys()
    
    def values(self):
        """
        获取字典的值
        
        Returns:
            dict_values: 字典的值
        """
        return self.items.values()
    
    def pop(self, key, default=None):
        """
        弹出指定键的项
        
        Args:
            key: 键
            default: 默认值
        
        Returns:
            Any: 弹出的值或默认值
        """
        return self.items.pop(key, default)
    
    def popitem(self):
        """
        弹出一个项
        
        Returns:
            tuple: 弹出的项
        """
        return self.items.popitem()
    
    def setdefault(self, key, default=None):
        """
        设置默认值
        
        Args:
            key: 键
            default: 默认值
        
        Returns:
            Any: 值或默认值
        """
        return self.items.setdefault(key, default)
    
    def update(self, other):
        """
        更新字典
        
        Args:
            other: 另一个字典
        """
        if isinstance(other, Dict):
            self.items.update(other.items)
        else:
            self.items.update(other)
    
    def __str__(self):
        """
        获取字典的字符串表示
        
        Returns:
            str: 字符串表示
        """
        return str(self.items)
