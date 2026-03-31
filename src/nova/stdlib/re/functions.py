"""
Nova语言标准库正则表达式函数模块
"""

import re as builtin_re
from nova.stdlib.core.types import String, List, Tuple

# 正则表达式函数
def compile(pattern, flags=0):
    """
    编译正则表达式模式
    
    Args:
        pattern: 正则表达式模式
        flags: 标志
    
    Returns:
        regex: 编译后的正则表达式对象
    """
    return builtin_re.compile(str(pattern), flags)

def match(pattern, string, flags=0):
    """
    从字符串开头匹配
    
    Args:
        pattern: 正则表达式模式
        string: 要匹配的字符串
        flags: 标志
    
    Returns:
        match: 匹配对象或None
    """
    return builtin_re.match(str(pattern), str(string), flags)

def search(pattern, string, flags=0):
    """
    在字符串中搜索匹配
    
    Args:
        pattern: 正则表达式模式
        string: 要搜索的字符串
        flags: 标志
    
    Returns:
        match: 匹配对象或None
    """
    return builtin_re.search(str(pattern), str(string), flags)

def findall(pattern, string, flags=0):
    """
    查找所有匹配项
    
    Args:
        pattern: 正则表达式模式
        string: 要搜索的字符串
        flags: 标志
    
    Returns:
        list: 匹配项列表
    """
    return builtin_re.findall(str(pattern), str(string), flags)

def finditer(pattern, string, flags=0):
    """
    查找所有匹配项并返回迭代器
    
    Args:
        pattern: 正则表达式模式
        string: 要搜索的字符串
        flags: 标志
    
    Returns:
        iterator: 匹配对象迭代器
    """
    return builtin_re.finditer(str(pattern), str(string), flags)

def sub(pattern, repl, string, count=0, flags=0):
    """
    替换匹配项
    
    Args:
        pattern: 正则表达式模式
        repl: 替换字符串
        string: 要处理的字符串
        count: 替换次数
        flags: 标志
    
    Returns:
        string: 替换后的字符串
    """
    return String(builtin_re.sub(str(pattern), str(repl), str(string), count, flags))

def subn(pattern, repl, string, count=0, flags=0):
    """
    替换匹配项并返回替换次数
    
    Args:
        pattern: 正则表达式模式
        repl: 替换字符串
        string: 要处理的字符串
        count: 替换次数
        flags: 标志
    
    Returns:
        tuple: (替换后的字符串, 替换次数)
    """
    result = builtin_re.subn(str(pattern), str(repl), str(string), count, flags)
    return (String(result[0]), result[1])

def split(pattern, string, maxsplit=0, flags=0):
    """
    按匹配项分割字符串
    
    Args:
        pattern: 正则表达式模式
        string: 要分割的字符串
        maxsplit: 最大分割次数
        flags: 标志
    
    Returns:
        list: 分割后的字符串列表
    """
    return builtin_re.split(str(pattern), str(string), maxsplit, flags)

def escape(pattern):
    """
    转义正则表达式特殊字符
    
    Args:
        pattern: 字符串
    
    Returns:
        string: 转义后的字符串
    """
    return String(builtin_re.escape(str(pattern)))

def purge():
    """
    清除正则表达式缓存
    """
    builtin_re.purge()

# 标志常量
IGNORECASE = builtin_re.IGNORECASE
MULTILINE = builtin_re.MULTILINE
DOTALL = builtin_re.DOTALL
VERBOSE = builtin_re.VERBOSE
LOCALE = builtin_re.LOCALE
UNICODE = builtin_re.UNICODE
ASCII = builtin_re.ASCII
