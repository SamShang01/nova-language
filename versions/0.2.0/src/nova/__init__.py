"""
Nova语言主模块
"""

from .version import __version__, get_version_string, version_greater_or_equal

# 导出
__all__ = [
    '__version__',
    'get_version_string',
    'version_greater_or_equal'
]