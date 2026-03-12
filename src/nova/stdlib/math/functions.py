"""
Nova语言标准库数学函数模块
"""

import math
import builtins
from nova.stdlib.core.types import Float

# 数学常量
PI = Float(builtins.float(math.pi))
E = Float(builtins.float(math.e))

# 三角函数
def sin(x):
    """
    正弦函数
    
    Args:
        x: 角度（弧度）
    
    Returns:
        float: 正弦值
    """
    return Float(math.sin(builtins.float(x)))

def cos(x):
    """
    余弦函数
    
    Args:
        x: 角度（弧度）
    
    Returns:
        float: 余弦值
    """
    return Float(math.cos(builtins.float(x)))

def tan(x):
    """
    正切函数
    
    Args:
        x: 角度（弧度）
    
    Returns:
        float: 正切值
    """
    return Float(math.tan(builtins.float(x)))

# 数学运算函数
def sqrt(x):
    """
    平方根函数
    
    Args:
        x: 非负数
    
    Returns:
        float: 平方根
    """
    return Float(math.sqrt(builtins.float(x)))

def pow(x, y):
    """
    幂函数
    
    Args:
        x: 底数
        y: 指数
    
    Returns:
        float: x的y次方
    """
    return Float(math.pow(builtins.float(x), builtins.float(y)))

def abs(x):
    """
    绝对值函数
    
    Args:
        x: 数值
    
    Returns:
        float: 绝对值
    """
    return Float(builtins.abs(builtins.float(x)))

def floor(x):
    """
    向下取整函数
    
    Args:
        x: 数值
    
    Returns:
        float: 不大于x的最大整数
    """
    return Float(math.floor(builtins.float(x)))

def ceil(x):
    """
    向上取整函数
    
    Args:
        x: 数值
    
    Returns:
        float: 不小于x的最小整数
    """
    return Float(math.ceil(builtins.float(x)))

def round(x):
    """
    四舍五入函数
    
    Args:
        x: 数值
    
    Returns:
        float: 四舍五入后的整数
    """
    return Float(builtins.round(builtins.float(x)))

def min(x, y):
    """
    最小值函数
    
    Args:
        x: 数值
        y: 数值
    
    Returns:
        float: 较小的值
    """
    return Float(builtins.min(builtins.float(x), builtins.float(y)))

def max(x, y):
    """
    最大值函数
    
    Args:
        x: 数值
        y: 数值
    
    Returns:
        float: 较大的值
    """
    return Float(builtins.max(builtins.float(x), builtins.float(y)))
