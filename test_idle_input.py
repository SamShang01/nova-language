#!/usr/bin/env python3
# 测试 Nova IDLE 输入处理逻辑

import re

def test_input_processing():
    # 模拟用户输入
    test_inputs = [
        'let a=1;执行：let a=1;（前后一致）',
        'a;执行：a;（前后一致）',
        'print(1);执行：print(1);（前后一致）'
    ]
    
    for input_text in test_inputs:
        print(f"原始输入: '{input_text}'")
        
        # 提取Nova代码（移除可能的中文说明）
        nova_code = re.sub(r'执行：.*', '', input_text).strip()
        print(f"提取后: '{nova_code}'")
        print()

if __name__ == '__main__':
    test_input_processing()
