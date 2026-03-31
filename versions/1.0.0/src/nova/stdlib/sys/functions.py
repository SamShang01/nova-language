"""
Nova语言标准库系统操作函数模块
"""

import sys as builtin_sys
import os
from nova.stdlib.core.types import String, List, Dict

# 命令行参数
argv = builtin_sys.argv

# 退出函数
def exit(code=0):
    """
    退出程序
    
    Args:
        code: 退出码
    """
    builtin_sys.exit(code)

# 系统路径
path = builtin_sys.path

# 平台信息
platform = builtin_sys.platform

# 版本信息
version = builtin_sys.version

# 环境变量操作
def getenv(key, default=None):
    """
    获取环境变量
    
    Args:
        key: 环境变量名
        default: 默认值
    
    Returns:
        string: 环境变量值
    """
    value = os.getenv(str(key), default)
    if value is not None:
        return String(value)
    return default

def putenv(key, value):
    """
    设置环境变量
    
    Args:
        key: 环境变量名
        value: 环境变量值
    """
    os.putenv(str(key), str(value))

# 环境变量字典
environ = os.environ

# 标准输入输出
stdin = builtin_sys.stdin
stdout = builtin_sys.stdout
stderr = builtin_sys.stderr

# 内存大小获取
def getsizeof(obj):
    """
    获取对象大小
    
    Args:
        obj: 对象
    
    Returns:
        int: 对象大小（字节）
    """
    return builtin_sys.getsizeof(obj)

# 模块信息
modules = builtin_sys.modules

# 版权和许可证信息
copyright = builtin_sys.copyright
license = builtin_sys.license
