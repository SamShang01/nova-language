"""
Nova语言标准库IO模块
"""

from .file import File
from .streams import stdin, stdout, stderr

__all__ = [
    'File',
    'stdin',
    'stdout',
    'stderr'
]
