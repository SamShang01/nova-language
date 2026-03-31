"""
Nova语言标准库数学函数模块
"""

import math
import builtins
from nova.stdlib.core.types import Float

# 数学常量
PI = Float(builtins.float(math.pi))
E = Float(builtins.float(math.e))

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

# 额外的数学函数
def exp(x):
    """
    指数函数
    
    Args:
        x: 指数
    
    Returns:
        float: e的x次方
    """
    return Float(math.exp(builtins.float(x)))

def log(x, base=None):
    """
    对数函数
    
    Args:
        x: 数值
        base: 底数（可选，默认为e）
    
    Returns:
        float: 对数
    """
    if base is None:
        return Float(math.log(builtins.float(x)))
    else:
        return Float(math.log(builtins.float(x), builtins.float(base)))

def log10(x):
    """
    以10为底的对数
    
    Args:
        x: 数值
    
    Returns:
        float: 以10为底的对数
    """
    return Float(math.log10(builtins.float(x)))

def log2(x):
    """
    以2为底的对数
    
    Args:
        x: 数值
    
    Returns:
        float: 以2为底的对数
    """
    return Float(math.log2(builtins.float(x)))

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

def asin(x):
    """
    反正弦函数
    
    Args:
        x: 数值（-1到1之间）
    
    Returns:
        float: 反正弦值（弧度）
    """
    return Float(math.asin(builtins.float(x)))

def acos(x):
    """
    反余弦函数
    
    Args:
        x: 数值（-1到1之间）
    
    Returns:
        float: 反余弦值（弧度）
    """
    return Float(math.acos(builtins.float(x)))

def atan(x):
    """
    反正切函数
    
    Args:
        x: 数值
    
    Returns:
        float: 反正切值（弧度）
    """
    return Float(math.atan(builtins.float(x)))

def atan2(y, x):
    """
    反正切函数（带象限）
    
    Args:
        y: y坐标
        x: x坐标
    
    Returns:
        float: 反正切值（弧度）
    """
    return Float(math.atan2(builtins.float(y), builtins.float(x)))

def hypot(x, y):
    """
    计算直角三角形的斜边长度
    
    Args:
        x: 一条直角边
        y: 另一条直角边
    
    Returns:
        float: 斜边长度
    """
    return Float(math.hypot(builtins.float(x), builtins.float(y)))

def degrees(x):
    """
    弧度转角度
    
    Args:
        x: 弧度
    
    Returns:
        float: 角度
    """
    return Float(math.degrees(builtins.float(x)))

def radians(x):
    """
    角度转弧度
    
    Args:
        x: 角度
    
    Returns:
        float: 弧度
    """
    return Float(math.radians(builtins.float(x)))

def factorial(x):
    """
    阶乘函数
    
    Args:
        x: 非负整数
    
    Returns:
        float: 阶乘值
    """
    return Float(math.factorial(int(x)))

def gcd(a, b):
    """
    最大公约数
    
    Args:
        a: 整数
        b: 整数
    
    Returns:
        float: 最大公约数
    """
    return Float(math.gcd(int(a), int(b)))

def lcm(a, b):
    """
    最小公倍数
    
    Args:
        a: 整数
        b: 整数
    
    Returns:
        float: 最小公倍数
    """
    return Float(math.lcm(int(a), int(b)))

# 数学常量
PI = Float(builtins.float(math.pi))
E = Float(builtins.float(math.e))
TAU = Float(builtins.float(math.tau))
INF = Float(float('inf'))
NAN = Float(float('nan'))
