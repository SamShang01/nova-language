"""
Nova语言版本信息
"""

__version__ = (0, 12, 0)
__version_str__ = "0.12.0"

def get_version_string():
    return __version_str__

__all__ = ['__version__', '__version_str__', 'get_version_string']
