"""
Nova语言标准库网络编程socket模块
"""

import socket as builtin_socket
from nova.stdlib.core.types import String, Int, List, Tuple

# 常量
AF_INET = builtin_socket.AF_INET
SOCK_STREAM = builtin_socket.SOCK_STREAM
SOCK_DGRAM = builtin_socket.SOCK_DGRAM
SOL_SOCKET = builtin_socket.SOL_SOCKET
SO_REUSEADDR = builtin_socket.SO_REUSEADDR

# 函数
def socket(family=AF_INET, type=SOCK_STREAM, proto=0):
    """
    创建socket对象
    
    Args:
        family: 地址族
        type: socket类型
        proto: 协议
    
    Returns:
        socket: socket对象
    """
    return builtin_socket.socket(family, type, proto)

def connect(sock, address):
    """
    连接到远程地址
    
    Args:
        sock: socket对象
        address: (host, port)元组
    """
    sock.connect(address)

def bind(sock, address):
    """
    绑定到本地地址
    
    Args:
        sock: socket对象
        address: (host, port)元组
    """
    sock.bind(address)

def listen(sock, backlog=5):
    """
    开始监听连接
    
    Args:
        sock: socket对象
        backlog: 最大连接数
    """
    sock.listen(backlog)

def accept(sock):
    """
    接受连接
    
    Args:
        sock: socket对象
    
    Returns:
        tuple: (conn, address)
    """
    return sock.accept()

def send(sock, data):
    """
    发送数据
    
    Args:
        sock: socket对象
        data: 数据
    
    Returns:
        int: 发送的字节数
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return sock.send(data)

def recv(sock, bufsize, flags=0):
    """
    接收数据
    
    Args:
        sock: socket对象
        bufsize: 缓冲区大小
        flags: 标志
    
    Returns:
        string: 接收到的数据
    """
    data = sock.recv(bufsize, flags)
    return String(data.decode('utf-8'))

def close(sock):
    """
    关闭socket
    
    Args:
        sock: socket对象
    """
    sock.close()
