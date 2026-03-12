"""
Nova语言语义分析器作用域管理
"""

class Scope:
    """
    作用域
    
    Attributes:
        name: 作用域名称
        parent: 父作用域
        symbols: 符号字典，键为符号名称，值为符号对象
    """
    
    def __init__(self, name, parent=None):
        """
        初始化作用域
        
        Args:
            name: 作用域名称
            parent: 父作用域
        """
        self.name = name
        self.parent = parent
        self.symbols = {}
    
    def declare_symbol(self, symbol):
        """
        声明符号
        
        Args:
            symbol: 符号对象
        
        Raises:
            ValueError: 如果符号已存在
        """
        if symbol.name in self.symbols:
            raise ValueError(f"Symbol '{symbol.name}' already exists in scope '{self.name}'")
        self.symbols[symbol.name] = symbol
    
    def resolve_symbol(self, name):
        """
        解析符号
        
        Args:
            name: 符号名称
        
        Returns:
            Symbol: 符号对象，如果未找到则返回None
        """
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.resolve_symbol(name)
        else:
            return None
    
    def has_symbol(self, name):
        """
        检查作用域是否包含符号
        
        Args:
            name: 符号名称
        
        Returns:
            bool: 是否包含符号
        """
        if name in self.symbols:
            return True
        elif self.parent:
            return self.parent.has_symbol(name)
        else:
            return False
    
    def get_local_symbol(self, name):
        """
        获取本地作用域中的符号
        
        Args:
            name: 符号名称
        
        Returns:
            Symbol: 符号对象，如果未找到则返回None
        """
        return self.symbols.get(name)
    
    def remove_symbol(self, name):
        """
        从本地作用域中删除符号
        
        Args:
            name: 符号名称
        
        Returns:
            bool: 是否成功删除
        """
        if name in self.symbols:
            del self.symbols[name]
            return True
        return False
    
    def __str__(self):
        return f"Scope('{self.name}', parent='{self.parent.name if self.parent else None}')"
