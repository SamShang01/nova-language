#!/usr/bin/env python3
# 测试 __main__.py 的路径问题

import sys
import os

# 模拟 __main__.py 中的路径插入
main_file = os.path.join(os.path.dirname(__file__), 'src', 'nova', '__main__.py')
print(f"模拟 __main__.py 文件路径: {main_file}")

# 计算路径插入
inserted_path = os.path.abspath(os.path.join(os.path.dirname(main_file), '..', '..'))
print(f"__main__.py 插入的路径: {inserted_path}")

# 实际需要的路径
actual_path = os.path.join(os.path.dirname(__file__), 'src')
print(f"实际需要的路径: {actual_path}")

# 检查路径是否正确
print(f"路径是否相同: {inserted_path == actual_path}")

# 检查 script.py 是否在插入的路径中
script_in_inserted = os.path.exists(os.path.join(inserted_path, 'script.py'))
print(f"script.py 是否在插入的路径中: {script_in_inserted}")

# 检查 nova 模块是否在插入的路径中
nova_in_inserted = os.path.exists(os.path.join(inserted_path, 'src', 'nova'))
print(f"nova 模块是否在插入的路径中: {nova_in_inserted}")
