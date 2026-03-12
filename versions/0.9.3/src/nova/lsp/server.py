"""
Nova语言服务器实现
"""

import sys
import json
import socket
import threading
from .protocol import Protocol, TextDocumentSyncKind

class NovaLanguageServer:
    """
    Nova语言服务器
    """
    
    def __init__(self):
        """
        初始化语言服务器
        """
        self.protocol = Protocol()
        self.running = False
        self.thread = None
        
    def start(self, port=0):
        """
        启动语言服务器
        
        Args:
            port: 监听端口，0表示随机分配
        
        Returns:
            int: 实际监听的端口
        """
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen(1)
        
        # 获取实际端口
        _, actual_port = self.socket.getsockname()
        
        # 启动处理线程
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
        
        print(f"Nova Language Server started on port {actual_port}")
        return actual_port
    
    def stop(self):
        """
        停止语言服务器
        """
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.socket:
            self.socket.close()
        
    def _listen(self):
        """
        监听客户端连接
        """
        while self.running:
            try:
                client_socket, addr = self.socket.accept()
                print(f"Client connected from {addr}")
                
                # 处理客户端连接
                self._handle_client(client_socket)
                
            except socket.error:
                if not self.running:
                    break
                import traceback
                traceback.print_exc()
    
    def _handle_client(self, client_socket):
        """
        处理客户端连接
        
        Args:
            client_socket: 客户端socket
        """
        try:
            buffer = b''
            
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                buffer += data
                
                # 处理消息
                while True:
                    # 查找消息边界
                    header_end = buffer.find(b'\r\n\r\n')
                    if header_end == -1:
                        break
                    
                    # 解析头部
                    header = buffer[:header_end].decode('utf-8')
                    body_start = header_end + 4
                    
                    # 提取Content-Length
                    content_length = 0
                    for line in header.split('\r\n'):
                        if line.startswith('Content-Length:'):
                            content_length = int(line.split(':')[1].strip())
                            break
                    
                    # 检查是否有完整的消息
                    if len(buffer) < body_start + content_length:
                        break
                    
                    # 提取消息体
                    body = buffer[body_start:body_start + content_length].decode('utf-8')
                    buffer = buffer[body_start + content_length:]
                    
                    # 处理消息
                    self._handle_message(body, client_socket)
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
        finally:
            client_socket.close()
    
    def _handle_message(self, message, client_socket):
        """
        处理LSP消息
        
        Args:
            message: 消息内容
            client_socket: 客户端socket
        """
        try:
            # 检查消息是否为空
            if not message or message.strip() == '':
                return
                
            data = json.loads(message)
            
            # 处理不同类型的消息
            if 'method' in data:
                # 处理请求
                response = self._handle_request(data)
                if response:
                    self._send_message(response, client_socket)
            elif 'id' in data:
                # 处理响应
                pass
            else:
                # 处理通知
                self._handle_notification(data)
                
        except json.JSONDecodeError as e:
            print(f"JSON解码错误: {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    def _handle_request(self, request):
        """
        处理LSP请求
        
        Args:
            request: 请求数据
        
        Returns:
            dict: 响应数据
        """
        method = request.get('method')
        request_id = request.get('id')
        
        # 处理不同的请求方法
        if method == 'initialize':
            return self._handle_initialize(request_id, request.get('params', {}))
        elif method == 'textDocument/definition':
            return self._handle_definition(request_id, request.get('params', {}))
        elif method == 'textDocument/completion':
            return self._handle_completion(request_id, request.get('params', {}))
        elif method == 'textDocument/hover':
            return self._handle_hover(request_id, request.get('params', {}))
        elif method == 'shutdown':
            return self._handle_shutdown(request_id)
        elif method == 'exit':
            self.running = False
            return None
        
        # 默认响应
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32601,
                'message': f'Method not implemented: {method}'
            }
        }
    
    def _handle_notification(self, notification):
        """
        处理LSP通知
        
        Args:
            notification: 通知数据
        """
        method = notification.get('method')
        
        if method == 'textDocument/didOpen':
            self._handle_document_open(notification.get('params', {}))
        elif method == 'textDocument/didChange':
            self._handle_document_change(notification.get('params', {}))
        elif method == 'textDocument/didSave':
            self._handle_document_save(notification.get('params', {}))
        elif method == 'textDocument/didClose':
            self._handle_document_close(notification.get('params', {}))
    
    def _handle_initialize(self, request_id, params):
        """
        处理初始化请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
        
        Returns:
            dict: 响应数据
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'capabilities': {
                    'textDocumentSync': {
                        'kind': TextDocumentSyncKind.Incremental,
                        'change': 1,
                        'willSave': False,
                        'willSaveWaitUntil': False,
                        'save': {
                            'includeText': False
                        }
                    },
                    'definitionProvider': True,
                    'completionProvider': {
                        'resolveProvider': False,
                        'triggerCharacters': ['.', ':', '(']
                    },
                    'hoverProvider': True
                }
            }
        }
    
    def _handle_definition(self, request_id, params):
        """
        处理定义查找请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
        
        Returns:
            dict: 响应数据
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': None
        }
    
    def _handle_completion(self, request_id, params):
        """
        处理补全请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
        
        Returns:
            dict: 响应数据
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'isIncomplete': False,
                'items': []
            }
        }
    
    def _handle_hover(self, request_id, params):
        """
        处理悬停请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
        
        Returns:
            dict: 响应数据
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': None
        }
    
    def _handle_shutdown(self, request_id):
        """
        处理关闭请求
        
        Args:
            request_id: 请求ID
        
        Returns:
            dict: 响应数据
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': None
        }
    
    def _handle_document_open(self, params):
        """
        处理文档打开通知
        
        Args:
            params: 通知参数
        """
        pass
    
    def _handle_document_change(self, params):
        """
        处理文档变更通知
        
        Args:
            params: 通知参数
        """
        pass
    
    def _handle_document_save(self, params):
        """
        处理文档保存通知
        
        Args:
            params: 通知参数
        """
        pass
    
    def _handle_document_close(self, params):
        """
        处理文档关闭通知
        
        Args:
            params: 通知参数
        """
        pass
    
    def _send_message(self, message, client_socket):
        """
        发送消息到客户端
        
        Args:
            message: 消息数据
            client_socket: 客户端socket
        """
        try:
            body = json.dumps(message, ensure_ascii=False).encode('utf-8')
            header = f"Content-Length: {len(body)}\r\n\r\n".encode('utf-8')
            client_socket.sendall(header + body)
        except Exception as e:
            import traceback
            traceback.print_exc()

# 命令行入口
if __name__ == '__main__':
    server = NovaLanguageServer()
    port = server.start()
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server.stop()