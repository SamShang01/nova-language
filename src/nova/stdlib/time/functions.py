"""
Nova语言标准库时间日期处理函数模块
"""

import time as builtin_time
from nova.stdlib.core.types import Float, Int, String, List, Tuple

# 时间相关函数
def time():
    """
    获取当前时间戳（秒）
    
    Returns:
        float: 当前时间戳
    """
    return Float(builtin_time.time())

def sleep(seconds):
    """
    暂停执行指定秒数
    
    Args:
        seconds: 暂停时间（秒）
    """
    builtin_time.sleep(float(seconds))

def localtime(secs=None):
    """
    获取本地时间
    
    Args:
        secs: 时间戳（可选）
    
    Returns:
        tuple: 本地时间元组
    """
    if secs is None:
        return builtin_time.localtime()
    else:
        return builtin_time.localtime(float(secs))

def gmtime(secs=None):
    """
    获取格林威治时间
    
    Args:
        secs: 时间戳（可选）
    
    Returns:
        tuple: 格林威治时间元组
    """
    if secs is None:
        return builtin_time.gmtime()
    else:
        return builtin_time.gmtime(float(secs))

def strftime(format, t=None):
    """
    格式化时间
    
    Args:
        format: 格式字符串
        t: 时间元组（可选）
    
    Returns:
        string: 格式化后的时间字符串
    """
    if t is None:
        return String(builtin_time.strftime(str(format)))
    else:
        return String(builtin_time.strftime(str(format), t))

def strptime(string, format):
    """
    解析时间字符串
    
    Args:
        string: 时间字符串
        format: 格式字符串
    
    Returns:
        tuple: 时间元组
    """
    return builtin_time.strptime(str(string), str(format))

def mktime(t):
    """
    将时间元组转换为时间戳
    
    Args:
        t: 时间元组
    
    Returns:
        float: 时间戳
    """
    return Float(builtin_time.mktime(t))

def asctime(t=None):
    """
    将时间元组转换为字符串
    
    Args:
        t: 时间元组（可选）
    
    Returns:
        string: 时间字符串
    """
    if t is None:
        return String(builtin_time.asctime())
    else:
        return String(builtin_time.asctime(t))

def ctime(secs=None):
    """
    将时间戳转换为字符串
    
    Args:
        secs: 时间戳（可选）
    
    Returns:
        string: 时间字符串
    """
    if secs is None:
        return String(builtin_time.ctime())
    else:
        return String(builtin_time.ctime(float(secs)))

# 时区相关变量
timezone = builtin_time.timezone
altzone = builtin_time.altzone
daylight = builtin_time.daylight
tzname = builtin_time.tzname
