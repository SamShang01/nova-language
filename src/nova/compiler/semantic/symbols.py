"""
Nova语言语义分析器符号定义
"""

class Symbol:
    """
    符号基类
    
    Attributes:
        name: 符号名称
        type: 符号类型
    """
    
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class VariableSymbol(Symbol):
    """
    变量符号
    
    Attributes:
        name: 变量名称
        type: 变量类型
        mutable: 是否可变
        value: 变量值（可选）
    """
    
    def __init__(self, name, type, mutable=False, value=None):
        super().__init__(name, type)
        self.mutable = mutable
        self.value = value

class FunctionSymbol(Symbol):
    """
    函数符号
    
    Attributes:
        name: 函数名称
        return_type: 返回类型
        params: 参数列表，格式为 [ParameterDefinition对象 或 (param_name, param_type), ...]
        body: 函数体
    """
    
    def __init__(self, name, return_type, params=None, body=None):
        super().__init__(name, return_type)
        self.return_type = return_type
        self.params = params or []
        self.body = body

class GenericFunctionSymbol(Symbol):
    """
    泛型函数符号
    
    Attributes:
        name: 函数名称
        return_type: 返回类型
        type_params: 类型参数列表
        params: 参数列表，格式为 [(param_name, param_type), ...]
        body: 函数体
        where_clause: where子句
    """
    
    def __init__(self, name, return_type, type_params=None, params=None, body=None, where_clause=None):
        super().__init__(name, return_type)
        self.return_type = return_type
        self.type_params = type_params or []
        self.params = params or []
        self.body = body
        self.where_clause = where_clause

class TypeSymbol(Symbol):
    """
    类型符号
    
    Attributes:
        name: 类型名称
        type: 类型对象
        members: 类型成员（如结构体字段、枚举变体等）
        methods: 类型方法（如类方法、实例方法等）
    """
    
    def __init__(self, name, type, members=None, methods=None):
        super().__init__(name, type)
        self.members = members or []
        self.methods = methods or []

class TraitSymbol(Symbol):
    """
    特质符号
    
    Attributes:
        name: 特质名称
        methods: 方法列表
        type_params: 泛型类型参数
    """
    
    def __init__(self, name, methods=None, type_params=None):
        super().__init__(name, None)
        self.methods = methods or []
        self.type_params = type_params or []

class ImplSymbol(Symbol):
    """
    实现符号
    
    Attributes:
        type_name: 实现的类型名称
        trait_name: 实现的特质名称
        methods: 实现的方法列表
    """
    
    def __init__(self, type_name, trait_name, methods=None):
        super().__init__(f"{type_name}::{trait_name}", None)
        self.type_name = type_name
        self.trait_name = trait_name
        self.methods = methods or []
