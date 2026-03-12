"""
Nova语言标准库字符串处理函数模块
"""

from nova.stdlib.core.types import String

def to_upper(s):
    """
    转换为大写
    
    Args:
        s: 字符串
    
    Returns:
        string: 大写字符串
    """
    return String(str(s).upper())

def to_lower(s):
    """
    转换为小写
    
    Args:
        s: 字符串
    
    Returns:
        string: 小写字符串
    """
    return String(str(s).lower())

def trim(s):
    """
    去除首尾空白
    
    Args:
        s: 字符串
    
    Returns:
        string: 去除空白后的字符串
    """
    return String(str(s).strip())

def split(s, delimiter):
    """
    分割字符串
    
    Args:
        s: 字符串
        delimiter: 分隔符
    
    Returns:
        list: 分割后的字符串列表
    """
    return str(s).split(str(delimiter))

def join(strings, delimiter):
    """
    连接字符串
    
    Args:
        strings: 字符串列表
        delimiter: 分隔符
    
    Returns:
        string: 连接后的字符串
    """
    return String(str(delimiter).join(map(str, strings)))

def contains(s, substr):
    """
    检查是否包含子串
    
    Args:
        s: 字符串
        substr: 子串
    
    Returns:
        bool: 是否包含
    """
    return substr in str(s)

def starts_with(s, prefix):
    """
    检查是否以指定前缀开头
    
    Args:
        s: 字符串
        prefix: 前缀
    
    Returns:
        bool: 是否以指定前缀开头
    """
    return str(s).startswith(str(prefix))

def ends_with(s, suffix):
    """
    检查是否以指定后缀结尾
    
    Args:
        s: 字符串
        suffix: 后缀
    
    Returns:
        bool: 是否以指定后缀结尾
    """
    return str(s).endswith(str(suffix))

def replace(s, old, new):
    """
    替换字符串
    
    Args:
        s: 字符串
        old: 要替换的子串
        new: 新子串
    
    Returns:
        string: 替换后的字符串
    """
    return String(str(s).replace(str(old), str(new)))

def substring(s, start, end=None):
    """
    获取子串
    
    Args:
        s: 字符串
        start: 起始位置
        end: 结束位置（可选）
    
    Returns:
        string: 子串
    """
    if end is None:
        return String(str(s)[start:])
    else:
        return String(str(s)[start:end])

def reverse(s):
    """
    反转字符串
    
    Args:
        s: 字符串
    
    Returns:
        string: 反转后的字符串
    """
    return String(str(s)[::-1])
