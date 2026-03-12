"""
Nova编程语言命令行入口
"""

import sys
import os

# 添加根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from script import cli_main

if __name__ == '__main__':
    cli_main()
