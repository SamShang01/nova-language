#!/usr/bin/env python3
# 直接使用源码的 Nova IDLE 测试

import sys
import os

# 添加源码目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("正在导入 Nova 模块...")
    from nova.cli.main import NovaIDLE
    from nova import __version__
    
    print(f"Nova 版本: {__version__}")
    print("正在创建 Nova IDLE 实例...")
    
    # 创建 Nova IDLE 实例
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
