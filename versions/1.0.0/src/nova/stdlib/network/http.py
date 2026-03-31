"""
Nova语言标准库网络编程HTTP模块
"""

import urllib.request as builtin_request
import urllib.parse as builtin_parse
import urllib.error as builtin_error
from nova.stdlib.core.types import String, Dict

# HTTP请求函数
def request(url, data=None, headers=None, method='GET'):
    """
    发送HTTP请求
    
    Args:
        url: 请求URL
        data: 请求数据（可选）
        headers: 请求头（可选）
        method: 请求方法
    
    Returns:
        string: 响应内容
    """
    try:
        if data is not None:
            data = builtin_parse.urlencode(data).encode('utf-8')
        
        req = builtin_request.Request(url, data=data, headers=headers or {}, method=method)
        with builtin_request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            return String(content)
    except builtin_error.URLError as e:
        raise Exception(f"HTTP请求错误: {str(e)}")

def get(url, headers=None):
    """
    发送GET请求
    
    Args:
        url: 请求URL
        headers: 请求头（可选）
    
    Returns:
        string: 响应内容
    """
    return request(url, headers=headers, method='GET')

def post(url, data=None, headers=None):
    """
    发送POST请求
    
    Args:
        url: 请求URL
        data: 请求数据（可选）
        headers: 请求头（可选）
    
    Returns:
        string: 响应内容
    """
    return request(url, data=data, headers=headers, method='POST')

def put(url, data=None, headers=None):
    """
    发送PUT请求
    
    Args:
        url: 请求URL
        data: 请求数据（可选）
        headers: 请求头（可选）
    
    Returns:
        string: 响应内容
    """
    return request(url, data=data, headers=headers, method='PUT')

def delete(url, headers=None):
    """
    发送DELETE请求
    
    Args:
        url: 请求URL
        headers: 请求头（可选）
    
    Returns:
        string: 响应内容
    """
    return request(url, headers=headers, method='DELETE')
