"""
Nova语言标准库文件工具模块
"""

import os
import shutil
from nova.stdlib.core.types import String, List

# 目录操作
def mkdir(path, exist_ok=False):
    """
    创建目录
    
    Args:
        path: 目录路径
        exist_ok: 如果目录已存在是否报错
    """
    os.makedirs(str(path), exist_ok=exist_ok)

def rmdir(path):
    """
    删除目录
    
    Args:
        path: 目录路径
    """
    os.rmdir(str(path))

def listdir(path):
    """
    列出目录内容
    
    Args:
        path: 目录路径
    
    Returns:
        list: 目录内容列表
    """
    return os.listdir(str(path))

def isdir(path):
    """
    检查是否为目录
    
    Args:
        path: 路径
    
    Returns:
        bool: 是否为目录
    """
    return os.path.isdir(str(path))

def isfile(path):
    """
    检查是否为文件
    
    Args:
        path: 路径
    
    Returns:
        bool: 是否为文件
    """
    return os.path.isfile(str(path))

def exists(path):
    """
    检查路径是否存在
    
    Args:
        path: 路径
    
    Returns:
        bool: 路径是否存在
    """
    return os.path.exists(str(path))

# 文件操作
def copy(src, dst):
    """
    复制文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    shutil.copy(str(src), str(dst))

def copy2(src, dst):
    """
    复制文件（保留元数据）
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    shutil.copy2(str(src), str(dst))

def move(src, dst):
    """
    移动文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    shutil.move(str(src), str(dst))

def remove(path):
    """
    删除文件
    
    Args:
        path: 文件路径
    """
    os.remove(str(path))

def rename(src, dst):
    """
    重命名文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    """
    os.rename(str(src), str(dst))

# 路径操作
def join(*paths):
    """
    拼接路径
    
    Args:
        *paths: 路径部分
    
    Returns:
        string: 拼接后的路径
    """
    return String(os.path.join(*map(str, paths)))

def abspath(path):
    """
    获取绝对路径
    
    Args:
        path: 路径
    
    Returns:
        string: 绝对路径
    """
    return String(os.path.abspath(str(path)))

def basename(path):
    """
    获取文件名
    
    Args:
        path: 路径
    
    Returns:
        string: 文件名
    """
    return String(os.path.basename(str(path)))

def dirname(path):
    """
    获取目录名
    
    Args:
        path: 路径
    
    Returns:
        string: 目录名
    """
    return String(os.path.dirname(str(path)))

def split(path):
    """
    分割路径
    
    Args:
        path: 路径
    
    Returns:
        tuple: (目录, 文件名)
    """
    result = os.path.split(str(path))
    return (String(result[0]), String(result[1]))

def splitext(path):
    """
    分割扩展名
    
    Args:
        path: 路径
    
    Returns:
        tuple: (文件名, 扩展名)
    """
    result = os.path.splitext(str(path))
    return (String(result[0]), String(result[1]))

# 文件信息
def getsize(path):
    """
    获取文件大小
    
    Args:
        path: 文件路径
    
    Returns:
        int: 文件大小（字节）
    """
    return os.path.getsize(str(path))

def getmtime(path):
    """
    获取文件修改时间
    
    Args:
        path: 文件路径
    
    Returns:
        float: 修改时间戳
    """
    return os.path.getmtime(str(path))

def getctime(path):
    """
    获取文件创建时间
    
    Args:
        path: 文件路径
    
    Returns:
        float: 创建时间戳
    """
    return os.path.getctime(str(path))

def getatime(path):
    """
    获取文件访问时间
    
    Args:
        path: 文件路径
    
    Returns:
        float: 访问时间戳
    """
    return os.path.getatime(str(path))

# 其他函数
def chmod(path, mode):
    """
    修改文件权限
    
    Args:
        path: 文件路径
        mode: 权限模式
    """
    os.chmod(str(path), mode)

def chown(path, uid, gid):
    """
    修改文件所有者
    
    Args:
        path: 文件路径
        uid: 用户ID
        gid: 组ID
    """
    os.chown(str(path), uid, gid)

def stat(path):
    """
    获取文件状态
    
    Args:
        path: 文件路径
    
    Returns:
        stat_result: 文件状态
    """
    return os.stat(str(path))
