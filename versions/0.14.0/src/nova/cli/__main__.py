#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova CLI 主入口

当使用 `python -m nova.cli` 时执行此文件
"""

import sys
from .main import cli_main

if __name__ == '__main__':
    sys.exit(cli_main())
