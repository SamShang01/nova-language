"""
修复所有测试文件，添加本地源代码路径
"""

import os
import glob

def fix_test_file(filepath):
    """修复单个测试文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经修复
    if 'sys.path.insert(0, os.path.join' in content:
        print(f"跳过已修复的文件: {filepath}")
        return
    
    # 找到import unittest的位置
    lines = content.split('\n')
    import_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == 'import unittest':
            import_idx = i
            break
    
    if import_idx == -1:
        print(f"无法找到import unittest: {filepath}")
        return
    
    # 插入路径修复代码
    fix_code = '''import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))'''
    
    lines[import_idx] = fix_code
    new_content = '\n'.join(lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已修复: {filepath}")

# 修复所有测试文件
test_files = glob.glob('tests/test_*.py')
for filepath in test_files:
    fix_test_file(filepath)

print("\n所有测试文件修复完成！")
