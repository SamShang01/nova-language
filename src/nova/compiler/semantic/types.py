"""
Nova语言语义分析器类型定义
"""

class Type:
    """
    类型基类
    
    Attributes:
        name: 类型名称
    """
    
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        return self.name == other.name
    
    def __str__(self):
        return self.name

class PrimitiveType(Type):
    """
    基本类型
    """
    
    def __init__(self, name):
        super().__init__(name)

class StructType(Type):
    """
    结构体类型
    
    Attributes:
        name: 类型名称
        fields: 字段列表，格式为 [(field_name, field_type), ...]
        methods: 方法列表，格式为 [(method_name, params, return_type), ...]
    """
    
    def __init__(self, name, fields=None, methods=None):
        super().__init__(name)
        self.fields = fields or []
        self.methods = methods or []

class EnumType(Type):
    """
    枚举类型
    
    Attributes:
        name: 类型名称
        variants: 变体列表，格式为 [(variant_name, variant_type), ...]
    """
    
    def __init__(self, name, variants=None):
        super().__init__(name)
        self.variants = variants or []

class TraitType(Type):
    """
    Trait类型
    
    Attributes:
        name: 类型名称
        methods: 方法列表，格式为 [(method_name, method_signature), ...]
        type_params: 泛型类型参数列表
    """
    
    def __init__(self, name, methods=None, type_params=None):
        super().__init__(name)
        self.methods = methods or []
        self.type_params = type_params or []

class GenericType(Type):
    """
    泛型类型
    
    Attributes:
        name: 类型参数名称
        trait_constraints: Trait约束列表
    """
    
    def __init__(self, name):
        super().__init__(name)
        self.trait_constraints = []  # 存储Trait约束信息

class GenericStructType(Type):
    """
    泛型结构体类型
    
    Attributes:
        name: 类型名称
        type_params: 类型参数列表
        fields: 字段列表，格式为 [(field_name, field_type), ...]
    """
    
    def __init__(self, name, type_params=None, fields=None):
        super().__init__(name)
        self.type_params = type_params or []
        self.fields = fields or []

class GenericInstanceType(Type):
    """
    泛型实例类型
    
    Attributes:
        base_type: 基础类型
        type_args: 类型参数列表
    """
    
    def __init__(self, base_type, type_args=None):
        self.base_type = base_type
        self.type_args = type_args or []
        super().__init__(self._generate_name())
    
    def _generate_name(self):
        """
        生成类型名称
        
        Returns:
            str: 类型名称
        """
        if not self.type_args:
            return self.base_type.name
        type_args_str = ", ".join(str(arg) for arg in self.type_args)
        return f"{self.base_type.name}<{type_args_str}>"

# 数组类型
class ArrayType(Type):
    """
    数组类型
    
    Attributes:
        element_type: 元素类型
    """
    
    def __init__(self, element_type):
        super().__init__(f"[{element_type.name}]")
        self.element_type = element_type
        # fields属性将在类定义之后初始化
        self.fields = []
    
    def __eq__(self, other):
        if not isinstance(other, ArrayType):
            return False
        return self.element_type == other.element_type

# 元组类型
class TupleType(Type):
    """
    元组类型
    
    Attributes:
        element_types: 元素类型列表
    """
    
    def __init__(self, element_types):
        self.element_types = element_types
        super().__init__(self._generate_name())
    
    def _generate_name(self):
        """
        生成类型名称
        
        Returns:
            str: 类型名称
        """
        element_types_str = ", ".join(str(t) for t in self.element_types)
        return f"({element_types_str})"
    
    def __eq__(self, other):
        if not isinstance(other, TupleType):
            return False
        return self.element_types == other.element_types

# 函数类型
class FunctionType(Type):
    """
    函数类型
    
    Attributes:
        param_types: 参数类型列表
        return_type: 返回类型
    """
    
    def __init__(self, param_types, return_type):
        self.param_types = param_types
        self.return_type = return_type
        super().__init__(self._generate_name())
    
    def _generate_name(self):
        """
        生成类型名称
        
        Returns:
            str: 类型名称
        """
        param_types_str = ", ".join(str(t) for t in self.param_types)
        return f"func({param_types_str}) -> {self.return_type}"
    
    def __eq__(self, other):
        if not isinstance(other, FunctionType):
            return False
        return self.param_types == other.param_types and self.return_type == other.return_type

# 指针类型
class PointerType(Type):
    """
    指针类型
    
    Attributes:
        pointee_type: 指向的类型
        is_mutable: 是否可变
    """
    
    def __init__(self, pointee_type, is_mutable=False):
        self.pointee_type = pointee_type
        self.is_mutable = is_mutable
        super().__init__(self._generate_name())
    
    def _generate_name(self):
        """
        生成类型名称
        
        Returns:
            str: 类型名称
        """
        if self.is_mutable:
            return f"*mut {self.pointee_type}"
        else:
            return f"*{self.pointee_type}"
    
    def __eq__(self, other):
        if not isinstance(other, PointerType):
            return False
        return self.pointee_type == other.pointee_type and self.is_mutable == other.is_mutable

class ReferenceType(Type):
    """
    引用类型（类似C++的引用）
    
    Attributes:
        referenced_type: 引用的类型
        is_mutable: 是否可变引用
    """
    
    def __init__(self, referenced_type, is_mutable=False):
        self.referenced_type = referenced_type
        self.is_mutable = is_mutable
        super().__init__(self._generate_name())
    
    def _generate_name(self):
        if self.is_mutable:
            return f"&mut {self.referenced_type}"
        else:
            return f"&{self.referenced_type}"
    
    def __eq__(self, other):
        if not isinstance(other, ReferenceType):
            return False
        return self.referenced_type == other.referenced_type and self.is_mutable == other.is_mutable

class TypeType(Type):
    """
    类型类型（用于类型萃取）
    
    表示一个类型本身作为值，例如：
    - type: int 表示int类型
    - type: *T 表示指向T的指针类型
    """
    
    def __init__(self, wrapped_type):
        self.wrapped_type = wrapped_type
        super().__init__(f"type: {wrapped_type}")
    
    def __eq__(self, other):
        if not isinstance(other, TypeType):
            return False
        return self.wrapped_type == other.wrapped_type

# 预定义基本类型
INT_TYPE = PrimitiveType("int")
FLOAT_TYPE = PrimitiveType("float")
DOUBLE_TYPE = PrimitiveType("double")
STRING_TYPE = PrimitiveType("string")
BOOL_TYPE = PrimitiveType("bool")
CHAR_TYPE = PrimitiveType("char")
UNIT_TYPE = PrimitiveType("unit")
ANY_TYPE = PrimitiveType("any")
