#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 REPL 修复
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.repl import NovaREPL

# 创建 REPL 实例
repl = NovaREPL()

# 测试命令序列
test_commands = [
    "let a;",  # 无类型无初始值，应该报错
    "let a:int;",  # 有类型无初始值，应该成功
    "a;",  # 访问变量，应该输出 None
    "type(a);",  # 调用 type 函数，应该输出 int
    ":type a",  # 查看变量类型，应该显示 a: int = None
    "a = 12;",  # 赋值
    "a;",  # 访问变量，应该输出 12
    ":type a",  # 查看变量类型，应该显示 a: int = 12
]

# 模拟执行命令
for command in test_commands:
    print(f"nova> {command}")
    if command.startswith(':'):
        # 处理特殊命令
        repl._handle_special_command(command)
    else:
        # 执行 Nova 代码
        repl._execute_code(command)
    print()