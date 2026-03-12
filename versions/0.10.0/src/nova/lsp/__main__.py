"""
Nova语言服务器协议(LSP)主入口
"""

import argparse
from .server import NovaLanguageServer

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Nova语言服务器')
    parser.add_argument('--port', type=int, default=61009, help='监听端口')
    args = parser.parse_args()
    
    server = NovaLanguageServer()
    port = server.start(args.port)
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server.stop()