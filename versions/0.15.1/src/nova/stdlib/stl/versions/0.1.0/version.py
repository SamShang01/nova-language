# Nova STL 库版本信息

__version__ = (0, 1, 0)

VERSION_STRING = "0.1.0"

RELEASE_DATE = "2026-03-03"

VERSION_NAME = "Initial STL Release"

VERSION_DESCRIPTION = """
Nova STL 库 0.1.0 版本 - 初始版本

主要特性：
- 完整的 STL 容器系统：Vector, List, Stack, Queue, Set, Map, Deque, Heap, Trie
- 迭代器系统：Iterator, RandomAccessIterator, BidirectionalIterator
- 函数对象和比较器：Less, Greater, EqualTo, Plus, Minus 等
- 算法库：sort, reverse, find, binarySearch, count, transform, accumulate 等
- 数值算法：gcd, lcm, power, factorial, fibonacci 等
- Option 类型：处理可选值
- 类型特征：类型检查和类型推断支持
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
    print(f"Nova STL {VERSION_STRING}")
    print(f"Release Date: {RELEASE_DATE}")
    print(f"Version Name: {VERSION_NAME}")
