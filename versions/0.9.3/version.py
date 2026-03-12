"""
Nova语言版本信息
"""

# 当前版本
__version__ = (0, 9, 3)
__version_str__ = "0.9.3"

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
