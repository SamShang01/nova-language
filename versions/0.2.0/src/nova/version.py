"""
Nova语言版本信息
"""

# 版本号
def get_version():
    """
    获取当前版本
    
    Returns:
        tuple: 版本元组 (major, minor, patch)
    """
    return (0, 2, 0)

__version__ = get_version()

# 版本比较
def version_greater_or_equal(version):
    """
    检查当前版本是否大于等于指定版本
    
    Args:
        version: 指定版本，格式为 (major, minor, patch)
    
    Returns:
        bool: 当前版本是否大于等于指定版本
    """
    current = __version__
    return current >= version

# 版本字符串
def get_version_string():
    """
    获取版本字符串
    
    Returns:
        str: 版本字符串，格式为 "x.y.z"
    """
    return '.'.join(map(str, __version__))

# 导出
__all__ = [
    '__version__',
    'get_version',
    'get_version_string',
    'version_greater_or_equal'
]