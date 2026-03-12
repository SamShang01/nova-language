"""
Nova语言版本信息（0.11.0版本）
"""

# 当前版本
__version__ = (0, 11, 0)
__version_str__ = "0.11.0"

# 版本判断函数
def version_greater_or_equal(major, minor, patch):
    """
    判断当前版本是否大于等于指定版本

    Args:
        major: 主版本号
        minor: 次版本号
        patch: 修订号

    Returns:
        bool: 当前版本是否大于等于指定版本
    """
    current = __version__
    if current[0] > major:
        return True
    elif current[0] == major:
        if current[1] > minor:
            return True
        elif current[1] == minor:
            return current[2] >= patch
    return False

# 版本字符串
def get_version_string():
    """
    获取版本字符串

    Returns:
        str: 版本字符串，格式为 x.y.z
    """
    return '.'.join(map(str, __version__))

__all__ = [
    '__version__',
    '__version_str__',
    'get_version_string',
    'version_greater_or_equal'
]
