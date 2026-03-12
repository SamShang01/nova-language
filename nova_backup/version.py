"""
Nova语言版本管理模块
"""

# 当前版本
__version__ = (0, 2, 0)
__version_str__ = "0.2.0"

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

# 版本比较
if __version__ >= (0, 1, 0):
    print(f"Nova语言版本: {get_version_string()}")

# 版本特性标识
if __version__ >= (0, 1, 0):
    # 0.1.0 版本特性
    FEATURES = {
        'lexer': True,
        'parser': False,
        'semantic_analyzer': False,
        'vm': False,
        'stdlib_core': True,
        'stdlib_collections': False,
        'stdlib_io': False,
        'stdlib_async': False
    }

if __version__ >= (0, 2, 0):
    # 0.2.0 版本特性（计划）
    FEATURES.update({
        'parser': True,
        'semantic_analyzer': True,
        'stdlib_collections': True,
        'stdlib_io': True,
        'stdlib_async': True
    })

if __version__ >= (1, 0, 0):
    # 1.0.0 版本特性（计划）
    FEATURES.update({
        'vm': True,
        'optimizations': True
    })

# 版本导入
if __version__ >= (0, 2, 0):
    # 0.2.0版本及以上支持语义分析器
    from src.nova.compiler.semantic import SemanticAnalyzer

if __version__ >= (0, 3, 0):
    # 0.3.0版本及以上支持虚拟机
    from src.nova.vm import VirtualMachine
