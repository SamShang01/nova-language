#!/usr/bin/env python3
# 测试 Nova IDLE 初始化

import sys
sys.path.insert(0, 'src')

try:
    from nova.cli.main import NovaIDLE
    
    print("正在创建 Nova IDLE...")
    idle = NovaIDLE()
    print("Nova IDLE 创建成功！")
    
    print("正在运行 Nova IDLE...")
    idle.run()
    
except Exception as e:
    import traceback
    print(f"错误: {e}")
    print(f"详细错误信息:\n{traceback.format_exc()}")
