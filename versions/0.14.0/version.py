# Nova 语言版本信息

__version__ = (0, 14, 0)

VERSION_STRING = "0.14.0"

RELEASE_DATE = "2026-03-03"

VERSION_NAME = "Enhanced STL Release"

VERSION_DESCRIPTION = """
Nova 0.14.0 版本 - 增强的 STL 库

主要更新：
- 新增容器：Deque（双端队列）、Heap（堆/优先队列）、Trie（前缀树）
- 性能优化：快速排序、归并排序、堆排序等高级算法
- 新增算法：transform、accumulate、inner_product 等
- 完整的 STL 测试套件
"""

def get_version():
    """获取版本号元组"""
    return __version__

def get_version_string():
    """获取版本号字符串"""
    return VERSION_STRING

def get_release_date():
    """获取发布日期"""
    return RELEASE_DATE

if __name__ == "__main__":
    print(f"Nova {VERSION_STRING}")
    print(f"Release Date: {RELEASE_DATE}")
    print(f"Version Name: {VERSION_NAME}")
