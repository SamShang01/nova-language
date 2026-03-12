"""
Nova语言标准库核心函数模块
"""

import builtins
from .types import string as String, int as Int, unit

# 内置函数
def print(value):
    """
    打印值
    
    Args:
        value: 要打印的值
    
    Returns:
        unit: 单元值
    """
    builtins.print(builtins.str(value))
    return unit()

def len(value):
    """
    获取长度
    
    Args:
        value: 要获取长度的值
    
    Returns:
        int: 长度
    """
    return Int(builtins.len(builtins.str(value)))

def input(prompt=""):
    """
    获取用户输入
    
    Args:
        prompt: 提示信息
    
    Returns:
        string: 用户输入
    """
    user_input = builtins.input(builtins.str(prompt))
    return String(user_input)

def range(start, end=None, step=1):
    """
    生成范围
    
    Args:
        start: 开始值
        end: 结束值
        step: 步长
    
    Returns:
        list: 范围列表
    """
    if end is None:
        return list(builtins.range(start))
    else:
        return list(builtins.range(start, end, step))

def enumerate(iterable):
    """
    枚举可迭代对象
    
    Args:
        iterable: 可迭代对象
    
    Returns:
        list: 枚举列表
    """
    return list(builtins.enumerate(iterable))

def abs(value):
    """
    获取绝对值
    
    Args:
        value: 要获取绝对值的值
    
    Returns:
        int: 绝对值
    """
    return Int(builtins.abs(value))

def max(*args):
    """
    获取最大值
    
    Args:
        *args: 要比较的值
    
    Returns:
        int: 最大值
    """
    return Int(builtins.max(args))

def min(*args):
    """
    获取最小值
    
    Args:
        *args: 要比较的值
    
    Returns:
        int: 最小值
    """
    return Int(builtins.min(args))

def sum(iterable):
    """
    求和
    
    Args:
        iterable: 可迭代对象
    
    Returns:
        int: 和
    """
    return Int(builtins.sum(iterable))

def round(value, ndigits=0):
    """
    四舍五入
    
    Args:
        value: 要四舍五入的值
        ndigits: 小数位数
    
    Returns:
        float: 四舍五入后的值
    """
    return builtins.round(value, ndigits)

def type(value):
    """
    获取类型
    
    Args:
        value: 要获取类型的值
    
    Returns:
        string: 类型名称
    """
    return String(builtins.type(value).__name__)

def isinstance(value, type_name):
    """
    检查类型
    
    Args:
        value: 要检查的值
        type_name: 类型名称
    
    Returns:
        bool: 是否是指定类型
    """
    return builtins.isinstance(value, type_name)

def to_str(value):
    """
    字符串转换
    
    Args:
        value: 要转换的值
    
    Returns:
        string: 转换后的字符串
    """
    return String(builtins.str(value))

def to_int(value):
    """
    整数转换
    
    Args:
        value: 要转换的值
    
    Returns:
        int: 转换后的整数
    """
    return Int(builtins.int(value))

def to_float(value):
    """
    浮点数转换
    
    Args:
        value: 要转换的值
    
    Returns:
        float: 转换后的浮点数
    """
    return builtins.float(value)

def list(*args):
    """
    创建列表
    
    Args:
        *args: 列表元素
    
    Returns:
        list: 创建的列表
    """
    return builtins.list(args)

def dict(**kwargs):
    """
    创建字典
    
    Args:
        **kwargs: 字典键值对
    
    Returns:
        dict: 创建的字典
    """
    return builtins.dict(kwargs)

def contains(container, item):
    """
    检查容器是否包含元素
    
    Args:
        container: 容器
        item: 要检查的元素
    
    Returns:
        bool: 是否包含
    """
    return item in container

def keys(dictionary):
    """
    获取字典的键
    
    Args:
        dictionary: 字典
    
    Returns:
        list: 键列表
    """
    return builtins.list(dictionary.keys())

def values(dictionary):
    """
    获取字典的值
    
    Args:
        dictionary: 字典
    
    Returns:
        list: 值列表
    """
    return builtins.list(dictionary.values())

def items(dictionary):
    """
    获取字典的键值对
    
    Args:
        dictionary: 字典
    
    Returns:
        list: 键值对列表
    """
    return builtins.list(dictionary.items())

def append(lst, item):
    """
    向列表添加元素
    
    Args:
        lst: 列表
        item: 要添加的元素
    
    Returns:
        unit: 单元值
    """
    lst.append(item)
    return unit()

def remove(lst, item):
    """
    从列表移除元素
    
    Args:
        lst: 列表
        item: 要移除的元素
    
    Returns:
        unit: 单元值
    """
    lst.remove(item)
    return unit()

def pop(lst, index=-1):
    """
    从列表弹出元素
    
    Args:
        lst: 列表
        index: 索引，默认为最后一个
    
    Returns:
        Any: 弹出的元素
    """
    return lst.pop(index)

def sort(lst, reverse=False):
    """
    排序列表
    
    Args:
        lst: 列表
        reverse: 是否降序
    
    Returns:
        list: 排序后的列表
    """
    return builtins.sorted(lst, reverse=reverse)

def reverse(lst):
    """
    反转列表
    
    Args:
        lst: 列表
    
    Returns:
        list: 反转后的列表
    """
    return builtins.list(builtins.reversed(lst))

def slice(lst, start=None, end=None, step=None):
    """
    切片操作
    
    Args:
        lst: 列表
        start: 开始索引
        end: 结束索引
        step: 步长
    
    Returns:
        list: 切片后的列表
    """
    return lst[start:end:step]

def map_func(func, iterable):
    """
    映射函数
    
    Args:
        func: 函数
        iterable: 可迭代对象
    
    Returns:
        list: 映射后的列表
    """
    return builtins.list(builtins.map(func, iterable))

def filter_func(func, iterable):
    """
    过滤函数
    
    Args:
        func: 函数
        iterable: 可迭代对象
    
    Returns:
        list: 过滤后的列表
    """
    return builtins.list(builtins.filter(func, iterable))

def reduce_func(func, iterable, initial=None):
    """
    归约函数
    
    Args:
        func: 函数
        iterable: 可迭代对象
        initial: 初始值
    
    Returns:
        Any: 归约结果
    """
    from functools import reduce
    if initial is not None:
        return reduce(func, iterable, initial)
    return reduce(func, iterable)

def zip_func(*iterables):
    """
    压缩函数
    
    Args:
        *iterables: 可迭代对象
    
    Returns:
        list: 压缩后的列表
    """
    return builtins.list(builtins.zip(*iterables))

def any_func(iterable):
    """
    检查是否有任意元素为真
    
    Args:
        iterable: 可迭代对象
    
    Returns:
        bool: 是否有任意元素为真
    """
    return builtins.any(iterable)

def all_func(iterable):
    """
    检查是否所有元素都为真
    
    Args:
        iterable: 可迭代对象
    
    Returns:
        bool: 是否所有元素都为真
    """
    return builtins.all(iterable)

def chr_func(code):
    """
    将Unicode码点转换为字符
    
    Args:
        code: Unicode码点
    
    Returns:
        string: 字符
    """
    return String(builtins.chr(code))

def ord_func(char):
    """
    将字符转换为Unicode码点
    
    Args:
        char: 字符
    
    Returns:
        int: Unicode码点
    """
    return Int(builtins.ord(char))

def hex_func(value):
    """
    转换为十六进制字符串
    
    Args:
        value: 值
    
    Returns:
        string: 十六进制字符串
    """
    return String(builtins.hex(value))

def oct_func(value):
    """
    转换为八进制字符串
    
    Args:
        value: 值
    
    Returns:
        string: 八进制字符串
    """
    return String(builtins.oct(value))

def bin_func(value):
    """
    转换为二进制字符串
    
    Args:
        value: 值
    
    Returns:
        string: 二进制字符串
    """
    return String(builtins.bin(value))

def pow_func(base, exp, mod=None):
    """
    幂运算
    
    Args:
        base: 底数
        exp: 指数
        mod: 模数
    
    Returns:
        int: 幂运算结果
    """
    if mod is not None:
        return Int(builtins.pow(base, exp, mod))
    return Int(builtins.pow(base, exp))

def divmod_func(a, b):
    """
    除法和取模
    
    Args:
        a: 被除数
        b: 除数
    
    Returns:
        tuple: (商, 余数)
    """
    quotient, remainder = builtins.divmod(a, b)
    return (Int(quotient), Int(remainder))

def hash_func(value):
    """
    获取哈希值
    
    Args:
        value: 值
    
    Returns:
        int: 哈希值
    """
    return Int(builtins.hash(value))

def id_func(value):
    """
    获取对象ID
    
    Args:
        value: 值
    
    Returns:
        int: 对象ID
    """
    return Int(builtins.id(value))

def breakpoint():
    """
    设置断点，进入调试器
    
    类似于Python的breakpoint()函数，调用Nova调试器
    
    Returns:
        unit: 单元值
    """
    from nova.debugger import get_debugger
    
    debugger = get_debugger()
    
    # 获取当前帧信息
    import inspect
    frame = inspect.currentframe()
    
    frame_info = {
        'file': frame.f_code.co_filename,
        'line': frame.f_lineno,
        'function': frame.f_code.co_name,
        'locals': frame.f_locals,
        'globals': frame.f_globals
    }
    
    # 进入调试器
    debugger.set_trace(frame_info)
    
    return unit()
