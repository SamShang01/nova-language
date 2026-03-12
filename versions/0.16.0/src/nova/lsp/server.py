"""
Nova语言LSP服务器

实现Language Server Protocol服务器，提供代码智能提示、跳转定义等功能
"""

import sys
import json
import socket
import threading
import time
from typing import Dict, Any, List, Optional, Tuple


class LSPMessage:
    """
    LSP消息封装
    """
    
    def __init__(self, method: str, params: Dict[str, Any] = None, id: Optional[int] = None):
        """
        初始化LSP消息
        
        Args:
            method: 方法名
            params: 参数
            id: 消息ID（用于请求/响应）
        """
        self.method = method
        self.params = params
        self.id = id
    
    def to_json(self) -> str:
        """
        转换为JSON字符串
        
        Returns:
            str: JSON字符串
        """
        message = {
            "jsonrpc": "2.0",
            "method": self.method
        }
        if self.params:
            message["params"] = self.params
        if self.id is not None:
            message["id"] = self.id
        return json.dumps(message)
    
    @classmethod
    def from_json(cls, data: str) -> 'LSPMessage':
        """
        从JSON字符串创建LSP消息
        
        Args:
            data: JSON字符串
        
        Returns:
            LSPMessage: LSP消息
        """
        message = json.loads(data)
        return cls(
            method=message.get("method"),
            params=message.get("params"),
            id=message.get("id")
        )


class LSPServer:
    """
    LSP服务器
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        """
        初始化LSP服务器
        
        Args:
            host: 主机地址
            port: 端口号
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.thread = None
        self.message_id = 1
        
        # 文档缓存
        self.documents: Dict[str, str] = {}
        
        # 方法处理映射
        self.method_handlers = {
            "initialize": self.handle_initialize,
            "textDocument/didOpen": self.handle_text_document_did_open,
            "textDocument/didChange": self.handle_text_document_did_change,
            "textDocument/didClose": self.handle_text_document_did_close,
            "textDocument/hover": self.handle_text_document_hover,
            "textDocument/definition": self.handle_text_document_definition,
            "textDocument/completion": self.handle_text_document_completion,
            "textDocument/signatureHelp": self.handle_text_document_signature_help,
            "textDocument/rename": self.handle_text_document_rename,
            "textDocument/references": self.handle_text_document_references,
            "textDocument/codeAction": self.handle_text_document_code_action,
            "textDocument/codeLens": self.handle_text_document_code_lens,
            "textDocument/formatting": self.handle_text_document_formatting,
            "textDocument/rangeFormatting": self.handle_text_document_range_formatting,
            "workspace/symbol": self.handle_workspace_symbol,
            "shutdown": self.handle_shutdown,
            "exit": self.handle_exit
        }
    
    def start(self):
        """
        启动LSP服务器
        """
        self.running = True
        self.thread = threading.Thread(target=self._server_loop)
        self.thread.daemon = True
        self.thread.start()
        print(f"LSP服务器启动在 {self.host}:{self.port}")
    
    def stop(self):
        """
        停止LSP服务器
        """
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.thread:
            self.thread.join()
        print("LSP服务器已停止")
    
    def _server_loop(self):
        """
        服务器主循环
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            while self.running:
                try:
                    self.server_socket.settimeout(1.0)
                    self.client_socket, addr = self.server_socket.accept()
                    print(f"客户端连接: {addr}")
                    self._handle_client()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"服务器错误: {e}")
                    continue
        except Exception as e:
            print(f"服务器启动失败: {e}")
    
    def _handle_client(self):
        """
        处理客户端连接
        """
        try:
            while self.running:
                # 读取消息头
                header = b""
                while b"\r\n\r\n" not in header:
                    data = self.client_socket.recv(1024)
                    if not data:
                        break
                    header += data
                
                if not header:
                    break
                
                # 解析消息头
                header_str = header.decode('utf-8')
                content_length = 0
                for line in header_str.split('\r\n'):
                    if line.startswith('Content-Length:'):
                        content_length = int(line.split(':')[1].strip())
                        break
                
                # 读取消息体
                body = b""
                while len(body) < content_length:
                    data = self.client_socket.recv(content_length - len(body))
                    if not data:
                        break
                    body += data
                
                if not body:
                    break
                
                # 处理消息
                message_str = body.decode('utf-8')
                self._process_message(message_str)
        except Exception as e:
            print(f"客户端处理错误: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
    
    def _process_message(self, message_str: str):
        """
        处理消息
        
        Args:
            message_str: 消息字符串
        """
        try:
            message = LSPMessage.from_json(message_str)
            if message.method in self.method_handlers:
                response = self.method_handlers[message.method](message.params)
                if message.id is not None and response is not None:
                    self._send_response(message.id, response)
        except Exception as e:
            print(f"消息处理错误: {e}")
            if message.id is not None:
                self._send_error(message.id, str(e))
    
    def _send_response(self, id: int, result: Dict[str, Any]):
        """
        发送响应
        
        Args:
            id: 消息ID
            result: 结果
        """
        response = {
            "jsonrpc": "2.0",
            "id": id,
            "result": result
        }
        self._send_message(response)
    
    def _send_error(self, id: int, error_message: str):
        """
        发送错误
        
        Args:
            id: 消息ID
            error_message: 错误消息
        """
        error = {
            "jsonrpc": "2.0",
            "id": id,
            "error": {
                "code": -32603,
                "message": error_message
            }
        }
        self._send_message(error)
    
    def _send_notification(self, method: str, params: Dict[str, Any]):
        """
        发送通知
        
        Args:
            method: 方法名
            params: 参数
        """
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._send_message(notification)
    
    def _send_message(self, message: Dict[str, Any]):
        """
        发送消息
        
        Args:
            message: 消息
        """
        if not self.client_socket:
            return
        
        try:
            message_str = json.dumps(message)
            content_length = len(message_str.encode('utf-8'))
            header = f"Content-Length: {content_length}\r\n\r\n"
            full_message = header + message_str
            self.client_socket.sendall(full_message.encode('utf-8'))
        except Exception as e:
            print(f"发送消息错误: {e}")
    
    # 方法处理函数
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理初始化请求
        """
        return {
            "capabilities": {
                "textDocumentSync": 1,  # 增量同步
                "hoverProvider": True,
                "completionProvider": {
                    "resolveProvider": True,
                    "triggerCharacters": [".", "(", "="],
                    "completionItem": {
                        "documentationFormat": ["markdown", "plaintext"]
                    }
                },
                "signatureHelpProvider": {
                    "triggerCharacters": ["("]
                },
                "definitionProvider": True,
                "referencesProvider": True,
                "documentHighlightProvider": True,
                "documentSymbolProvider": True,
                "workspaceSymbolProvider": True,
                "codeActionProvider": True,
                "codeLensProvider": {
                    "resolveProvider": True
                },
                "documentFormattingProvider": True,
                "documentRangeFormattingProvider": True,
                "renameProvider": True
            }
        }
    
    def handle_text_document_did_open(self, params: Dict[str, Any]):
        """
        处理文档打开
        """
        uri = params.get("textDocument", {}).get("uri")
        text = params.get("textDocument", {}).get("text")
        if uri and text:
            self.documents[uri] = text
            print(f"文档打开: {uri}")
    
    def handle_text_document_did_change(self, params: Dict[str, Any]):
        """
        处理文档变更
        """
        uri = params.get("textDocument", {}).get("uri")
        changes = params.get("contentChanges", [])
        if uri and changes:
            # 简单处理：直接替换整个文档
            new_text = changes[0].get("text")
            if new_text:
                self.documents[uri] = new_text
                print(f"文档变更: {uri}")
    
    def handle_text_document_did_close(self, params: Dict[str, Any]):
        """
        处理文档关闭
        """
        uri = params.get("textDocument", {}).get("uri")
        if uri in self.documents:
            del self.documents[uri]
            print(f"文档关闭: {uri}")
    
    def handle_text_document_hover(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理悬停请求
        """
        # 简单实现：返回固定的悬停信息
        return {
            "contents": [
                {
                    "language": "nova",
                    "value": "Nova语言"
                },
                "这是一个悬停提示"
            ]
        }
    
    def handle_text_document_definition(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理定义跳转
        """
        # 简单实现：返回当前位置
        return {
            "uri": params.get("textDocument", {}).get("uri"),
            "range": {
                "start": {
                    "line": 0,
                    "character": 0
                },
                "end": {
                    "line": 0,
                    "character": 10
                }
            }
        }
    
    def handle_text_document_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理代码补全
        """
        # 简单实现：返回一些固定的补全项
        items = [
            {
                "label": "func",
                "kind": 3,  # 函数
                "detail": "函数定义",
                "documentation": "定义一个函数",
                "insertText": "func ${1:name}(${2:params}) ${3:-> ${4:type}} {\n    ${5:body}\n}"
            },
            {
                "label": "let",
                "kind": 14,  # 变量
                "detail": "变量定义",
                "documentation": "定义一个变量",
                "insertText": "let ${1:name} = ${2:value};"
            },
            {
                "label": "if",
                "kind": 16,  # 关键字
                "detail": "条件语句",
                "documentation": "条件判断",
                "insertText": "if (${1:condition}) {\n    ${2:body}\n}"
            },
            {
                "label": "class",
                "kind": 5,  # 类
                "detail": "类定义",
                "documentation": "定义一个类",
                "insertText": "class ${1:Name} {\n    ${2:body}\n}"
            }
        ]
        return {"items": items}
    
    def handle_text_document_signature_help(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理签名帮助
        """
        # 简单实现：返回固定的签名信息
        return {
            "signatures": [
                {
                    "label": "func example(a: int, b: string) -> int",
                    "documentation": "示例函数",
                    "parameters": [
                        {
                            "label": "a: int",
                            "documentation": "第一个参数"
                        },
                        {
                            "label": "b: string",
                            "documentation": "第二个参数"
                        }
                    ]
                }
            ],
            "activeSignature": 0,
            "activeParameter": 0
        }
    
    def handle_text_document_rename(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理重命名
        """
        # 简单实现：返回空的工作区编辑
        return {
            "changes": {}
        }
    
    def handle_text_document_references(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理引用查找
        """
        # 简单实现：返回当前位置
        return [
            {
                "uri": params.get("textDocument", {}).get("uri"),
                "range": {
                    "start": {
                        "line": 0,
                        "character": 0
                    },
                    "end": {
                        "line": 0,
                        "character": 10
                    }
                }
            }
        ]
    
    def handle_text_document_code_action(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理代码操作
        """
        # 简单实现：返回一些固定的代码操作
        return [
            {
                "title": "添加注释",
                "kind": "refactor",
                "edit": {
                    "changes": {}
                }
            }
        ]
    
    def handle_text_document_code_lens(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理代码透镜
        """
        # 简单实现：返回空列表
        return []
    
    def handle_text_document_formatting(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文档格式化
        """
        # 简单实现：返回空列表
        return []
    
    def handle_text_document_range_formatting(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理范围格式化
        """
        # 简单实现：返回空列表
        return []
    
    def handle_workspace_symbol(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理工作区符号
        """
        # 简单实现：返回空列表
        return []
    
    def handle_shutdown(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理关闭请求
        """
        return None
    
    def handle_exit(self, params: Dict[str, Any]):
        """
        处理退出请求
        """
        self.stop()


def main():
    """
    主函数
    """
    server = LSPServer()
    server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("服务器正在停止...")
        server.stop()


if __name__ == "__main__":
    main()