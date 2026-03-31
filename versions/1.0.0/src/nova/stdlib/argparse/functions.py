"""
Nova语言标准库命令行参数解析函数模块
"""

import argparse as builtin_argparse
from nova.stdlib.core.types import String

# 命令行参数解析器
def ArgumentParser(description=None, prog=None, usage=None):
    """
    创建命令行参数解析器
    
    Args:
        description: 程序描述
        prog: 程序名称
        usage: 使用说明
    
    Returns:
        ArgumentParser: 参数解析器对象
    """
    return builtin_argparse.ArgumentParser(
        description=description,
        prog=prog,
        usage=usage
    )

def parse_args(parser, args=None):
    """
    解析命令行参数
    
    Args:
        parser: 参数解析器对象
        args: 要解析的参数列表（可选）
    
    Returns:
        Namespace: 解析后的参数命名空间
    """
    return parser.parse_args(args)
