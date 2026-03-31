#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试版本读取脚本
"""

import os

# 读取版本信息
version_file = os.path.join(os.path.dirname(__file__), 'src', 'nova', 'version.py')
if os.path.exists(version_file):
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(f.read())
    print(f'版本元组: {__version__}')
    print(f'版本字符串: {__version_str__}')
else:
    print('版本文件不存在')