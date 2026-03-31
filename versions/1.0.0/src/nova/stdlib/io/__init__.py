"""
Nova语言标准库IO模块
"""

from .file import File, open, read, write, close
from .streams import stdin, stdout, stderr
from .file_utils import *

__all__ = [
    # 核心文件类
    'File',
    # 标准流
    'stdin',
    'stdout',
    'stderr',
    # 文件操作函数
    'open', 'read', 'write', 'close',
    # 文件工具函数
    'mkdir', 'rmdir', 'listdir', 'isdir', 'isfile', 'exists',
    'copy', 'copy2', 'move', 'remove', 'rename',
    'join', 'abspath', 'basename', 'dirname', 'split', 'splitext',
    'getsize', 'getmtime', 'getctime', 'getatime',
    'chmod', 'chown', 'stat'
]
