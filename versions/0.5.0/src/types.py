"""
Nova语言标准库核心类型模块
"""

import builtins

# 基本类型定义
class Int:
    """
    整数类型
    """
    
    def __init__(self, value):
        self.value = builtins.int(value)
    
    def __add__(self, other):
        if isinstance(other, Int):
            return Int(self.value + other.value)
        elif isinstance(other, (int, float)):
            return Int(self.value + other)
        else:
            raise TypeError(f"Cannot add Int with {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, Int):
            return Int(self.value - other.value)
        elif isinstance(other, (int, float)):
            return Int(self.value - other)
        else:
            raise TypeError(f"Cannot subtract {type(other)} from Int")
    
    def __mul__(self, other):
        if isinstance(other, Int):
            return Int(self.value * other.value)
        elif isinstance(other, (int, float)):
            return Int(self.value * other)
        else:
            raise TypeError(f"Cannot multiply Int with {type(other)}")
    
    def __div__(self, other):
        if isinstance(other, Int):
            return Int(self.value // other.value)
        elif isinstance(other, (int, float)):
            return Int(self.value // other)
        else:
            raise TypeError(f"Cannot divide Int by {type(other)}")
    
    def __eq__(self, other):
        if isinstance(other, Int):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        else:
            return False
    
    def __str__(self):
        return str(self.value)

class Float:
    """
    浮点数类型
    """
    
    def __init__(self, value):
        self.value = builtins.float(value)
    
    def __add__(self, other):
        if isinstance(other, Float):
            return Float(self.value + other.value)
        elif isinstance(other, (int, float)):
            return Float(self.value + other)
        else:
            raise TypeError(f"Cannot add Float with {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, Float):
            return Float(self.value - other.value)
        elif isinstance(other, (int, float)):
            return Float(self.value - other)
        else:
            raise TypeError(f"Cannot subtract {type(other)} from Float")
    
    def __mul__(self, other):
        if isinstance(other, Float):
            return Float(self.value * other.value)
        elif isinstance(other, (int, float)):
            return Float(self.value * other)
        else:
            raise TypeError(f"Cannot multiply Float with {type(other)}")
    
    def __div__(self, other):
        if isinstance(other, Float):
            return Float(self.value / other.value)
        elif isinstance(other, (int, float)):
            return Float(self.value / other)
        else:
            raise TypeError(f"Cannot divide Float by {type(other)}")
    
    def __eq__(self, other):
        if isinstance(other, Float):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        else:
            return False
    
    def __str__(self):
        return builtins.str(self.value)

class String:
    """
    字符串类型
    """
    
    def __init__(self, value):
        self.value = builtins.str(value)
    
    def __add__(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        elif isinstance(other, str):
            return String(self.value + other)
        else:
            raise TypeError(f"Cannot concatenate String with {type(other)}")
    
    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return False
    
    def __len__(self):
        return builtins.len(self.value)
    
    def __str__(self):
        return self.value

class Bool:
    """
    布尔类型
    """
    
    def __init__(self, value):
        self.value = builtins.bool(value)
    
    def __eq__(self, other):
        if isinstance(other, Bool):
            return self.value == other.value
        elif isinstance(other, bool):
            return self.value == other
        else:
            return False
    
    def __str__(self):
        return builtins.str(self.value)

class Char:
    """
    字符类型
    """
    
    def __init__(self, value):
        if isinstance(value, str) and builtins.len(value) == 1:
            self.value = value
        else:
            raise TypeError("Char must be a single character string")
    
    def __eq__(self, other):
        if isinstance(other, Char):
            return self.value == other.value
        elif isinstance(other, str) and builtins.len(other) == 1:
            return self.value == other
        else:
            return False
    
    def __str__(self):
        return self.value

class Unit:
    """
    单元类型
    """
    
    def __init__(self):
        pass
    
    def __eq__(self, other):
        return isinstance(other, Unit)
    
    def __str__(self):
        return "()"

# 类型别名
int = Int
float = Float
string = String
bool = Bool
char = Char
unit = Unit
