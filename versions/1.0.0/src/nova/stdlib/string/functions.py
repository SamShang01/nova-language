"""
Nova语言标准库字符串处理函数模块
"""

from nova.stdlib.core.types import String

def to_upper(s):
    """
    转换为大写
    
    Args:
        s: 字符串
    
    Returns:
        string: 大写字符串
    """
    return String(str(s).upper())

def to_lower(s):
    """
    转换为小写
    
    Args:
        s: 字符串
    
    Returns:
        string: 小写字符串
    """
    return String(str(s).lower())

def trim(s):
    """
    去除首尾空白
    
    Args:
        s: 字符串
    
    Returns:
        string: 去除空白后的字符串
    """
    return String(str(s).strip())

def split(s, delimiter):
    """
    分割字符串
    
    Args:
        s: 字符串
        delimiter: 分隔符
    
    Returns:
        list: 分割后的字符串列表
    """
    return str(s).split(str(delimiter))

def join(strings, delimiter):
    """
    连接字符串
    
    Args:
        strings: 字符串列表
        delimiter: 分隔符
    
    Returns:
        string: 连接后的字符串
    """
    return String(str(delimiter).join(map(str, strings)))

def contains(s, substr):
    """
    检查是否包含子串
    
    Args:
        s: 字符串
        substr: 子串
    
    Returns:
        bool: 是否包含
    """
    return substr in str(s)

def starts_with(s, prefix):
    """
    检查是否以指定前缀开头
    
    Args:
        s: 字符串
        prefix: 前缀
    
    Returns:
        bool: 是否以指定前缀开头
    """
    return str(s).startswith(str(prefix))

def ends_with(s, suffix):
    """
    检查是否以指定后缀结尾
    
    Args:
        s: 字符串
        suffix: 后缀
    
    Returns:
        bool: 是否以指定后缀结尾
    """
    return str(s).endswith(str(suffix))

def replace(s, old, new):
    """
    替换字符串
    
    Args:
        s: 字符串
        old: 要替换的子串
        new: 新子串
    
    Returns:
        string: 替换后的字符串
    """
    return String(str(s).replace(str(old), str(new)))

def substring(s, start, end=None):
    """
    获取子串
    
    Args:
        s: 字符串
        start: 起始位置
        end: 结束位置（可选）
    
    Returns:
        string: 子串
    """
    if end is None:
        return String(str(s)[start:])
    else:
        return String(str(s)[start:end])

def reverse(s):
    """
    反转字符串
    
    Args:
        s: 字符串
    
    Returns:
        string: 反转后的字符串
    """
    return String(str(s)[::-1])

def capitalize(s):
    """
    首字母大写
    
    Args:
        s: 字符串
    
    Returns:
        string: 首字母大写后的字符串
    """
    return String(str(s).capitalize())

def title(s):
    """
    标题化字符串
    
    Args:
        s: 字符串
    
    Returns:
        string: 标题化后的字符串
    """
    return String(str(s).title())

def swapcase(s):
    """
    大小写互换
    
    Args:
        s: 字符串
    
    Returns:
        string: 大小写互换后的字符串
    """
    return String(str(s).swapcase())

def ljust(s, width, fillchar=' '):
    """
    左对齐
    
    Args:
        s: 字符串
        width: 宽度
        fillchar: 填充字符
    
    Returns:
        string: 左对齐后的字符串
    """
    return String(str(s).ljust(width, fillchar))

def rjust(s, width, fillchar=' '):
    """
    右对齐
    
    Args:
        s: 字符串
        width: 宽度
        fillchar: 填充字符
    
    Returns:
        string: 右对齐后的字符串
    """
    return String(str(s).rjust(width, fillchar))

def center(s, width, fillchar=' '):
    """
    居中对齐
    
    Args:
        s: 字符串
        width: 宽度
        fillchar: 填充字符
    
    Returns:
        string: 居中对齐后的字符串
    """
    return String(str(s).center(width, fillchar))

def lstrip(s, chars=None):
    """
    去除左侧空白
    
    Args:
        s: 字符串
        chars: 要去除的字符
    
    Returns:
        string: 去除左侧空白后的字符串
    """
    return String(str(s).lstrip(chars))

def rstrip(s, chars=None):
    """
    去除右侧空白
    
    Args:
        s: 字符串
        chars: 要去除的字符
    
    Returns:
        string: 去除右侧空白后的字符串
    """
    return String(str(s).rstrip(chars))

def strip(s, chars=None):
    """
    去除首尾空白
    
    Args:
        s: 字符串
        chars: 要去除的字符
    
    Returns:
        string: 去除首尾空白后的字符串
    """
    return String(str(s).strip(chars))

def split(s, sep=None, maxsplit=-1):
    """
    分割字符串
    
    Args:
        s: 字符串
        sep: 分隔符
        maxsplit: 最大分割次数
    
    Returns:
        list: 分割后的字符串列表
    """
    return str(s).split(sep, maxsplit)

def rsplit(s, sep=None, maxsplit=-1):
    """
    从右侧分割字符串
    
    Args:
        s: 字符串
        sep: 分隔符
        maxsplit: 最大分割次数
    
    Returns:
        list: 分割后的字符串列表
    """
    return str(s).rsplit(sep, maxsplit)

def splitlines(s, keepends=False):
    """
    按行分割字符串
    
    Args:
        s: 字符串
        keepends: 是否保留换行符
    
    Returns:
        list: 按行分割后的字符串列表
    """
    return str(s).splitlines(keepends)

def join(strings, sep=''):
    """
    连接字符串
    
    Args:
        strings: 字符串列表
        sep: 分隔符
    
    Returns:
        string: 连接后的字符串
    """
    return String(str(sep).join(map(str, strings)))

def replace(s, old, new, count=-1):
    """
    替换字符串
    
    Args:
        s: 字符串
        old: 要替换的子串
        new: 新子串
        count: 替换次数
    
    Returns:
        string: 替换后的字符串
    """
    return String(str(s).replace(str(old), str(new), count))

def find(s, sub, start=0, end=None):
    """
    查找子串位置
    
    Args:
        s: 字符串
        sub: 子串
        start: 开始位置
        end: 结束位置
    
    Returns:
        int: 子串位置，未找到返回-1
    """
    return str(s).find(str(sub), start, end)

def rfind(s, sub, start=0, end=None):
    """
    从右侧查找子串位置
    
    Args:
        s: 字符串
        sub: 子串
        start: 开始位置
        end: 结束位置
    
    Returns:
        int: 子串位置，未找到返回-1
    """
    return str(s).rfind(str(sub), start, end)

def index(s, sub, start=0, end=None):
    """
    查找子串位置（未找到抛出异常）
    
    Args:
        s: 字符串
        sub: 子串
        start: 开始位置
        end: 结束位置
    
    Returns:
        int: 子串位置
    """
    return str(s).index(str(sub), start, end)

def rindex(s, sub, start=0, end=None):
    """
    从右侧查找子串位置（未找到抛出异常）
    
    Args:
        s: 字符串
        sub: 子串
        start: 开始位置
        end: 结束位置
    
    Returns:
        int: 子串位置
    """
    return str(s).rindex(str(sub), start, end)

def count(s, sub, start=0, end=None):
    """
    计算子串出现次数
    
    Args:
        s: 字符串
        sub: 子串
        start: 开始位置
        end: 结束位置
    
    Returns:
        int: 子串出现次数
    """
    return str(s).count(str(sub), start, end)

def startswith(s, prefix, start=0, end=None):
    """
    检查是否以指定前缀开头
    
    Args:
        s: 字符串
        prefix: 前缀
        start: 开始位置
        end: 结束位置
    
    Returns:
        bool: 是否以指定前缀开头
    """
    return str(s).startswith(str(prefix), start, end)

def endswith(s, suffix, start=0, end=None):
    """
    检查是否以指定后缀结尾
    
    Args:
        s: 字符串
        suffix: 后缀
        start: 开始位置
        end: 结束位置
    
    Returns:
        bool: 是否以指定后缀结尾
    """
    return str(s).endswith(str(suffix), start, end)

def isalpha(s):
    """
    检查是否全为字母
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为字母
    """
    return str(s).isalpha()

def isdigit(s):
    """
    检查是否全为数字
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为数字
    """
    return str(s).isdigit()

def isalnum(s):
    """
    检查是否全为字母或数字
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为字母或数字
    """
    return str(s).isalnum()

def isspace(s):
    """
    检查是否全为空白字符
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为空白字符
    """
    return str(s).isspace()

def islower(s):
    """
    检查是否全为小写
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为小写
    """
    return str(s).islower()

def isupper(s):
    """
    检查是否全为大写
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为大写
    """
    return str(s).isupper()

def istitle(s):
    """
    检查是否为标题格式
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否为标题格式
    """
    return str(s).istitle()

def isdecimal(s):
    """
    检查是否全为十进制数字
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为十进制数字
    """
    return str(s).isdecimal()

def isnumeric(s):
    """
    检查是否全为数字字符
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否全为数字字符
    """
    return str(s).isnumeric()

def isidentifier(s):
    """
    检查是否为有效的标识符
    
    Args:
        s: 字符串
    
    Returns:
        bool: 是否为有效的标识符
    """
    return str(s).isidentifier()

def zfill(s, width):
    """
    用0填充字符串
    
    Args:
        s: 字符串
        width: 宽度
    
    Returns:
        string: 用0填充后的字符串
    """
    return String(str(s).zfill(width))

def expandtabs(s, tabsize=8):
    """
    展开制表符
    
    Args:
        s: 字符串
        tabsize: 制表符大小
    
    Returns:
        string: 展开制表符后的字符串
    """
    return String(str(s).expandtabs(tabsize))

def maketrans(s, t, deletechars=''):
    """
    创建字符映射表
    
    Args:
        s: 源字符
        t: 目标字符
        deletechars: 要删除的字符
    
    Returns:
        dict: 字符映射表
    """
    return str(s).maketrans(t, deletechars)

def translate(s, table):
    """
    翻译字符串
    
    Args:
        s: 字符串
        table: 字符映射表
    
    Returns:
        string: 翻译后的字符串
    """
    return String(str(s).translate(table))

def format(s, *args, **kwargs):
    """
    格式化字符串
    
    Args:
        s: 字符串
        *args: 位置参数
        **kwargs: 关键字参数
    
    Returns:
        string: 格式化后的字符串
    """
    return String(str(s).format(*args, **kwargs))

def partition(s, sep):
    """
    分割字符串为三部分
    
    Args:
        s: 字符串
        sep: 分隔符
    
    Returns:
        tuple: (前, 分隔符, 后)
    """
    return str(s).partition(str(sep))

def rpartition(s, sep):
    """
    从右侧分割字符串为三部分
    
    Args:
        s: 字符串
        sep: 分隔符
    
    Returns:
        tuple: (前, 分隔符, 后)
    """
    return str(s).rpartition(str(sep))
