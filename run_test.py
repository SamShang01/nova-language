#!/usr/bin/env python
"""
运行测试并过滤输出
"""

import subprocess
import sys

# 运行测试
result = subprocess.run(
    [sys.executable, "-m", "nova", "run", "test_multiple_trait_constraints.nova"],
    capture_output=True,
    text=True
)

# 输出所有内容
print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)

# 过滤包含 COMPARE 的行
print("\n\n过滤 COMPARE 相关的行:")
for line in result.stdout.split('\n') + result.stderr.split('\n'):
    if 'COMPARE' in line or 'Error' in line or 'Exception' in line:
        print(line)
