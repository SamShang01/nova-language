"""
Nova语言抽象语法树(AST)节点定义
"""

class Node:
    """
    AST节点基类
    """
    
    def __init__(self, line, column):
        self.line = line
        self.column = column
    
    def accept(self, visitor):
        """
        接受访问者
        
        Args:
            visitor: 访问者对象
        """
        method_name = f"visit_{self.__class__.__name__}"
        if hasattr(visitor, method_name):
            return getattr(visitor, method_name)(self)
        else:
            return self.generic_visit(visitor)
    
    def generic_visit(self, visitor):
        """
        通用访问方法
        
        Args:
            visitor: 访问者对象
        """
        pass

# 程序节点
class Program(Node):
    """
    程序节点
    """
    
    def __init__(self, line, column, statements):
        super().__init__(line, column)
        self.statements = statements

# 模块声明
class ModuleDeclaration(Node):
    """
    模块声明节点
    """
    
    def __init__(self, line, column, name):
        super().__init__(line, column)
        self.name = name

# 导入语句
class ImportStatement(Node):
    """
    导入语句节点
    """
    
    def __init__(self, line, column, path, alias=None):
        super().__init__(line, column)
        self.path = path
        self.alias = alias

# Feature语句
class FeatureStatement(Node):
    """
    Feature语句节点
    """
    
    def __init__(self, line, column, feature_name):
        super().__init__(line, column)
        self.feature_name = feature_name

# 函数定义
class FunctionDefinition(Node):
    """
    函数定义节点
    """
    
    def __init__(self, line, column, name, params, return_type, body):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body


class ParameterDefinition(Node):
    """
    参数定义节点
    
    支持普通参数、默认值参数、可变参数和关键字可变参数
    """
    
    def __init__(self, line, column, name, param_type, default_value=None, 
                 is_varargs=False, is_kwargs=False):
        super().__init__(line, column)
        self.name = name
        self.param_type = param_type
        self.default_value = default_value
        self.is_varargs = is_varargs
        self.is_kwargs = is_kwargs

# 变量声明
class VariableDeclaration(Node):
    """
    变量声明节点
    """
    
    def __init__(self, line, column, name, var_type, value, mutable=False):
        super().__init__(line, column)
        self.name = name
        self.var_type = var_type
        self.value = value
        self.mutable = mutable

# 常量声明
class ConstantDeclaration(Node):
    """
    常量声明节点
    """
    
    def __init__(self, line, column, name, const_type, value):
        super().__init__(line, column)
        self.name = name
        self.const_type = const_type
        self.value = value

# 表达式基类
class Expression(Node):
    """
    表达式节点基类
    """
    pass

# 二元表达式
class BinaryExpression(Expression):
    """
    二元表达式节点
    """
    
    def __init__(self, line, column, left, operator, right):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right

# 一元表达式
class UnaryExpression(Expression):
    """
    一元表达式节点
    """
    
    def __init__(self, line, column, operator, operand):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand

# 字面量表达式
class LiteralExpression(Expression):
    """
    字面量表达式节点
    """
    
    def __init__(self, line, column, value, literal_type):
        super().__init__(line, column)
        self.value = value
        self.literal_type = literal_type

# 标识符表达式
class IdentifierExpression(Expression):
    """
    标识符表达式节点
    """
    
    def __init__(self, line, column, name):
        super().__init__(line, column)
        self.name = name

# 调用表达式
class CallExpression(Expression):
    """
    调用表达式节点
    """
    
    def __init__(self, line, column, callee, arguments):
        super().__init__(line, column)
        self.callee = callee
        self.arguments = arguments

# 命名参数表达式
class NamedArgumentExpression(Expression):
    """
    命名参数表达式节点
    """
    
    def __init__(self, line, column, name, value):
        super().__init__(line, column)
        self.name = name
        self.value = value

# 成员表达式
class MemberExpression(Expression):
    """
    成员表达式节点
    """
    
    def __init__(self, line, column, object, member):
        super().__init__(line, column)
        self.object = object
        self.member = member

# 索引表达式
class IndexExpression(Expression):
    """
    索引表达式节点
    """
    
    def __init__(self, line, column, object, index):
        super().__init__(line, column)
        self.object = object
        self.index = index

# 数组字面量表达式
class ArrayLiteralExpression(Expression):
    """
    数组字面量表达式节点
    """
    
    def __init__(self, line, column, elements):
        super().__init__(line, column)
        self.elements = elements

# 元组字面量表达式
class TupleLiteralExpression(Expression):
    """
    元组字面量表达式节点
    """
    
    def __init__(self, line, column, elements):
        super().__init__(line, column)
        self.elements = elements

# Lambda表达式
class LambdaExpression(Expression):
    """
    Lambda表达式节点
    """
    
    def __init__(self, line, column, params, body):
        super().__init__(line, column)
        self.params = params
        self.body = body

# If语句
class IfStatement(Node):
    """
    If语句节点
    """
    
    def __init__(self, line, column, condition, then_branch, else_branch=None):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

# For循环
class ForLoop(Node):
    """
    For循环节点
    """
    
    def __init__(self, line, column, variable, iterable, body):
        super().__init__(line, column)
        self.variable = variable
        self.iterable = iterable
        self.body = body

# While循环
class WhileLoop(Node):
    """
    While循环节点
    """
    
    def __init__(self, line, column, condition, body):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

# Loop语句
class LoopStatement(Node):
    """
    Loop语句节点
    """
    
    def __init__(self, line, column, body):
        super().__init__(line, column)
        self.body = body

# Match语句
class MatchStatement(Node):
    """
    Match语句节点
    """
    
    def __init__(self, line, column, expression, cases):
        super().__init__(line, column)
        self.expression = expression
        self.cases = cases

# Return语句
class ReturnStatement(Node):
    """
    Return语句节点
    """
    
    def __init__(self, line, column, value=None):
        super().__init__(line, column)
        self.value = value

# Break语句
class BreakStatement(Node):
    """
    Break语句节点
    """
    
    def __init__(self, line, column):
        super().__init__(line, column)

# Continue语句
class ContinueStatement(Node):
    """
    Continue语句节点
    """
    
    def __init__(self, line, column):
        super().__init__(line, column)

# 结构体定义
class StructDefinition(Node):
    """
    结构体定义节点
    """
    
    def __init__(self, line, column, name, fields, methods=None):
        super().__init__(line, column)
        self.name = name
        self.fields = fields
        self.methods = methods or []

# 枚举定义
class EnumDefinition(Node):
    """
    枚举定义节点
    """
    
    def __init__(self, line, column, name, variants):
        super().__init__(line, column)
        self.name = name
        self.variants = variants

# Trait定义
class TraitDefinition(Node):
    """
    Trait定义节点
    """
    
    def __init__(self, line, column, name, methods):
        super().__init__(line, column)
        self.name = name
        self.methods = methods

# Impl块
class ImplBlock(Node):
    """
    Impl块节点
    """
    
    def __init__(self, line, column, type_name, methods, trait_name=None):
        super().__init__(line, column)
        self.type_name = type_name
        self.methods = methods
        self.trait_name = trait_name

# 泛型类型参数
class GenericTypeParameter(Node):
    """
    泛型类型参数节点
    """
    
    def __init__(self, line, column, name, constraints=None):
        super().__init__(line, column)
        self.name = name
        self.constraints = constraints

# 泛型函数定义
class GenericFunctionDefinition(FunctionDefinition):
    """
    泛型函数定义节点
    """
    
    def __init__(self, line, column, name, type_params, params, return_type, body, where_clause=None):
        super().__init__(line, column, name, params, return_type, body)
        self.type_params = type_params
        self.where_clause = where_clause

# 泛型结构体定义
class GenericStructDefinition(StructDefinition):
    """
    泛型结构体定义节点
    """
    
    def __init__(self, line, column, name, type_params, fields, methods=None):
        super().__init__(line, column, name, fields, methods)
        self.type_params = type_params

# 类型约束
class TypeConstraint(Node):
    """
    类型约束节点
    """
    
    def __init__(self, line, column, type_param, trait_name):
        super().__init__(line, column)
        self.type_param = type_param
        self.trait_name = trait_name

# Where子句
class WhereClause(Node):
    """
    Where子句节点
    """
    
    def __init__(self, line, column, constraints):
        super().__init__(line, column)
        self.constraints = constraints

# 类型表达式
class TypeExpression(Expression):
    """
    类型表达式节点
    """
    
    def __init__(self, line, column, name):
        super().__init__(line, column)
        self.name = name

# 泛型类型表达式
class GenericTypeExpression(Expression):
    """
    泛型类型表达式节点
    """
    
    def __init__(self, line, column, base_type, type_args):
        super().__init__(line, column)
        self.base_type = base_type
        self.type_args = type_args

# 数组类型表达式
class ArrayTypeExpression(Expression):
    """
    数组类型表达式节点
    """
    
    def __init__(self, line, column, element_type):
        super().__init__(line, column)
        self.element_type = element_type

# 元组类型表达式
class TupleTypeExpression(Expression):
    """
    元组类型表达式节点
    """
    
    def __init__(self, line, column, element_types):
        super().__init__(line, column)
        self.element_types = element_types

# 函数类型表达式
class FunctionTypeExpression(Expression):
    """
    函数类型表达式节点
    """
    
    def __init__(self, line, column, param_types, return_type):
        super().__init__(line, column)
        self.param_types = param_types
        self.return_type = return_type
