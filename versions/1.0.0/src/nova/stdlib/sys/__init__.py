"""
Nova语言标准库系统操作模块
"""

from .functions import *

__all__ = [
    'argv', 'exit', 'path', 'platform', 'version',
    'getenv', 'putenv', 'environ', 'stderr', 'stdout',
    'stdin', 'getsizeof', 'modules', 'copyright', 'license'
]
