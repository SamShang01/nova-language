"""
Nova语言标准库JSON处理函数模块
"""

import json as builtin_json
from nova.stdlib.core.types import String, Dict, List

# JSON序列化和反序列化函数
def dumps(obj, indent=None, sort_keys=False):
    """
    将对象转换为JSON字符串
    
    Args:
        obj: 要序列化的对象
        indent: 缩进空格数（可选）
        sort_keys: 是否按键排序（可选）
    
    Returns:
        string: JSON字符串
    """
    return String(builtin_json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False))

def loads(s):
    """
    将JSON字符串转换为对象
    
    Args:
        s: JSON字符串
    
    Returns:
        object: 解析后的对象
    """
    return builtin_json.loads(str(s))

def dump(obj, fp, indent=None, sort_keys=False):
    """
    将对象写入文件对象
    
    Args:
        obj: 要序列化的对象
        fp: 文件对象
        indent: 缩进空格数（可选）
        sort_keys: 是否按键排序（可选）
    """
    builtin_json.dump(obj, fp, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

def load(fp):
    """
    从文件对象读取JSON
    
    Args:
        fp: 文件对象
    
    Returns:
        object: 解析后的对象
    """
    return builtin_json.load(fp)
