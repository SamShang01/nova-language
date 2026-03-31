#!/usr/bin/env python3
# 详细的 Nova IDLE 测试

import sys
sys.path.insert(0, 'src')

try:
    print("正在导入 Nova IDLE...")
    from nova.cli.main import NovaIDLE
    
    print("正在创建 Nova IDLE 实例...")
    idle = NovaIDLE()
    
    print("Nova IDLE 实例创建成功！")
    print("正在启动主循环...")
    
    # 运行主循环
    idle.run()
    
except Exception as e:
    import traceback
    print(f"错误: {e}")
    print(f"详细错误信息:\n{traceback.format_exc()}")
    input("按回车键退出...")
