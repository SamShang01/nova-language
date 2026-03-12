"""
Nova语言标准库
"""

import builtins

from nova.version import __version__

# 保存内置的print函数
builtin_print = builtins.print

# 核心模块
from .core import *

# 集合模块
if __version__ >= (0, 2, 0):
    from .collections import *

# IO模块
if __version__ >= (0, 2, 0):
    from .io import *

# 异步模块
if __version__ >= (0, 3, 0):
    from .asynchronous import *

# 数学模块
if __version__ >= (0, 2, 0):
    from .math import *

# 字符串处理模块
if __version__ >= (0, 2, 0):
    from .string import *

# GUI模块
if __version__ >= (0, 4, 0):
    from .gui import *

__all__ = [
    # 核心库
    'print',
    'len',
    'type',
    'isinstance',
    'range',
    'enumerate',
]

# 集合模块
if __version__ >= (0, 2, 0):
    __all__.extend([
        'List',
        'Dict',
        'Set',
    ])

# IO模块
if __version__ >= (0, 2, 0):
    __all__.extend([
        'File',
        'stdin',
        'stdout',
        'stderr',
    ])

# 异步模块
if __version__ >= (0, 3, 0):
    __all__.extend([
        'async',
        'await',
        'Future',
    ])

# 数学模块
if __version__ >= (0, 2, 0):
    __all__.extend([
        'sin',
        'cos',
        'tan',
        'sqrt',
        'pow',
        'abs',
        'floor',
        'ceil',
        'round',
        'min',
        'max',
        'PI',
        'E'
    ])

# 字符串处理模块
if __version__ >= (0, 2, 0):
    __all__.extend([
        'to_upper',
        'to_lower',
        'trim',
        'split',
        'join',
        'contains',
        'starts_with',
        'ends_with',
        'replace',
        'substring'
    ])

# GUI模块
if __version__ >= (0, 4, 0):
    __all__.extend([
        'Widget',
        'Button',
        'Label',
        'Entry',
        'Text',
        'Canvas',
        'Menu'
    ])

# 版本特性标识
if __version__ >= (0, 1, 0):
    builtin_print(f"Nova语言标准库版本: {__version__}")

if __version__ >= (0, 2, 0):
    builtin_print("Nova语言标准库 0.2.0 特性:")
    builtin_print("1. 完善核心库功能")
    builtin_print("2. 添加更多集合类型")
    builtin_print("3. 增强IO库功能")
    builtin_print("4. 实现完整的异步库")

if __version__ >= (0, 3, 0):
    builtin_print("Nova语言标准库 0.3.0 特性:")
    builtin_print("1. 扩展标准库核心函数")
    builtin_print("2. 实现__future__.nova文件支持")
    builtin_print("3. 性能优化")

if __version__ >= (0, 4, 0):
    builtin_print("Nova语言标准库 0.4.0 特性:")
    builtin_print("1. 实现编译功能")
    builtin_print("2. 实现GUI功能")
    builtin_print("3. 扩展测试用例")
