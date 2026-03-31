"""
Nova语言标准库网络编程模块
"""

from .socket import *
from .http import *

__all__ = [
    # socket模块
    'socket', 'AF_INET', 'SOCK_STREAM', 'SOCK_DGRAM',
    'SOL_SOCKET', 'SO_REUSEADDR', 'connect', 'bind',
    'listen', 'accept', 'send', 'recv', 'close',
    # http模块
    'get', 'post', 'put', 'delete', 'request'
]
