"""
Nova语言标准库加密哈希函数模块
"""

import hashlib
import base64
from nova.stdlib.core.types import String, bytes

# 哈希函数
def md5(data):
    """
    MD5哈希
    
    Args:
        data: 要哈希的数据
    
    Returns:
        object: MD5哈希对象
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.md5(data)

def sha1(data):
    """
    SHA1哈希
    
    Args:
        data: 要哈希的数据
    
    Returns:
        object: SHA1哈希对象
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha1(data)

def sha224(data):
    """
    SHA224哈希
    
    Args:
        data: 要哈希的数据
    
    Returns:
        object: SHA224哈希对象
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha224(data)

def sha256(data):
    """
    SHA256哈希
    
    Args:
        data: 要哈希的数据
    
    Returns:
        object: SHA256哈希对象
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data)

def sha384(data):
    """
    SHA384哈希
    
    Args:
        data: 要哈希的数据
    
    Returns:
        object: SHA384哈希对象
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha384(data)

def sha512(data):
    """
    SHA512哈希
    
    Args:
        data: 要哈希的数据
    
    Returns:
        object: SHA512哈希对象
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha512(data)

# 哈希结果处理
def hexdigest(hash_obj):
    """
    获取十六进制哈希值
    
    Args:
        hash_obj: 哈希对象
    
    Returns:
        string: 十六进制哈希值
    """
    return String(hash_obj.hexdigest())

def digest(hash_obj):
    """
    获取原始哈希值
    
    Args:
        hash_obj: 哈希对象
    
    Returns:
        bytes: 原始哈希值
    """
    return hash_obj.digest()

# Base64编码解码
def base64_encode(data):
    """
    Base64编码
    
    Args:
        data: 要编码的数据
    
    Returns:
        string: Base64编码后的字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return String(base64.b64encode(data).decode('utf-8'))

def base64_decode(data):
    """
    Base64解码
    
    Args:
        data: 要解码的Base64字符串
    
    Returns:
        string: 解码后的字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return String(base64.b64decode(data).decode('utf-8'))
