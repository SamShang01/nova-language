"""
LSP协议定义
"""

class TextDocumentSyncKind:
    """
    文本文档同步类型
    """
    NoneSync = 0
    Full = 1
    Incremental = 2

class TextDocumentSaveReason:
    """
    文本文档保存原因
    """
    Manual = 1
    AfterDelay = 2
    FocusOut = 3

class DiagnosticSeverity:
    """
    诊断严重性
    """
    Error = 1
    Warning = 2
    Information = 3
    Hint = 4

class CompletionItemKind:
    """
    补全项类型
    """
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25

class SymbolKind:
    """
    符号类型
    """
    File = 1
    Module = 2
    Namespace = 3
    Package = 4
    Class = 5
    Method = 6
    Property = 7
    Field = 8
    Constructor = 9
    Enum = 10
    Interface = 11
    Function = 12
    Variable = 13
    Constant = 14
    String = 15
    Number = 16
    Boolean = 17
    Array = 18
    Object = 19
    Key = 20
    Null = 21
    EnumMember = 22
    Struct = 23
    Event = 24
    Operator = 25
    TypeParameter = 26

class Protocol:
    """
    LSP协议实现
    """
    
    def __init__(self):
        """
        初始化协议
        """
        self.jsonrpc = "2.0"
    
    def create_request(self, method, params, request_id):
        """
        创建请求
        
        Args:
            method: 方法名
            params: 参数
            request_id: 请求ID
        
        Returns:
            dict: 请求对象
        """
        return {
            "jsonrpc": self.jsonrpc,
            "id": request_id,
            "method": method,
            "params": params
        }
    
    def create_notification(self, method, params):
        """
        创建通知
        
        Args:
            method: 方法名
            params: 参数
        
        Returns:
            dict: 通知对象
        """
        return {
            "jsonrpc": self.jsonrpc,
            "method": method,
            "params": params
        }
    
    def create_response(self, request_id, result=None, error=None):
        """
        创建响应
        
        Args:
            request_id: 请求ID
            result: 结果
            error: 错误
        
        Returns:
            dict: 响应对象
        """
        response = {
            "jsonrpc": self.jsonrpc,
            "id": request_id
        }
        
        if error:
            response["error"] = error
        else:
            response["result"] = result
        
        return response
    
    def create_error(self, code, message, data=None):
        """
        创建错误
        
        Args:
            code: 错误码
            message: 错误消息
            data: 附加数据
        
        Returns:
            dict: 错误对象
        """
        error = {
            "code": code,
            "message": message
        }
        
        if data:
            error["data"] = data
        
        return error
