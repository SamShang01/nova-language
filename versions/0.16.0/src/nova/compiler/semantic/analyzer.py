"""
Nova语言语义分析器
"""

from nova.compiler.parser import *
from nova.compiler.semantic.symbols import *
from nova.compiler.semantic.symbols import TypeSymbol
from nova.compiler.semantic.types import *
from nova.compiler.semantic.scope import Scope
from nova.compiler.semantic.errors import SemanticError
from nova.compiler.features import get_feature_manager

class SemanticAnalyzer:
    """
    语义分析器
    
    负责遍历AST并进行类型检查和作用域分析
    """
    
    def __init__(self):
        """
        初始化语义分析器
        """
        # 全局作用域
        self.global_scope = Scope("global")
        # 当前作用域
        self.current_scope = self.global_scope
        # 类型映射
        self.types = {
            "int": INT_TYPE,
            "float": FLOAT_TYPE,
            "double": DOUBLE_TYPE,
            "string": STRING_TYPE,
            "bool": BOOL_TYPE,
            "char": CHAR_TYPE,
            "unit": UNIT_TYPE,
        }
        # 类型实现的 Trait 映射
        self.type_traits = {}
        # 特性管理器
        self.feature_manager = get_feature_manager()
        # 内置函数
        self._initialize_builtins()
    
    def _initialize_builtins(self):
        """
        初始化内置函数
        """
        # 添加基本类型到types字典
        self.types["int"] = INT_TYPE
        self.types["float"] = FLOAT_TYPE
        self.types["double"] = DOUBLE_TYPE
        self.types["string"] = STRING_TYPE
        self.types["bool"] = BOOL_TYPE
        self.types["char"] = CHAR_TYPE
        self.types["unit"] = UNIT_TYPE
        self.types["any"] = ANY_TYPE
        
        # 初始化Vector类型
        self._initialize_vector_type()
    
    def _initialize_vector_type(self):
        """
        初始化Vector类型
        """
        # 创建Vector类型
        vector_type = StructType("Vector", fields=[])
        self.types["Vector"] = vector_type
        
        # 添加Vector方法到fields列表
        # isEmpty() -> bool
        vector_type.fields.append(("isEmpty", FunctionType([], BOOL_TYPE)))
        # size() -> int
        vector_type.fields.append(("size", FunctionType([], INT_TYPE)))
        # push(value: T) -> unit
        vector_type.fields.append(("push", FunctionType([ANY_TYPE], UNIT_TYPE)))
        # contains(value: T) -> bool
        vector_type.fields.append(("contains", FunctionType([ANY_TYPE], BOOL_TYPE)))
        # clear() -> unit
        vector_type.fields.append(("clear", FunctionType([], UNIT_TYPE)))
        # first() -> T
        vector_type.fields.append(("first", FunctionType([], ANY_TYPE)))
        # last() -> T
        vector_type.fields.append(("last", FunctionType([], ANY_TYPE)))
        # add(value: T) -> unit
        vector_type.fields.append(("add", FunctionType([ANY_TYPE], UNIT_TYPE)))
        # remove(value: T) -> unit
        vector_type.fields.append(("remove", FunctionType([ANY_TYPE], UNIT_TYPE)))
        # toArray() -> [T]
        vector_type.fields.append(("toArray", FunctionType([], ArrayType(ANY_TYPE))))
        
        # print函数
        print_func = FunctionSymbol(
            "print",
            UNIT_TYPE,
            params=[("value", ANY_TYPE)]
        )
        self.global_scope.declare_symbol(print_func)
        
        # println函数
        println_func = FunctionSymbol(
            "println",
            UNIT_TYPE,
            params=[("value", ANY_TYPE)]
        )
        self.global_scope.declare_symbol(println_func)
        
        # len函数
        len_func = FunctionSymbol(
            "len",
            INT_TYPE,
            params=[("value", ANY_TYPE)]
        )
        self.global_scope.declare_symbol(len_func)
        
        # str函数
        str_func = FunctionSymbol(
            "str",
            STRING_TYPE,
            params=[("value", ANY_TYPE)]
        )
        self.global_scope.declare_symbol(str_func)
        
        # type函数
        type_func = FunctionSymbol(
            "type",
            STRING_TYPE,
            params=[("value", INT_TYPE)]
        )
        self.global_scope.declare_symbol(type_func)
        
        # int函数
        int_func = FunctionSymbol(
            "int",
            INT_TYPE,
            params=[("value", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(int_func)
        
        # float函数
        float_func = FunctionSymbol(
            "float",
            FLOAT_TYPE,
            params=[("value", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(float_func)
        
        # Double构造函数
        double_func = FunctionSymbol(
            "Double",
            DOUBLE_TYPE,
            params=[("value", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(double_func)
        
        # dis函数 - 反汇编Nova代码
        dis_func = FunctionSymbol(
            "dis",
            UNIT_TYPE,
            params=[("code", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(dis_func)
        
        # this变量（用于类方法中）
        this_var = VariableSymbol("this", ANY_TYPE, mutable=False)
        self.global_scope.declare_symbol(this_var)
        
        # 字符串函数
        to_upper_func = FunctionSymbol(
            "to_upper",
            STRING_TYPE,
            params=[("s", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(to_upper_func)
        
        to_lower_func = FunctionSymbol(
            "to_lower",
            STRING_TYPE,
            params=[("s", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(to_lower_func)
        
        trim_func = FunctionSymbol(
            "trim",
            STRING_TYPE,
            params=[("s", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(trim_func)
        
        split_func = FunctionSymbol(
            "split",
            STRING_TYPE,
            params=[("s", STRING_TYPE), ("delimiter", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(split_func)
        
        join_func = FunctionSymbol(
            "join",
            STRING_TYPE,
            params=[("strings", STRING_TYPE), ("delimiter", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(join_func)
        
        contains_func = FunctionSymbol(
            "contains",
            BOOL_TYPE,
            params=[("s", STRING_TYPE), ("substr", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(contains_func)
        
        starts_with_func = FunctionSymbol(
            "starts_with",
            BOOL_TYPE,
            params=[("s", STRING_TYPE), ("prefix", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(starts_with_func)
        
        ends_with_func = FunctionSymbol(
            "ends_with",
            BOOL_TYPE,
            params=[("s", STRING_TYPE), ("suffix", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(ends_with_func)
        
        replace_func = FunctionSymbol(
            "replace",
            STRING_TYPE,
            params=[("s", STRING_TYPE), ("old", STRING_TYPE), ("new", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(replace_func)
        
        substring_func = FunctionSymbol(
            "substring",
            STRING_TYPE,
            params=[("s", STRING_TYPE), ("start", INT_TYPE)]
        )
        self.global_scope.declare_symbol(substring_func)
        
        # 数学函数
        sin_func = FunctionSymbol(
            "sin",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(sin_func)
        
        cos_func = FunctionSymbol(
            "cos",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(cos_func)
        
        tan_func = FunctionSymbol(
            "tan",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(tan_func)
        
        sqrt_func = FunctionSymbol(
            "sqrt",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(sqrt_func)
        
        pow_func = FunctionSymbol(
            "pow",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE), ("y", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(pow_func)
        
        abs_func = FunctionSymbol(
            "abs",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(abs_func)
        
        floor_func = FunctionSymbol(
            "floor",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(floor_func)
        
        ceil_func = FunctionSymbol(
            "ceil",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(ceil_func)
        
        round_func = FunctionSymbol(
            "round",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(round_func)
        
        min_func = FunctionSymbol(
            "min",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE), ("y", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(min_func)
        
        max_func = FunctionSymbol(
            "max",
            FLOAT_TYPE,
            params=[("x", FLOAT_TYPE), ("y", FLOAT_TYPE)]
        )
        self.global_scope.declare_symbol(max_func)
        
        reverse_func = FunctionSymbol(
            "reverse",
            STRING_TYPE,
            params=[("s", STRING_TYPE)]
        )
        self.global_scope.declare_symbol(reverse_func)
        
        # 数学常量
        pi_var = VariableSymbol("PI", FLOAT_TYPE)
        self.global_scope.declare_symbol(pi_var)
        
        e_var = VariableSymbol("E", FLOAT_TYPE)
        self.global_scope.declare_symbol(e_var)
    
    def analyze(self, program):
        """
        分析程序
        
        Args:
            program: 程序节点
        
        Returns:
            Program: 分析后的程序节点
        
        Raises:
            SemanticError: 语义分析错误
        """
        for statement in program.statements:
            statement.accept(self)
        return program
    
    def visit_Program(self, node):
        """
        访问程序节点
        """
        for statement in node.statements:
            statement.accept(self)
    
    def visit_ModuleDeclaration(self, node):
        """
        访问模块声明节点
        """
        # 简化实现，仅记录模块名称
        pass
    
    def visit_ImportStatement(self, node):
        """
        访问导入语句节点
        """
        # 简化实现，仅记录导入路径
        pass
    
    def visit_FeatureStatement(self, node):
        """
        访问Feature语句节点
        
        处理 from __future__ import ... 语句
        """
        try:
            # 启用特性
            self.feature_manager.enable(node.feature_name)
        except ValueError as e:
            # 特性不存在，抛出语义错误
            raise SemanticError(
                f"Unknown feature: {node.feature_name}",
                node.line,
                node.column
            )
    
    def visit_FunctionDefinition(self, node):
        """
        访问函数定义节点
        """
        # 检查是否是结构体方法（有self参数）
        is_method = False
        struct_name = None
        if node.params and node.params[0].name == "self":
            is_method = True
            # 尝试从返回类型中获取结构体名称
            if node.return_type:
                # 解析返回类型
                return_type_obj = self._resolve_type(node.return_type)
                # 尝试获取结构体名称
                if hasattr(return_type_obj, 'name'):
                    struct_name = return_type_obj.name
                elif isinstance(node.return_type, str):
                    # 如果返回类型是字符串，直接使用字符串作为结构体名称
                    struct_name = node.return_type
                elif hasattr(node.return_type, 'name'):
                    # 如果返回类型是一个类型表达式，使用其名称作为结构体名称
                    struct_name = node.return_type.name
            
            # 尝试从当前 Impl 块上下文中获取结构体名称
            # 即使从返回类型中获取了结构体名称，也要优先使用 Impl 块上下文
            if hasattr(self, 'current_impl_type') and self.current_impl_type:
                struct_name = self.current_impl_type
        
        # 保存当前作用域
        original_scope = self.current_scope
        
        # 解析返回类型
        return_type = UNIT_TYPE
        if node.return_type:
            return_type = self._resolve_type(node.return_type)
        else:
            # 如果没有显式返回类型，先设置为UNIT_TYPE，稍后推断
            return_type = UNIT_TYPE
        
        # 创建函数符号
        func_symbol = FunctionSymbol(
            node.name,
            return_type,
            params=node.params,
            body=node.body
        )
        
        # 声明函数到作用域（在分析函数体之前）
        try:
            original_scope.declare_symbol(func_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 创建函数作用域
        func_scope = Scope(node.name, parent=original_scope)
        
        # 检查是否是Impl块中的方法，如果是，并且没有显式声明self参数，从父作用域中复制self符号
        if hasattr(self, 'current_impl_type') and self.current_impl_type and not any(param.name == 'self' for param in node.params):
            # 从当前作用域（method_scope）中查找self符号
            self_symbol = self.current_scope.resolve_symbol('self')
            if self_symbol:
                # 将self符号复制到func_scope中
                try:
                    func_scope.declare_symbol(self_symbol)
                except ValueError as e:
                    # 忽略已存在的符号错误
                    pass
        
        # 声明参数
        for param in node.params:
            if isinstance(param, tuple):
                # 兼容旧格式：元组(name, type)
                param_name, param_type = param
            else:
                # 新格式：ParameterDefinition对象
                param_name = param.name
                param_type = param.param_type
            
            # 特殊处理self参数
            if param_name == "self" and struct_name and struct_name in self.types:
                # 使用结构体类型作为self的类型
                param_type_obj = self.types[struct_name]
            else:
                # 普通参数，正常解析类型
                param_type_obj = self._resolve_type(param_type)
            
            # 创建变量符号并声明到函数作用域
            var_symbol = VariableSymbol(param_name, param_type_obj)
            try:
                func_scope.declare_symbol(var_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        # 特殊处理结构体方法
        if is_method and struct_name and struct_name in self.types:
            # 为方法添加结构体名称
            struct_name_symbol = TypeSymbol(struct_name, self.types[struct_name])
            try:
                func_scope.declare_symbol(struct_name_symbol)
            except ValueError as e:
                # 忽略已存在的符号错误
                pass
        
        # 分析函数体（抽象方法没有函数体）
        # 直接使用func_scope作为当前作用域进行分析
        old_scope = self.current_scope
        self.current_scope = func_scope
        try:
            if node.body:
                for stmt in node.body:
                    stmt.accept(self)
        finally:
            self.current_scope = old_scope
        
        # 如果没有显式返回类型，推断返回类型
        if not node.return_type:
            inferred_return_type = self._infer_return_type(node.body)
            if inferred_return_type:
                # 更新函数符号的返回类型
                func_symbol.return_type = inferred_return_type
    
    def visit_GenericFunctionDefinition(self, node):
        """
        访问泛型函数定义节点
        """
        # 创建泛型函数作用域
        generic_scope = Scope(f"generic_{node.name}", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = generic_scope
        
        # 声明泛型类型参数
        type_param_map = {}
        for type_param in node.type_params:
            # 创建泛型类型
            generic_type = GenericType(type_param.name)
            self.types[type_param.name] = generic_type
            type_param_map[type_param.name] = generic_type
            
            # 创建类型符号
            type_symbol = TypeSymbol(type_param.name, generic_type)
            try:
                self.current_scope.declare_symbol(type_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        # 检查where子句
        print(f"DEBUG visit_GenericFunctionDefinition: node.where_clause = {getattr(node, 'where_clause', None)}")
        where_clause = getattr(node, 'where_clause', None)
        if where_clause and (not isinstance(where_clause, list) or len(where_clause) > 0):
            print(f"DEBUG visit_GenericFunctionDefinition: calling _check_trait_constraints")
            self._check_trait_constraints(where_clause, type_param_map)
        else:
            print(f"DEBUG visit_GenericFunctionDefinition: no where_clause found")
        
        # 解析返回类型
        return_type = UNIT_TYPE
        if node.return_type:
            return_type = self._resolve_type(node.return_type)
        
        # 恢复作用域
        self.current_scope = old_scope
        
        # 创建泛型函数符号
        func_symbol = GenericFunctionSymbol(
            node.name,
            return_type,
            type_params=node.type_params,
            params=node.params,
            body=node.body,
            where_clause=node.where_clause
        )
        
        # 在全局作用域中声明函数
        try:
            self.current_scope.declare_symbol(func_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 创建函数作用域
        func_scope = Scope(node.name, parent=self.current_scope)
        self.current_scope = func_scope
        
        # 声明参数
        for param in node.params:
            if isinstance(param, tuple):
                # 兼容旧格式：元组(name, type)
                param_name, param_type = param
            else:
                # 新格式：ParameterDefinition对象
                param_name = param.name
                param_type = param.param_type
            
            param_type_obj = self._resolve_type(param_type)
            
            # 调试信息：检查泛型类型的trait_constraints
            if hasattr(param_type_obj, 'name') and param_type_obj.name in self.types:
                stored_type = self.types[param_type_obj.name]
                if hasattr(stored_type, 'trait_constraints'):
                    print(f"DEBUG visit_GenericFunctionDefinition: param {param_name} type {param_type_obj.name} trait_constraints: {stored_type.trait_constraints}")
            
            var_symbol = VariableSymbol(param_name, param_type_obj)
            try:
                self.current_scope.declare_symbol(var_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        # 分析函数体（抽象方法没有函数体）
        if node.body:
            for stmt in node.body:
                stmt.accept(self)
        
        # 恢复作用域
        self.current_scope = old_scope
    
    def visit_VariableDeclaration(self, node):
        """
        访问变量声明节点
        """
        # 解析类型
        var_type = None
        if node.var_type:
            var_type = self._resolve_type(node.var_type)
            # 如果是auto类型，从值推断类型
            if var_type == ANY_TYPE and node.value:
                var_type = self._infer_type(node.value)
        elif node.value:
            # 从值推断类型
            var_type = self._infer_type(node.value)
        else:
            raise SemanticError(node.line, node.column, "Variable declaration requires either a type annotation or an initial value")
        
        # 创建变量符号
        var_symbol = VariableSymbol(
            node.name,
            var_type,
            mutable=node.mutable,
            value=node.value
        )
        
        # 声明变量
        try:
            self.current_scope.declare_symbol(var_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 分析初始化值
        if node.value:
            value_type = self._infer_type(node.value)
            if not self._types_compatible(value_type, var_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Type mismatch: expected {var_type}, got {value_type}"
                )
    
    def visit_ConstantDeclaration(self, node):
        """
        访问常量声明节点
        """
        # 解析类型
        const_type = None
        if node.const_type:
            const_type = self._resolve_type(node.const_type)
            # 如果是auto类型，从值推断类型
            if const_type == ANY_TYPE and node.value:
                const_type = self._infer_type(node.value)
        elif node.value:
            # 从值推断类型
            const_type = self._infer_type(node.value)
        else:
            raise SemanticError(node.line, node.column, "Constant declaration requires either a type annotation or an initial value")
        
        # 创建常量符号
        const_symbol = VariableSymbol(
            node.name,
            const_type,
            mutable=False,
            value=node.value
        )
        
        # 声明常量（如果已存在则覆盖）
        try:
            self.current_scope.declare_symbol(const_symbol)
        except ValueError:
            # 如果符号已存在，更新它
            self.current_scope.symbols[node.name] = const_symbol
        
        # 分析初始化值
        if node.value:
            value_type = self._infer_type(node.value)
            if not self._types_compatible(value_type, const_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Type mismatch: expected {const_type}, got {value_type}"
                )
    
    def visit_IfStatement(self, node):
        """
        访问If语句节点
        """
        # 分析条件表达式
        condition_type = self._infer_type(node.condition)
        if condition_type != BOOL_TYPE:
            raise SemanticError(
                node.line, node.column,
                f"If condition must be of type bool, got {condition_type}"
            )
        
        # 分析then分支
        for stmt in node.then_branch:
            stmt.accept(self)
        
        # 分析else分支
        if node.else_branch:
            if isinstance(node.else_branch, list):
                for stmt in node.else_branch:
                    stmt.accept(self)
            else:
                # 嵌套if语句
                node.else_branch.accept(self)
    
    def visit_ForLoop(self, node):
        """
        访问For循环节点
        """
        # 创建循环作用域
        loop_scope = Scope("for_loop", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = loop_scope
        
        # 声明循环变量
        # 简化实现，假设迭代对象返回string类型
        loop_var = VariableSymbol(
            node.variable,
            STRING_TYPE,
            mutable=True
        )
        try:
            self.current_scope.declare_symbol(loop_var)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 分析迭代对象
        self._infer_type(node.iterable)
        
        # 分析循环体
        for stmt in node.body:
            stmt.accept(self)
        
        # 恢复作用域
        self.current_scope = old_scope
    
    def visit_WhileLoop(self, node):
        """
        访问While循环节点
        """
        # 分析条件表达式
        condition_type = self._infer_type(node.condition)
        if condition_type != BOOL_TYPE:
            raise SemanticError(
                node.line, node.column,
                f"While condition must be of type bool, got {condition_type}"
            )
        
        # 创建循环作用域
        loop_scope = Scope("while_loop", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = loop_scope
        
        # 分析循环体
        for stmt in node.body:
            stmt.accept(self)
        
        # 恢复作用域
        self.current_scope = old_scope
    
    def visit_LoopStatement(self, node):
        """
        访问Loop语句节点
        """
        # 创建循环作用域
        loop_scope = Scope("loop", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = loop_scope
        
        # 分析循环体
        for stmt in node.body:
            stmt.accept(self)
        
        # 恢复作用域
        self.current_scope = old_scope
    
    def visit_MatchStatement(self, node):
        """
        访问Match语句节点
        """
        # 分析表达式
        expr_type = self._infer_type(node.expression)
        
        # 分析匹配项
        for pattern, case_body in node.cases:
            # 分析case体
            self._infer_type(case_body)
    
    def visit_ReturnStatement(self, node):
        """
        访问Return语句节点
        """
        # 查找包含的函数
        func_symbol = self._find_enclosing_function()
        if not func_symbol:
            raise SemanticError(
                node.line, node.column,
                "Return statement outside of function"
            )
        
        # 分析返回值
        if node.value:
            return_type = self._infer_type(node.value)
            if not self._types_compatible(return_type, func_symbol.return_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Return type mismatch: expected {func_symbol.return_type}, got {return_type}"
                )
    
    def visit_BreakStatement(self, node):
        """
        访问Break语句节点
        """
        # 检查是否在循环中
        if not self._in_loop():
            raise SemanticError(
                node.line, node.column,
                "Break statement outside of loop"
            )
    
    def visit_ContinueStatement(self, node):
        """
        访问Continue语句节点
        """
        # 检查是否在循环中
        if not self._in_loop():
            raise SemanticError(
                node.line, node.column,
                "Continue statement outside of loop"
            )
    
    def visit_DeleteVariable(self, node):
        """
        访问DeleteVariable节点
        """
        # 检查变量是否存在
        if not self.current_scope.has_symbol(node.name):
            raise SemanticError(
                node.line, node.column,
                f"Variable '{node.name}' not defined"
            )
        
        # 从当前作用域中删除变量
        self.current_scope.remove_symbol(node.name)
    
    def visit_StructDefinition(self, node):
        """
        访问结构体定义节点
        """
        fields = []
        for field_name, field_type in node.fields:
            field_type_obj = self._resolve_type(field_type)
            fields.append((field_name, field_type_obj))
        
        # 收集方法信息
        methods = []
        for method in node.methods:
            # 解析方法签名
            method_name = method.name
            params = method.params
            return_type = method.return_type
            if return_type:
                return_type_obj = self._resolve_type(return_type)
            else:
                return_type_obj = None
            methods.append((method_name, params, return_type_obj))
            # 分析方法体
            method.accept(self)
        
        struct_type = StructType(node.name, fields)
        struct_type.methods = methods
        self.types[node.name] = struct_type
        
        type_symbol = TypeSymbol(node.name, struct_type, members=fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
    
    def visit_GenericStructDefinition(self, node):
        """
        访问泛型结构体定义节点
        """
        generic_scope = Scope(f"generic_{node.name}", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = generic_scope
        
        type_param_map = {}
        for type_param in node.type_params:
            generic_type = GenericType(type_param.name)
            self.types[type_param.name] = generic_type
            type_param_map[type_param.name] = generic_type
            
            type_symbol = TypeSymbol(type_param.name, generic_type)
            try:
                self.current_scope.declare_symbol(type_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        fields = []
        for field_name, field_type in node.fields:
            field_type_obj = self._resolve_type(field_type)
            fields.append((field_name, field_type_obj))
        
        struct_type = StructType(node.name, fields)
        struct_type.is_value_type = True
        struct_type.type_params = node.type_params
        
        # 收集方法信息
        methods = []
        self.current_scope = old_scope
        
        for method in node.methods:
            method_scope = Scope(method.name, parent=self.current_scope)
            old_method_scope = self.current_scope
            self.current_scope = method_scope
            
            if method.params and method.params[0].name == "self":
                self_symbol = VariableSymbol("self", struct_type)
                try:
                    self.current_scope.declare_symbol(self_symbol)
                except ValueError as e:
                    raise SemanticError(method.line, method.column, str(e))
            
            # 解析方法签名
            method_name = method.name
            params = method.params
            return_type = method.return_type
            if return_type:
                # 重新进入泛型作用域解析返回类型
                temp_scope = self.current_scope
                self.current_scope = generic_scope
                return_type_obj = self._resolve_type(return_type)
                self.current_scope = temp_scope
            else:
                return_type_obj = None
            methods.append((method_name, params, return_type_obj))
            
            # 分析方法体
            method.accept(self)
            
            self.current_scope = old_method_scope
        
        struct_type.methods = methods
        self.types[node.name] = struct_type
        
        type_symbol = TypeSymbol(node.name, struct_type, members=fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
    
    def visit_ClassDefinition(self, node):
        """
        访问类定义节点
        """
        # 解析字段类型（包括访问修饰符）
        fields = []
        for field_name, field_type, access_modifier in node.fields:
            field_type_obj = self._resolve_type(field_type)
            fields.append((field_name, field_type_obj, access_modifier))
        
        # 创建类类型
        class_type = StructType(node.name, fields)
        self.types[node.name] = class_type
        
        # 创建类型符号（先不设置方法，等分析方法后再设置）
        type_symbol = TypeSymbol(node.name, class_type, members=fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 创建类作用域
        class_scope = Scope(f"class_{node.name}", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = class_scope
        
        # 在类作用域中也声明类型符号
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError:
            pass  # 忽略已存在的符号错误
        
        # 分析方法（包括访问修饰符）
        methods = []
        for method, access_modifier in node.methods:
            method.accept(self)
            # 将方法信息添加到类型符号中
            methods.append((method.name, method.params, method.return_type, access_modifier))
        
        # 将方法添加到类型符号中
        type_symbol.methods = methods
        
        # 恢复作用域
        self.current_scope = old_scope
    
    def visit_GenericStructDefinition(self, node):
        """
        访问泛型结构体定义节点
        """
        # 创建泛型结构体作用域
        generic_scope = Scope(f"generic_{node.name}", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = generic_scope
        
        # 声明泛型类型参数
        type_param_map = {}
        for type_param in node.type_params:
            # 创建泛型类型
            generic_type = GenericType(type_param.name)
            self.types[type_param.name] = generic_type
            type_param_map[type_param.name] = generic_type
            
            # 创建类型符号
            type_symbol = TypeSymbol(type_param.name, generic_type)
            try:
                self.current_scope.declare_symbol(type_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        # 创建泛型结构体类型
        struct_type = GenericStructType(node.name, type_params=node.type_params, fields=node.fields)
        self.types[node.name] = struct_type
        
        # 恢复作用域
        self.current_scope = old_scope
        
        # 在全局作用域中声明类型符号
        type_symbol = TypeSymbol(node.name, struct_type, members=node.fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 分析泛型结构体方法
        for method in node.methods:
            # 创建方法作用域
            method_scope = Scope(method.name, parent=self.current_scope)
            old_scope = self.current_scope
            self.current_scope = method_scope
            
            # 为方法添加self参数
            if method.params and method.params[0].name == "self":
                # 为self参数创建符号
                self_symbol = VariableSymbol("self", struct_type)
                try:
                    self.current_scope.declare_symbol(self_symbol)
                except ValueError as e:
                    raise SemanticError(method.line, method.column, str(e))
            
            # 为方法添加结构体名称
            struct_name_symbol = TypeSymbol(node.name, struct_type)
            try:
                self.current_scope.declare_symbol(struct_name_symbol)
            except ValueError as e:
                # 忽略已存在的符号错误
                pass
            
            # 分析方法
            method.accept(self)
            
            # 恢复作用域
            self.current_scope = old_scope
    
    def visit_GenericClassDefinition(self, node):
        """
        访问泛型类定义节点
        """
        # 创建泛型类作用域
        generic_scope = Scope(f"generic_{node.name}", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = generic_scope
        
        # 声明泛型类型参数
        type_param_map = {}
        for type_param in node.type_params:
            # 创建泛型类型
            generic_type = GenericType(type_param.name)
            self.types[type_param.name] = generic_type
            type_param_map[type_param.name] = generic_type
            
            # 创建类型符号
            type_symbol = TypeSymbol(type_param.name, generic_type)
            try:
                self.current_scope.declare_symbol(type_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        # 解析字段类型
        resolved_fields = []
        for field in node.fields:
            if isinstance(field, tuple):
                if len(field) == 3:
                    # 字段格式: (name, type, access_modifier)
                    field_name, field_type, access_modifier = field
                    resolved_type = self._resolve_type(field_type)
                    resolved_fields.append((field_name, resolved_type, access_modifier))
                elif len(field) == 2:
                    # 字段格式: (name, type)
                    field_name, field_type = field
                    resolved_type = self._resolve_type(field_type)
                    resolved_fields.append((field_name, resolved_type))
                else:
                    # 其他格式，直接添加
                    resolved_fields.append(field)
            else:
                resolved_fields.append(field)
        
        # 创建泛型类类型
        class_type = StructType(node.name, resolved_fields)
        self.types[node.name] = class_type
        
        # 恢复作用域
        self.current_scope = old_scope
        
        # 在全局作用域中声明类型符号
        type_symbol = TypeSymbol(node.name, class_type, members=resolved_fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 分析泛型类方法（包括访问修饰符）
        for method, access_modifier in node.methods:
            # 创建方法作用域
            method_scope = Scope(method.name, parent=self.current_scope)
            old_method_scope = self.current_scope
            self.current_scope = method_scope
            
            # 为方法添加self/this参数
            if method.params and len(method.params) > 0 and method.params[0].name in ("self", "this"):
                # 为self/this参数创建符号
                self_symbol = VariableSymbol(method.params[0].name, class_type)
                try:
                    self.current_scope.declare_symbol(self_symbol)
                except ValueError as e:
                    raise SemanticError(method.line, method.column, str(e))
            else:
                # 自动添加this参数
                this_symbol = VariableSymbol("this", class_type)
                try:
                    self.current_scope.declare_symbol(this_symbol)
                except ValueError as e:
                    raise SemanticError(method.line, method.column, str(e))
            
            # 为方法添加类名称
            class_name_symbol = TypeSymbol(node.name, class_type)
            try:
                self.current_scope.declare_symbol(class_name_symbol)
            except ValueError as e:
                # 忽略已存在的符号错误
                pass
            
            # 分析方法
            method.accept(self)
            
            # 恢复作用域
            self.current_scope = old_method_scope
    
    def visit_EnumDefinition(self, node):
        """
        访问枚举定义节点
        """
        # 创建枚举类型
        enum_type = EnumType(node.name, variants=node.variants)
        self.types[node.name] = enum_type
        
        # 创建类型符号
        type_symbol = TypeSymbol(node.name, enum_type, members=node.variants)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
    
    def visit_TraitDefinition(self, node):
        """
        访问Trait定义节点
        """
        # 创建泛型作用域
        generic_scope = None
        type_param_map = {}
        
        if node.type_params:
            # 创建泛型作用域
            generic_scope = Scope(f"generic_{node.name}", parent=self.current_scope)
            old_scope = self.current_scope
            self.current_scope = generic_scope
            
            # 声明泛型类型参数
            for type_param in node.type_params:
                # 创建泛型类型
                generic_type = GenericType(type_param.name)
                self.types[type_param.name] = generic_type
                type_param_map[type_param.name] = generic_type
                
                # 创建类型符号
                type_symbol = TypeSymbol(type_param.name, generic_type)
                try:
                    self.current_scope.declare_symbol(type_symbol)
                except ValueError as e:
                    raise SemanticError(node.line, node.column, str(e))
        
        # 创建Trait类型
        trait_type = TraitType(node.name, methods=node.methods, type_params=node.type_params)
        self.types[node.name] = trait_type
        
        # 创建类型符号
        type_symbol = TypeSymbol(node.name, trait_type, members=node.methods)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 恢复作用域
        if generic_scope:
            self.current_scope = old_scope
    
    def visit_ImplBlock(self, node):
        """
        访问Impl块节点
        """
        # 创建泛型作用域
        generic_scope = None
        type_param_map = {}
        
        if node.type_params:
            # 创建泛型作用域
            generic_scope = Scope(f"generic_impl_{node.type_name}", parent=self.current_scope)
            old_scope = self.current_scope
            self.current_scope = generic_scope
            
            # 声明泛型类型参数
            for type_param in node.type_params:
                # 创建泛型类型
                generic_type = GenericType(type_param.name)
                self.types[type_param.name] = generic_type
                type_param_map[type_param.name] = generic_type
                
                # 创建类型符号
                type_symbol = TypeSymbol(type_param.name, generic_type)
                try:
                    self.current_scope.declare_symbol(type_symbol)
                except ValueError as e:
                    raise SemanticError(node.line, node.column, str(e))
        
        # 解析类型
        # 检查 type_name 是否是类型表达式对象
        print(f"DEBUG visit_ImplBlock: node.type_name = {node.type_name}")
        print(f"DEBUG visit_ImplBlock: node.type_name type = {type(node.type_name)}")
        print(f"DEBUG visit_ImplBlock: hasattr(node.type_name, 'accept') = {hasattr(node.type_name, 'accept')}")
        
        if hasattr(node.type_name, 'accept'):
            # 是类型表达式对象，使用 accept 方法解析
            print(f"DEBUG: calling node.type_name.accept(self)")
            type_obj = node.type_name.accept(self)
            print(f"DEBUG: type_obj after accept = {type_obj}")
            print(f"DEBUG: type_obj type after accept = {type(type_obj)}")
        else:
            # 是字符串，使用 _resolve_type 解析
            print(f"DEBUG: calling self._resolve_type(node.type_name)")
            type_obj = self._resolve_type(node.type_name)
            print(f"DEBUG: type_obj after _resolve_type = {type_obj}")
        
        # 调试信息
        print(f"DEBUG: node.type_name = {node.type_name}")
        print(f"DEBUG: type_obj = {type_obj}")
        print(f"DEBUG: type_obj type = {type(type_obj)}")
        
        # 获取类型名称字符串
        if isinstance(node.type_name, str):
            # 如果 node.type_name 是字符串，直接使用它
            type_name_str = node.type_name
        elif hasattr(type_obj, 'name'):
            type_name_str = type_obj.name
            # 如果是泛型实例类型，获取基础类型的名称
            if isinstance(type_obj, GenericInstanceType) and hasattr(type_obj.base_type, 'name'):
                type_name_str = type_obj.base_type.name
        else:
            # 尝试从 node.type_name 获取名称
            if hasattr(node.type_name, 'name'):
                type_name_str = node.type_name.name
            else:
                type_name_str = str(node.type_name)
        
        print(f"DEBUG: type_name_str = {type_name_str}")
        
        # 如果是为Trait实现方法，记录类型实现的Trait
        if node.trait_name:
            # 检查 trait_name 是否是类型表达式对象
            if hasattr(node.trait_name, 'accept'):
                # 是类型表达式对象，使用 accept 方法解析
                trait_type = node.trait_name.accept(self)
            else:
                # 是字符串，使用 _resolve_type 解析
                trait_type = self._resolve_type(node.trait_name)
            
            # 检查 trait_type 是否是有效的类型
            if trait_type is None:
                # 对于泛型 Trait，暂时跳过类型检查
                # 因为泛型 Trait 可能还没有完全解析
                pass
            elif isinstance(trait_type, TraitType):
                # 记录类型实现的Trait
                if type_name_str not in self.type_traits:
                    self.type_traits[type_name_str] = []
                if trait_type not in self.type_traits[type_name_str]:
                    self.type_traits[type_name_str].append(trait_type)
                
                # 检查实现的方法是否符合Trait要求
                self._check_trait_implementation(node, trait_type)
        
        # 分析方法
        # 设置当前正在分析 Impl 块的标志
        old_impl_context = getattr(self, 'current_impl_type', None)
        setattr(self, 'current_impl_type', type_name_str)
        
        try:
            for method in node.methods:
                # 为方法创建作用域
                method_scope = Scope(method.name, parent=self.current_scope)
                old_method_scope = self.current_scope
                self.current_scope = method_scope
                
                try:
                    # 为方法添加self参数
                    # 获取类型对象
                    if type_name_str in self.types:
                        impl_type = self.types[type_name_str]
                        # 创建self符号
                        self_symbol = VariableSymbol("self", impl_type)
                        try:
                            self.current_scope.declare_symbol(self_symbol)
                        except ValueError as e:
                            # 忽略已存在的符号错误
                            pass
                    
                    # 检查方法是否已经有self参数
                    has_self_param = False
                    for param in method.params:
                        if hasattr(param, 'name') and param.name == 'self':
                            has_self_param = True
                            break
                    
                    # 如果方法没有self参数，添加一个
                    if not has_self_param and type_name_str in self.types:
                        # 创建self参数
                        from nova.compiler.parser.ast import ParameterDefinition
                        self_param = ParameterDefinition(method.line, method.column, 'self', type_name_str)
                        method.params.insert(0, self_param)
                    
                    # 先将方法注册到类型的字段中，再分析方法体
                    if type_name_str in self.types:
                        impl_type = self.types[type_name_str]
                        if hasattr(impl_type, 'fields'):
                            # 解析方法的返回类型和参数类型
                            method_return_type = self._resolve_type(method.return_type) if method.return_type else UNIT_TYPE
                            method_param_types = []
                            for param in method.params:
                                if hasattr(param, 'param_type'):
                                    param_type = self._resolve_type(param.param_type)
                                    method_param_types.append(param_type)
                                elif isinstance(param, tuple) and len(param) >= 2:
                                    param_type = self._resolve_type(param[1])
                                    method_param_types.append(param_type)
                            
                            # 创建函数类型
                            method_type = FunctionType(method_param_types, method_return_type)
                            
                            # 检查方法是否已经存在于字段列表中
                            method_exists = False
                            for field in impl_type.fields:
                                if isinstance(field, tuple) and len(field) >= 2:
                                    field_name = field[0]
                                    if field_name == method.name:
                                        method_exists = True
                                        break
                            
                            # 如果方法不存在，将其添加到类型的字段中
                            if not method_exists:
                                impl_type.fields.append((method.name, method_type))
                    
                    # 分析方法体
                    method.accept(self)
                finally:
                    # 恢复方法作用域
                    self.current_scope = old_method_scope
        finally:
            # 恢复之前的 Impl 上下文
            setattr(self, 'current_impl_type', old_impl_context)
        
        # 恢复作用域
        if generic_scope:
            self.current_scope = old_scope
    
    def visit_BinaryExpression(self, node):
        """
        访问二元表达式节点
        """
        # 分析左右操作数
        left_type = self._infer_type(node.left)
        right_type = self._infer_type(node.right)
        
        # 特殊处理赋值操作
        if node.operator == "=":
            # 检查左侧是否是标识符
            if isinstance(node.left, IdentifierExpression):
                # 查找变量符号
                var_symbol = self.current_scope.resolve_symbol(node.left.name)
                if var_symbol and isinstance(var_symbol, VariableSymbol):
                    # 检查变量是否为常量（不可变）
                    if not var_symbol.mutable:
                        raise SemanticError(
                            node.line, node.column,
                            f"Cannot assign to constant '{node.left.name}'"
                        )
            
            # 对于赋值操作，检查右操作数的类型是否与左操作数的类型兼容
            if not self._types_compatible(right_type, left_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Type mismatch in assignment: expected {left_type}, got {right_type}"
                )
            # 赋值操作返回unit类型
            return UNIT_TYPE
        else:
            # 对于其他二元操作，检查类型兼容性
            if not self._types_compatible(left_type, right_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Type mismatch in binary expression: {left_type} and {right_type}"
                )
            
            # 对于比较操作，返回布尔类型
            if node.operator in ("==", "!=", "<", ">", "<=", ">="):
                return BOOL_TYPE
            
            # 对于其他二元操作，返回左侧类型
            return left_type
    
    def visit_UnaryExpression(self, node):
        """
        访问一元表达式节点
        """
        # 分析操作数
        operand_type = self._infer_type(node.operand)
        
        # 简化实现，返回操作数类型
        return operand_type
    
    def visit_AddressOfExpression(self, node):
        """
        访问取地址表达式节点 (&x)
        """
        # 分析操作数类型
        operand_type = self._infer_type(node.operand)
        
        # 返回指针类型
        return PointerType(operand_type, node.is_mutable)
    
    def visit_DereferenceExpression(self, node):
        """
        访问解引用表达式节点 (*ptr)
        """
        # 分析操作数类型
        operand_type = self._infer_type(node.operand)
        
        # 检查是否是指针类型
        if isinstance(operand_type, PointerType):
            return operand_type.pointee_type
        else:
            raise SemanticError(
                node.line, node.column,
                f"Cannot dereference non-pointer type: {operand_type}"
            )
    
    def visit_TypeTypeExpression(self, node):
        """
        访问类型类型表达式节点 (type: T)
        """
        # 如果有包装类型，解析它
        if node.wrapped_type:
            wrapped_type = self._resolve_type(node.wrapped_type)
            return TypeType(wrapped_type)
        else:
            # 没有指定类型，返回通用的type类型
            return TypeType(ANY_TYPE)
    
    def visit_LiteralExpression(self, node):
        """
        访问字面量表达式节点
        """
        # 根据字面量类型返回对应的类型对象
        literal_type = node.literal_type
        if literal_type == "integer":
            return INT_TYPE
        elif literal_type == "float":
            return FLOAT_TYPE
        elif literal_type == "string":
            return STRING_TYPE
        elif literal_type == "boolean":
            return BOOL_TYPE
        elif literal_type == "character":
            return CHAR_TYPE
        else:
            return UNIT_TYPE
    
    def visit_ArrayLiteralExpression(self, node):
        """
        访问数组字面量表达式节点
        """
        # 分析数组元素并推断元素类型
        if not node.elements:
            # 空数组，返回 any 类型的数组
            return ArrayType(ANY_TYPE)
        
        # 推断第一个元素的类型作为数组元素类型
        element_type = self._infer_type(node.elements[0])
        
        # 检查所有元素类型是否一致
        for i, element in enumerate(node.elements[1:], 1):
            elem_type = self._infer_type(element)
            if not self._types_compatible(elem_type, element_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Array element type mismatch at index {i}: expected {element_type}, got {elem_type}"
                )
        
        # 返回数组类型
        return ArrayType(element_type)
    
    def visit_TupleLiteralExpression(self, node):
        """
        访问元组字面量表达式节点
        """
        # 分析元组元素并推断元素类型
        element_types = []
        for element in node.elements:
            element_types.append(self._infer_type(element))
        
        # 返回元组类型
        return TupleType(element_types)
    
    def visit_IdentifierExpression(self, node):
        """
        访问标识符表达式节点
        """
        # 特殊处理self标识符
        if node.name == "self":
            # 直接从当前作用域中查找self参数
            if node.name in self.current_scope.symbols:
                return self.current_scope.symbols[node.name].type
            else:
                # 尝试从父作用域中查找
                scope = self.current_scope.parent
                while scope:
                    if node.name in scope.symbols:
                        return scope.symbols[node.name].type
                    scope = scope.parent
                # 如果仍然找不到，抛出错误
                raise SemanticError(
                    node.line, node.column,
                    f"Undefined identifier 'self'"
                )
        
        # 特殊处理this标识符（与self相同）
        if node.name == "this":
            # 直接从当前作用域中查找this参数
            if node.name in self.current_scope.symbols:
                return self.current_scope.symbols[node.name].type
            else:
                # 尝试从父作用域中查找
                scope = self.current_scope.parent
                while scope:
                    if node.name in scope.symbols:
                        return scope.symbols[node.name].type
                    scope = scope.parent
                # 如果仍然找不到，抛出错误
                raise SemanticError(
                    node.line, node.column,
                    f"Undefined identifier 'this'"
                )
        
        # 特殊处理super标识符
        if node.name == "super":
            # super是一个特殊标识符，用于访问父类
            # 返回一个特殊的super类型
            return ANY_TYPE
        
        # 解析普通符号
        symbol = self.current_scope.resolve_symbol(node.name)
        if not symbol:
            # 尝试从types中查找类型
            if node.name in self.types:
                return self.types[node.name]
            else:
                # 尝试从父作用域中查找
                scope = self.current_scope.parent
                while scope:
                    if scope.has_symbol(node.name):
                        return scope.resolve_symbol(node.name).type
                    scope = scope.parent
                # 如果仍然找不到，抛出错误
                raise SemanticError(
                    node.line, node.column,
                    f"Undefined identifier '{node.name}'"
                )
        
        # 返回符号类型
        if hasattr(symbol, 'type'):
            return symbol.type
        elif hasattr(symbol, 'return_type'):
            return symbol.return_type
        else:
            return UNIT_TYPE
    
    def visit_ArrayTypeExpression(self, node):
        """
        访问数组类型表达式节点
        """
        # 分析元素类型
        element_type = self._infer_type(node.element_type)
        # 返回数组类型
        return ArrayType(element_type)
    
    def visit_TypeExpression(self, node):
        """
        访问类型表达式节点
        """
        # 返回对应的类型对象
        if node.name in self.types:
            return self.types[node.name]
        else:
            # 尝试从当前作用域中解析类型
            symbol = self.current_scope.resolve_symbol(node.name)
            if symbol and isinstance(symbol, TypeSymbol):
                return symbol.type
            # 如果类型不存在，检查是否是基本类型
            if node.name == "bool":
                return BOOL_TYPE
            elif node.name == "int":
                return INT_TYPE
            elif node.name == "float":
                return FLOAT_TYPE
            elif node.name == "string":
                return STRING_TYPE
            elif node.name == "unit":
                return UNIT_TYPE
            # 如果类型不存在，返回一个新的类型对象
            return PrimitiveType(node.name)
    
    def visit_GenericTypeExpression(self, node):
        """
        访问泛型类型表达式节点
        """
        print(f"DEBUG visit_GenericTypeExpression: node.base_type = {node.base_type}")
        print(f"DEBUG visit_GenericTypeExpression: node.base_type type = {type(node.base_type)}")
        
        # 处理base_type是类型表达式对象的情况
        base_type_name = node.base_type
        if hasattr(base_type_name, 'name'):
            print(f"DEBUG: base_type_name has 'name' attribute: {base_type_name.name}")
            base_type_name = base_type_name.name
        elif hasattr(base_type_name, 'accept'):
            # 是类型表达式对象，使用 accept 方法解析
            print(f"DEBUG: base_type_name has 'accept' attribute")
            base_type_name = base_type_name.accept(self)
            # 如果解析结果是类型对象，使用其名称
            if hasattr(base_type_name, 'name'):
                print(f"DEBUG: resolved base_type_name has 'name' attribute: {base_type_name.name}")
                base_type_name = base_type_name.name
        
        print(f"DEBUG: base_type_name after processing = {base_type_name}")
        print(f"DEBUG: base_type_name type after processing = {type(base_type_name)}")
        
        # 确保base_type_name是字符串
        if not isinstance(base_type_name, str):
            # 如果不是字符串，尝试获取其名称
            if hasattr(base_type_name, 'name'):
                print(f"DEBUG: base_type_name is not string, but has 'name': {base_type_name.name}")
                base_type_name = base_type_name.name
            else:
                # 否则，返回一个新的泛型类型对象
                print(f"DEBUG: base_type_name is not string and has no 'name', converting to string")
                return GenericType(str(base_type_name))
        
        print(f"DEBUG: final base_type_name = {base_type_name}")
        print(f"DEBUG: checking if '{base_type_name}' in self.types: {base_type_name in self.types}")
        if base_type_name in self.types:
            print(f"DEBUG: found {base_type_name} in self.types: {self.types[base_type_name]}")
        
        # 尝试解析泛型结构体符号
        symbol = self.current_scope.resolve_symbol(base_type_name)
        if symbol and isinstance(symbol, TypeSymbol):
            # 检查是否是 Trait 类型
            if isinstance(symbol.type, TraitType):
                # 对于泛型 Trait，返回 Trait 类型本身
                # 简化实现，不处理泛型 Trait 的类型参数
                return symbol.type
            else:
                # 解析类型参数
                type_args = []
                for type_arg in node.type_args:
                    # 使用 _resolve_type 解析类型参数
                    if hasattr(type_arg, 'accept'):
                        type_args.append(type_arg.accept(self))
                    else:
                        type_args.append(self._resolve_type(type_arg))
                
                # 创建泛型实例类型
                return GenericInstanceType(symbol.type, type_args)
        
        # 如果符号不存在，检查是否在 types 中
        if base_type_name in self.types:
            base_type = self.types[base_type_name]
            print(f"DEBUG: base_type = {base_type}")
            print(f"DEBUG: base_type type = {type(base_type)}")
            # 检查是否是 Trait 类型
            if isinstance(base_type, TraitType):
                # 对于泛型 Trait，返回 Trait 类型本身
                print(f"DEBUG: base_type is TraitType, returning base_type")
                return base_type
            else:
                # 解析类型参数
                type_args = []
                for type_arg in node.type_args:
                    # 使用 _resolve_type 解析类型参数
                    if hasattr(type_arg, 'accept'):
                        type_args.append(type_arg.accept(self))
                    else:
                        type_args.append(self._resolve_type(type_arg))
                
                # 创建泛型实例类型
                result = GenericInstanceType(base_type, type_args)
                print(f"DEBUG: returning GenericInstanceType: {result}")
                return result
        
        # 如果符号不存在，返回一个新的泛型类型对象
        # 简化实现，返回泛型类型
        # 确保 base_type_name 是字符串
        if not isinstance(base_type_name, str):
            # 如果不是字符串，尝试获取其名称
            if hasattr(base_type_name, 'name'):
                base_type_name = base_type_name.name
            else:
                # 否则，转换为字符串
                base_type_name = str(base_type_name)
        return GenericType(base_type_name)
    
    def visit_CallExpression(self, node):
        """
        访问调用表达式节点
        """
        # 分析被调用对象
        callee_type = self._infer_type(node.callee)
        
        # 处理标识符调用（函数调用）
        if isinstance(node.callee, IdentifierExpression):
            # 尝试解析函数符号
            symbol = self.current_scope.resolve_symbol(node.callee.name)
            
            # 调试信息
            print(f"DEBUG visit_CallExpression: node.callee.name = {node.callee.name}")
            print(f"DEBUG visit_CallExpression: symbol = {symbol}")
            if symbol:
                print(f"DEBUG visit_CallExpression: symbol.type = {getattr(symbol, 'type', None)}")
                print(f"DEBUG visit_CallExpression: symbol.params = {getattr(symbol, 'params', None)}")
            
            # 检查是否是内置函数，如果是，优先使用内置函数的参数类型
            if node.callee.name in ["print", "println", "str", "len"]:
                # 内置函数，直接使用内置函数的参数类型
                if node.callee.name == "str":
                    # str函数可以接受任何类型的参数
                    return STRING_TYPE
                elif node.callee.name == "print":
                    return UNIT_TYPE
                elif node.callee.name == "println":
                    return UNIT_TYPE
                elif node.callee.name == "len":
                    return INT_TYPE
            
            # 如果从作用域中找不到符号，尝试从types中查找类型
            if not symbol and node.callee.name in self.types:
                # 创建一个临时的TypeSymbol对象
                symbol = TypeSymbol(node.callee.name, self.types[node.callee.name])
            
            # 处理结构体和泛型类实例化
            if symbol and hasattr(symbol, 'type') and isinstance(symbol.type, StructType):
                struct_type = symbol.type
                
                # 检查是否是泛型类（有类型参数）
                is_generic = False
                generic_params = []
                
                # 检查字段类型是否包含泛型类型
                for field in struct_type.fields:
                    if isinstance(field, tuple):
                        if len(field) >= 2:
                            field_type = field[1]
                            if hasattr(field_type, 'name') and field_type.name in self.types:
                                field_type_obj = self.types[field_type.name]
                                if hasattr(field_type_obj, 'name') and field_type_obj.name == field_type.name:
                                    generic_params.append(field_type.name)
                                    is_generic = True
                
                if is_generic:
                    # 泛型类实例化：从参数类型推断类型参数
                    type_args = []
                    for i, arg in enumerate(node.arguments):
                        arg_type = self._infer_type(arg)
                        type_args.append(arg_type)
                    
                    # 创建泛型实例类型
                    generic_instance_type = GenericInstanceType(struct_type, type_args)
                    
                    # 检查参数类型兼容性
                    for i, arg in enumerate(node.arguments):
                        arg_type = self._infer_type(arg)
                        
                        # 获取字段类型
                        if i < len(struct_type.fields):
                            field = struct_type.fields[i]
                            if isinstance(field, tuple):
                                field_name = field[0]
                                # 使用推断的类型参数
                                if i < len(type_args):
                                    expected_type = type_args[i]
                                else:
                                    if len(field) >= 2:
                                        expected_type = field[1]
                                    else:
                                        expected_type = None
                            else:
                                field_name = field
                                expected_type = None
                            
                            # 检查参数类型兼容性
                            if expected_type and not self._types_compatible(arg_type, expected_type):
                                raise SemanticError(
                                    node.line, node.column,
                                    f"Field '{field_name}' type mismatch: expected {expected_type}, got {arg_type}"
                                )
                    
                    # 返回泛型实例类型
                    return generic_instance_type
                else:
                    # 普通结构体实例化
                    # 检查结构体实例化的参数类型
                    for i, arg in enumerate(node.arguments):
                        arg_type = self._infer_type(arg)
                        
                        # 获取字段类型
                        if i < len(struct_type.fields):
                            field = struct_type.fields[i]
                            if isinstance(field, tuple):
                                field_name = field[0]
                                if len(field) >= 2:
                                    field_type = field[1]
                                else:
                                    field_type = None
                            else:
                                field_name = field
                                field_type = None
                            
                            # 检查参数类型兼容性
                            if field_type and not self._types_compatible(arg_type, field_type):
                                raise SemanticError(
                                    node.line, node.column,
                                    f"Field '{field_name}' type mismatch: expected {field_type}, got {arg_type}"
                                )
                    
                    # 返回结构体类型
                    return struct_type
            
            # 如果是函数符号，检查参数类型
            elif symbol and hasattr(symbol, 'params'):
                # 分析参数并检查类型
                for i, arg in enumerate(node.arguments):
                    arg_type = self._infer_type(arg)
                    
                    # 获取参数类型
                    if hasattr(symbol, 'params'):
                        if i < len(symbol.params):
                            param_info = symbol.params[i]
                            if isinstance(param_info, tuple):
                                param_type = param_info[1]
                            else:
                                param_type = param_info.param_type
                            
                            # 解析参数类型
                            param_type = self._resolve_type(param_type)
                            
                            # 检查参数类型兼容性
                            if not self._types_compatible(arg_type, param_type):
                                raise SemanticError(
                                    node.line, node.column,
                                    f"Parameter type mismatch: expected {param_type}, got {arg_type}"
                                )
                
                # 返回函数的返回类型
                if hasattr(symbol, 'return_type'):
                    return symbol.return_type
                else:
                    return UNIT_TYPE
            
            # 处理函数类型的变量（高阶函数参数）
            if symbol and hasattr(symbol, 'type') and isinstance(symbol.type, FunctionType):
                # 检查参数类型
                func_type = symbol.type
                for i, arg in enumerate(node.arguments):
                    arg_type = self._infer_type(arg)
                    
                    # 获取参数类型
                    if i < len(func_type.param_types):
                        param_type = func_type.param_types[i]
                        
                        # 检查参数类型兼容性
                        if not self._types_compatible(arg_type, param_type):
                            raise SemanticError(
                                node.line, node.column,
                                f"Parameter type mismatch: expected {param_type}, got {arg_type}"
                            )
                
                # 返回函数的返回类型
                return func_type.return_type
            
            # 处理内置函数
            if node.callee.name == "str":
                # str函数可以接受任何类型的参数
                return STRING_TYPE
            elif node.callee.name == "print":
                return UNIT_TYPE
            elif node.callee.name == "len":
                return INT_TYPE
        
        # 处理泛型类型实例化（如 Pair<T, U>(...)）
        if isinstance(node.callee, GenericTypeExpression):
            # 检查是否需要类型推断
            if not node.callee.type_args:
                # 需要类型推断
                symbol = self.current_scope.resolve_symbol(node.callee.base_type)
                if symbol:
                    # 检查是否是泛型结构体
                    if isinstance(symbol, TypeSymbol) and hasattr(symbol.type, 'type_params'):
                        # 泛型结构体，尝试从参数推断类型
                        inferred_type = self._infer_generic_type_from_args(symbol, node)
                        if inferred_type:
                            # 创建泛型实例类型
                            return GenericInstanceType(symbol.type, [inferred_type])
                        else:
                            raise SemanticError(
                                node.callee.line, node.callee.column,
                                f"无法推断类型参数 '{symbol.type.name}'，请使用显式类型指定，如 {symbol.type.name}<int>()"
                            )
                    
                    # 检查是否是泛型函数
                    elif isinstance(symbol, (GenericFunctionSymbol, FunctionSymbol)) and hasattr(symbol, 'type_params') and symbol.type_params:
                        # 泛型函数，尝试从参数推断类型
                        inferred_type = self._infer_generic_type_from_args(symbol, node)
                        if inferred_type:
                            # 返回推断出的类型（函数的返回类型）
                            return inferred_type
                        else:
                            raise SemanticError(
                                node.callee.line, node.callee.column,
                                f"无法推断类型参数 '{symbol.name}'，请使用显式类型指定，如 {symbol.name}<int>()"
                            )
            
            # 返回泛型类型实例化的类型
            return node.callee.accept(self)
        
        # 处理super方法调用
        if isinstance(node.callee, MemberExpression):
            if hasattr(node.callee.object, 'name') and node.callee.object.name == 'super':
                # super方法调用，返回ANY_TYPE
                return ANY_TYPE
            
            # 处理普通方法调用（如 a.add(b)）
            # 获取成员表达式的类型（应该是函数类型）
            member_type = self._infer_type(node.callee)
            
            # 如果成员类型是函数类型，返回函数的返回类型
            if isinstance(member_type, FunctionType):
                # 检查参数类型兼容性
                for i, arg in enumerate(node.arguments):
                    arg_type = self._infer_type(arg)
                    
                    # 获取参数类型
                    if i < len(member_type.param_types):
                        param_type = member_type.param_types[i]
                        
                        # 检查参数类型兼容性
                        if not self._types_compatible(arg_type, param_type):
                            raise SemanticError(
                                node.line, node.column,
                                f"Parameter type mismatch: expected {param_type}, got {arg_type}"
                            )
                
                # 返回函数的返回类型
                return member_type.return_type
        
        # 简化实现，返回unit类型
        return UNIT_TYPE
    
    def visit_NamedArgumentExpression(self, node):
        """
        访问命名参数表达式节点
        """
        # 分析参数值
        return self._infer_type(node.value)
    
    def visit_MemberExpression(self, node):
        """
        访问成员表达式节点
        """
        # 分析对象
        obj_type = self._infer_type(node.object)
        
        # 特殊处理super访问
        if hasattr(node.object, 'name') and node.object.name == 'super':
            # super访问父类的方法，返回ANY_TYPE
            return ANY_TYPE
        
        # 特殊处理数组类型的len方法
        if isinstance(obj_type, ArrayType) and node.member == "len":
            return FunctionType([], INT_TYPE)
        
        # 检查是否是泛型实例类型
        if hasattr(obj_type, 'base_type'):
            # 使用基础类型的fields
            base_type = obj_type.base_type
            fields = base_type.fields if hasattr(base_type, 'fields') else []
            # 获取基础类型的名称
            type_name = base_type.name if hasattr(base_type, 'name') else str(base_type)
        else:
            # 直接使用对象类型的fields
            fields = obj_type.fields if hasattr(obj_type, 'fields') else []
            # 获取对象类型的名称
            type_name = obj_type.name if hasattr(obj_type, 'name') else str(obj_type)
        
        print(f"DEBUG visit_MemberExpression: obj_type = {obj_type}")
        print(f"DEBUG visit_MemberExpression: type_name = {type_name}")
        print(f"DEBUG visit_MemberExpression: node.member = {node.member}")
        print(f"DEBUG visit_MemberExpression: fields = {fields}")
        print(f"DEBUG visit_MemberExpression: type_traits = {self.type_traits}")
        
        # 尝试获取成员的类型
        for field in fields:
            if isinstance(field, tuple):
                if len(field) >= 2:
                    field_name = field[0]
                    field_type = field[1]
                else:
                    field_name = field[0]
                    field_type = None
            else:
                field_name = field
                field_type = None
            
            if field_name == node.member:
                print(f"DEBUG visit_MemberExpression: found field {field_name} with type {field_type}")
                # 如果 field_type 是类型表达式对象，解析它
                if field_type and hasattr(field_type, 'accept'):
                    resolved_type = field_type.accept(self)
                    print(f"DEBUG visit_MemberExpression: resolved field type = {resolved_type}")
                    return resolved_type
                return field_type if field_type else obj_type
        
        # 如果没有找到成员，检查类型是否实现了某个Trait
        # 并从Trait中获取方法
        if type_name in self.type_traits:
            print(f"DEBUG visit_MemberExpression: type {type_name} has traits: {self.type_traits[type_name]}")
            for trait_type in self.type_traits[type_name]:
                print(f"DEBUG visit_MemberExpression: checking trait {trait_type}")
                if hasattr(trait_type, 'methods'):
                    print(f"DEBUG visit_MemberExpression: trait has methods: {trait_type.methods}")
                    for method in trait_type.methods:
                        print(f"DEBUG visit_MemberExpression: checking method {method}")
                        # 处理方法可能是元组或对象的情况
                        if isinstance(method, tuple):
                            # 元组格式: (method_name, params, return_type)
                            method_name = method[0] if len(method) > 0 else None
                            return_type = method[2] if len(method) > 2 else None
                        elif hasattr(method, 'name'):
                            method_name = method.name
                            return_type = method.return_type if hasattr(method, 'return_type') else None
                        else:
                            continue
                        
                        if method_name == node.member:
                            # 返回方法的函数类型，而不是返回类型
                            # 这样 visit_CallExpression 可以正确处理方法调用
                            if return_type:
                                print(f"DEBUG visit_MemberExpression: found method {method_name} with return type {return_type}")
                                resolved_return_type = self._resolve_type(return_type)
                                print(f"DEBUG visit_MemberExpression: resolved return type = {resolved_return_type}")
                                # 创建函数类型，从Trait方法中获取参数类型
                                param_types = []
                                if isinstance(method, tuple):
                                    # 元组格式: (method_name, params, return_type)
                                    if len(method) > 1:
                                        params = method[1]
                                        for param in params:
                                            if isinstance(param, tuple):
                                                # 元组格式: (param_name, param_type)
                                                if len(param) > 1:
                                                    param_type = self._resolve_type(param[1])
                                                    param_types.append(param_type)
                                elif hasattr(method, 'params'):
                                    # 方法对象格式
                                    for param in method.params:
                                        if isinstance(param, tuple):
                                            # 元组格式: (param_name, param_type)
                                            if len(param) > 1:
                                                param_type = self._resolve_type(param[1])
                                                param_types.append(param_type)
                                        elif hasattr(param, 'param_type'):
                                            # 参数对象格式
                                            param_type = self._resolve_type(param.param_type)
                                            param_types.append(param_type)
                                return FunctionType(param_types, resolved_return_type)
                            # 如果没有返回类型，返回bool类型的函数类型（默认）
                            print(f"DEBUG visit_MemberExpression: found method {method_name} with no return type, returning FunctionType([], BOOL_TYPE)")
                            return FunctionType([], BOOL_TYPE)
        
        # 如果类型是泛型类型，检查其Trait约束
        if isinstance(obj_type, GenericType) and hasattr(obj_type, 'trait_constraints'):
            print(f"DEBUG visit_MemberExpression: obj_type is GenericType with trait_constraints: {obj_type.trait_constraints}")
            for trait_type in obj_type.trait_constraints:
                print(f"DEBUG visit_MemberExpression: checking trait constraint {trait_type}")
                if hasattr(trait_type, 'methods'):
                    print(f"DEBUG visit_MemberExpression: trait has methods: {trait_type.methods}")
                    for method in trait_type.methods:
                        print(f"DEBUG visit_MemberExpression: checking method {method}")
                        # 处理方法可能是元组或对象的情况
                        if isinstance(method, tuple):
                            # 元组格式: (method_name, params, return_type)
                            method_name = method[0] if len(method) > 0 else None
                            return_type = method[2] if len(method) > 2 else None
                        elif hasattr(method, 'name'):
                            method_name = method.name
                            return_type = method.return_type if hasattr(method, 'return_type') else None
                        else:
                            continue
                        
                        if method_name == node.member:
                            # 返回方法的函数类型，而不是返回类型
                            if return_type:
                                print(f"DEBUG visit_MemberExpression: found method {method_name} with return type {return_type}")
                                resolved_return_type = self._resolve_type(return_type)
                                print(f"DEBUG visit_MemberExpression: resolved return type = {resolved_return_type}")
                                # 创建函数类型，从Trait方法中获取参数类型
                                param_types = []
                                if isinstance(method, tuple):
                                    # 元组格式: (method_name, params, return_type)
                                    if len(method) > 1:
                                        params = method[1]
                                        for param in params:
                                            if isinstance(param, tuple):
                                                # 元组格式: (param_name, param_type)
                                                if len(param) > 1:
                                                    param_type = self._resolve_type(param[1])
                                                    param_types.append(param_type)
                                elif hasattr(method, 'params'):
                                    # 方法对象格式
                                    for param in method.params:
                                        if isinstance(param, tuple):
                                            # 元组格式: (param_name, param_type)
                                            if len(param) > 1:
                                                param_type = self._resolve_type(param[1])
                                                param_types.append(param_type)
                                        elif hasattr(param, 'param_type'):
                                            # 参数对象格式
                                            param_type = self._resolve_type(param.param_type)
                                            param_types.append(param_type)
                                return FunctionType(param_types, resolved_return_type)
                            # 如果没有返回类型，返回bool类型的函数类型（默认）
                            print(f"DEBUG visit_MemberExpression: found method {method_name} with no return type, returning FunctionType([], BOOL_TYPE)")
                            return FunctionType([], BOOL_TYPE)
        
        # 如果类型本身是 Trait 类型，也检查 Trait 本身的方法
        if isinstance(obj_type, TraitType) and hasattr(obj_type, 'methods'):
            print(f"DEBUG visit_MemberExpression: obj_type is TraitType with methods: {obj_type.methods}")
            for method in obj_type.methods:
                print(f"DEBUG visit_MemberExpression: checking method {method}")
                # 处理方法可能是元组或对象的情况
                if isinstance(method, tuple):
                    # 元组格式: (method_name, params, return_type)
                    method_name = method[0] if len(method) > 0 else None
                    return_type = method[2] if len(method) > 2 else None
                elif hasattr(method, 'name'):
                    method_name = method.name
                    return_type = method.return_type if hasattr(method, 'return_type') else None
                else:
                    continue
                
                if method_name == node.member:
                    # 返回方法的函数类型，而不是返回类型
                    if return_type:
                        print(f"DEBUG visit_MemberExpression: found method {method_name} with return type {return_type}")
                        resolved_return_type = self._resolve_type(return_type)
                        print(f"DEBUG visit_MemberExpression: resolved return type = {resolved_return_type}")
                        # 创建函数类型，从Trait方法中获取参数类型
                        param_types = []
                        if isinstance(method, tuple):
                            # 元组格式: (method_name, params, return_type)
                            if len(method) > 1:
                                params = method[1]
                                for param in params:
                                    if isinstance(param, tuple):
                                        # 元组格式: (param_name, param_type)
                                        if len(param) > 1:
                                            param_type = self._resolve_type(param[1])
                                            param_types.append(param_type)
                        elif hasattr(method, 'params'):
                            # 方法对象格式
                            for param in method.params:
                                if isinstance(param, tuple):
                                    # 元组格式: (param_name, param_type)
                                    if len(param) > 1:
                                        param_type = self._resolve_type(param[1])
                                        param_types.append(param_type)
                                elif hasattr(param, 'param_type'):
                                    # 参数对象格式
                                    param_type = self._resolve_type(param.param_type)
                                    param_types.append(param_type)
                        return FunctionType(param_types, resolved_return_type)
                    # 如果没有返回类型，返回bool类型的函数类型（默认）
                    print(f"DEBUG visit_MemberExpression: found method {method_name} with no return type, returning FunctionType([], BOOL_TYPE)")
                    return FunctionType([], BOOL_TYPE)
        
        # 检查类型符号中是否有方法
        type_symbol = self.current_scope.resolve_symbol(type_name)
        if isinstance(type_symbol, TypeSymbol) and hasattr(type_symbol, 'methods'):
            print(f"DEBUG visit_MemberExpression: type {type_name} has methods: {type_symbol.methods}")
            for method in type_symbol.methods:
                print(f"DEBUG visit_MemberExpression: checking method {method}")
                # 处理方法可能是元组或对象的情况
                if isinstance(method, tuple):
                    # 元组格式: (method_name, params, return_type, access_modifier)
                    method_name = method[0] if len(method) > 0 else None
                    params = method[1] if len(method) > 1 else []
                    return_type = method[2] if len(method) > 2 else None
                elif hasattr(method, 'name'):
                    method_name = method.name
                    params = method.params if hasattr(method, 'params') else []
                    return_type = method.return_type if hasattr(method, 'return_type') else None
                else:
                    continue
                
                if method_name == node.member:
                    # 返回方法的函数类型
                    if return_type:
                        print(f"DEBUG visit_MemberExpression: found method {method_name} with return type {return_type}")
                        resolved_return_type = self._resolve_type(return_type)
                        print(f"DEBUG visit_MemberExpression: resolved return type = {resolved_return_type}")
                        # 创建函数类型
                        param_types = []
                        for param in params:
                            if isinstance(param, tuple):
                                # 元组格式: (param_name, param_type)
                                if len(param) > 1:
                                    param_type = self._resolve_type(param[1])
                                    param_types.append(param_type)
                            elif hasattr(param, 'param_type'):
                                # 参数对象格式
                                param_type = self._resolve_type(param.param_type)
                                param_types.append(param_type)
                        return FunctionType(param_types, resolved_return_type)
                    # 如果没有返回类型，返回bool类型的函数类型（默认）
                    print(f"DEBUG visit_MemberExpression: found method {method_name} with no return type, returning FunctionType([], BOOL_TYPE)")
                    return FunctionType([], BOOL_TYPE)
        
        # 没有找到成员，检查当前作用域中是否有同名的函数符号（类方法）
        symbol = self.current_scope.resolve_symbol(node.member)
        if isinstance(symbol, FunctionSymbol):
            print(f"DEBUG visit_MemberExpression: found function symbol {node.member} with return type {symbol.return_type}")
            # 返回函数的函数类型
            param_types = []
            for param_name, param_type in symbol.params:
                resolved_param_type = self._resolve_type(param_type)
                param_types.append(resolved_param_type)
            return_type = symbol.return_type if symbol.return_type else ANY_TYPE
            return FunctionType(param_types, return_type)
        
        # 没有找到成员，返回对象类型
        print(f"DEBUG visit_MemberExpression: member {node.member} not found, returning obj_type {obj_type}")
        return obj_type
    
    def visit_IndexExpression(self, node):
        """
        访问索引表达式节点
        """
        # 分析对象和索引
        obj_type = self._infer_type(node.object)
        index_type = self._infer_type(node.index)
        
        # 检查索引类型
        if index_type != INT_TYPE:
            raise SemanticError(
                node.line, node.column,
                f"Index must be of type int, got {index_type}"
            )
        
        # 简化实现，返回对象类型
        return obj_type
    
    def visit_OptionalChainExpression(self, node):
        """
        访问可选链表达式节点
        """
        # 分析对象
        obj_type = self._infer_type(node.object)
        
        # 简化实现，返回对象类型
        return obj_type
    
    def visit_StringInterpolationExpression(self, node):
        """
        访问字符串插值表达式节点
        """
        # 分析各个部分
        for part_type, part in node.parts:
            if part_type == "expression":
                # 分析表达式部分
                self._infer_type(part)
        
        # 字符串插值表达式返回字符串类型
        return STRING_TYPE
    
    def visit_AwaitExpression(self, node):
        """
        访问await表达式节点
        """
        # 分析await的表达式
        expr_type = self._infer_type(node.expression)
        # 这里可以添加对Future/Task类型的检查
        # 暂时返回表达式的类型，实际应该返回Future/Task中包含的类型
        return expr_type
    
    def visit_DestructuringDeclaration(self, node):
        """
        访问解构声明节点
        """
        # 解析类型
        var_type = None
        if node.var_type:
            var_type = self._resolve_type(node.var_type)
        elif node.value:
            # 从值推断类型
            var_type = self._infer_type(node.value)
        else:
            raise SemanticError(node.line, node.column, "Destructuring declaration requires either a type annotation or an initial value")
        
        # 为解构的变量创建符号
        if node.destructuring_type == "array":
            # 数组解构
            for i, binding in enumerate(node.bindings):
                # 简化实现，假设数组元素类型与数组类型相同
                element_type = var_type  # 实际应该从数组类型中获取元素类型
                var_symbol = VariableSymbol(
                    binding,
                    element_type,
                    mutable=node.mutable
                )
                try:
                    self.current_scope.declare_symbol(var_symbol)
                except ValueError as e:
                    raise SemanticError(node.line, node.column, str(e))
        elif node.destructuring_type == "object":
            # 对象解构
            for binding in node.bindings:
                if isinstance(binding, tuple):
                    # 带别名的对象解构: {name: alias}
                    prop_name, var_name = binding
                else:
                    # 不带别名的对象解构: {name}
                    prop_name = binding
                    var_name = binding
                
                # 简化实现，假设对象属性类型与对象类型相同
                prop_type = var_type  # 实际应该从对象类型中获取属性类型
                var_symbol = VariableSymbol(
                    var_name,
                    prop_type,
                    mutable=node.mutable
                )
                try:
                    self.current_scope.declare_symbol(var_symbol)
                except ValueError as e:
                    raise SemanticError(node.line, node.column, str(e))
        
        # 分析初始化值
        if node.value:
            value_type = self._infer_type(node.value)
            if not self._types_compatible(value_type, var_type):
                raise SemanticError(
                    node.line, node.column,
                    f"Type mismatch: expected {var_type}, got {value_type}"
                )
    
    def visit_LambdaExpression(self, node):
        """
        访问Lambda表达式节点
        """
        # 创建Lambda作用域
        lambda_scope = Scope("lambda", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = lambda_scope
        
        # 声明参数
        for param in node.params:
            if isinstance(param, tuple):
                # 兼容旧格式：元组(name, type)
                param_name, param_type = param
            else:
                # 新格式：ParameterDefinition对象
                param_name = param.name
                param_type = param.param_type
            
            param_type_obj = self._resolve_type(param_type)
            var_symbol = VariableSymbol(param_name, param_type_obj)
            try:
                self.current_scope.declare_symbol(var_symbol)
            except ValueError as e:
                raise SemanticError(node.line, node.column, str(e))
        
        # 分析函数体
        body_type = self._infer_type(node.body)
        
        # 恢复作用域
        self.current_scope = old_scope
        
        return body_type
    
    def _resolve_type(self, type_name):
        """
        解析类型名称为类型对象
        
        Args:
            type_name: 类型名称或类型表达式对象
        
        Returns:
            Type: 类型对象
        
        Raises:
            SemanticError: 如果类型未找到
        """
        # 检查是否是类型表达式对象
        if hasattr(type_name, 'accept'):
            # 是类型表达式对象，使用 accept 方法解析
            result = type_name.accept(self)
            # 如果解析结果是类型对象，直接返回
            if hasattr(result, 'name'):
                return result
            # 否则，尝试获取其名称并重新解析
            elif hasattr(result, '__str__'):
                return self._resolve_type(str(result))
            else:
                # 直接返回结果，可能是一个GenericType对象
                return result
        
        # 检查是否是TypeExpression对象
        if hasattr(type_name, 'name'):
            type_name = type_name.name
        
        # 检查是否是泛型类型表达式
        if hasattr(type_name, 'base_type'):
            return self._resolve_generic_type(type_name)
        
        # 检查是否是数组类型表达式
        if hasattr(type_name, 'element_type'):
            element_type = self._resolve_type(type_name.element_type)
            return ArrayType(element_type)
        
        # 检查是否是元组类型表达式
        if hasattr(type_name, 'element_types'):
            element_types = [self._resolve_type(t) for t in type_name.element_types]
            return TupleType(element_types)
        
        # 检查是否是函数类型表达式
        if hasattr(type_name, 'param_types'):
            param_types = [self._resolve_type(t) for t in type_name.param_types]
            return_type = self._resolve_type(type_name.return_type)
            return FunctionType(param_types, return_type)
        
        # 检查是否是指针类型表达式
        if hasattr(type_name, 'pointee_type'):
            pointee_type = self._resolve_type(type_name.pointee_type)
            is_mutable = hasattr(type_name, 'is_mutable') and type_name.is_mutable
            return PointerType(pointee_type, is_mutable)
        
        # 检查是否是引用类型表达式
        if hasattr(type_name, 'referenced_type'):
            referenced_type = self._resolve_type(type_name.referenced_type)
            is_mutable = hasattr(type_name, 'is_mutable') and type_name.is_mutable
            return ReferenceType(referenced_type, is_mutable)
        
        # 检查是否是类型类型表达式
        if hasattr(type_name, 'wrapped_type'):
            if type_name.wrapped_type is None:
                # 没有指定具体类型，返回通用的type类型
                return TypeType(ANY_TYPE)
            else:
                wrapped_type = self._resolve_type(type_name.wrapped_type)
                return TypeType(wrapped_type)
        
        # 处理auto类型
        if type_name == "auto":
            return ANY_TYPE
        
        # 处理type类型（类型类型）
        if type_name == "type":
            return TypeType(ANY_TYPE)
        
        # 简单类型
        if type_name in self.types:
            return self.types[type_name]
        else:
            # 尝试从作用域中解析
            symbol = self.current_scope.resolve_symbol(type_name)
            if isinstance(symbol, TypeSymbol):
                return symbol.type
            else:
                # 尝试创建一个新的泛型类型对象
                return GenericType(type_name)
    
    def _infer_type(self, expression):
        """
        推断表达式类型
        
        Args:
            expression: 表达式节点
        
        Returns:
            Type: 推断的类型
        """
        return expression.accept(self)
    
    def _types_compatible(self, type1, type2):
        """
        检查类型兼容性
        
        Args:
            type1: 类型1
            type2: 类型2
        
        Returns:
            bool: 类型是否兼容
        """
        # 如果其中一个类型是any类型，那么它应该可以与任何类型兼容
        # 使用 isinstance 检查，因为 ANY_TYPE 是 PrimitiveType 对象
        if (isinstance(type1, PrimitiveType) and type1.name == "any") or \
           (isinstance(type2, PrimitiveType) and type2.name == "any"):
            return True
        
        # 如果其中一个类型是泛型类型参数，那么它应该可以与任何类型兼容
        # 这在泛型函数调用时非常重要
        if isinstance(type1, GenericType) or isinstance(type2, GenericType):
            return True
        
        # 如果两个类型都是TypeType，检查包装类型
        if isinstance(type1, TypeType) and isinstance(type2, TypeType):
            # 如果其中一个包装类型是ANY_TYPE，则兼容
            if type1.wrapped_type == ANY_TYPE or type2.wrapped_type == ANY_TYPE:
                return True
            # 否则检查包装类型是否兼容
            return type1.wrapped_type == type2.wrapped_type
        
        # 如果其中一个是TypeType，另一个不是，不兼容
        if isinstance(type1, TypeType) or isinstance(type2, TypeType):
            return False
        
        # 检查 GenericInstanceType 和 StructType 的兼容性
        # Person<string, int> 和 Person 应该兼容
        if isinstance(type1, GenericInstanceType) and isinstance(type2, StructType):
            return type1.base_type == type2
        if isinstance(type2, GenericInstanceType) and isinstance(type1, StructType):
            return type2.base_type == type1
        # 检查两个 GenericInstanceType 的兼容性
        if isinstance(type1, GenericInstanceType) and isinstance(type2, GenericInstanceType):
            return type1.base_type == type2.base_type
        
        # 检查数组类型兼容性
        if isinstance(type1, ArrayType) and isinstance(type2, ArrayType):
            # 数组类型兼容，如果元素类型兼容
            return self._types_compatible(type1.element_type, type2.element_type)
        
        # 检查元组类型兼容性
        if isinstance(type1, TupleType) and isinstance(type2, TupleType):
            # 元组类型兼容，如果元素类型数量相同且每个元素类型兼容
            if len(type1.element_types) != len(type2.element_types):
                return False
            for t1, t2 in zip(type1.element_types, type2.element_types):
                if not self._types_compatible(t1, t2):
                    return False
            return True
        
        # 检查 Trait 兼容性：如果 type1 实现了 type2（type2 是 Trait）
        if isinstance(type2, TraitType):
            return self._type_implements_trait(type1, type2)
        
        # 检查 Trait 兼容性：如果 type2 实现了 type1（type1 是 Trait）
        if isinstance(type1, TraitType):
            return self._type_implements_trait(type2, type1)
        
        # 严格类型检查：不允许隐式类型转换
        # 只有完全相同的类型才兼容
        return type1 == type2
    
    def _type_implements_trait(self, type_obj, trait_type):
        """
        检查类型是否实现了指定的 Trait
        
        Args:
            type_obj: 类型对象
            trait_type: Trait类型对象
        
        Returns:
            bool: 是否实现了 Trait
        """
        # 获取类型名称
        type_name = str(type_obj)
        
        # 检查类型是否在 type_traits 映射中
        if type_name in self.type_traits:
            # 检查是否实现了指定的 Trait
            for implemented_trait in self.type_traits[type_name]:
                if implemented_trait == trait_type:
                    return True
        
        # 处理泛型实例类型（如 List<int>）
        # 尝试获取基础类型名称
        base_type_name = None
        if hasattr(type_obj, 'base_type'):
            # 泛型实例类型，获取基础类型
            base_type = type_obj.base_type
            base_type_name = base_type.name if hasattr(base_type, 'name') else str(base_type)
        elif '<' in type_name and '>' in type_name:
            # 从类型名称中提取基础类型名称
            base_type_name = type_name.split('<')[0]
        
        # 检查基础类型是否实现了 Trait
        if base_type_name and base_type_name in self.type_traits:
            for implemented_trait in self.type_traits[base_type_name]:
                if implemented_trait == trait_type:
                    return True
        
        # 检查基本类型的默认实现
        # 这里可以添加基本类型的默认 Trait 实现
        
        return False
    
    def _infer_generic_type_from_args(self, symbol, node):
        """
        从参数推断泛型类型参数
        
        Args:
            symbol: 泛型符号（泛型结构体或泛型函数）
            node: 泛型类型表达式节点
        
        Returns:
            Type: 推断出的类型，如果无法推断则返回None
        """
        # 检查是否有参数
        if not node.arguments or not hasattr(node, 'arguments'):
            return None
        
        # 获取第一个参数的类型
        first_arg_type = self._infer_type(node.arguments[0])
        
        # 如果第一个参数是泛型类型，无法推断
        if isinstance(first_arg_type, GenericType):
            return None
        
        # 检查所有参数类型是否一致
        for arg in node.arguments[1:]:
            arg_type = self._infer_type(arg)
            if arg_type != first_arg_type:
                # 类型不一致，无法推断
                return None
        
        # 返回推断出的类型
        return first_arg_type
    
    def _find_enclosing_function(self):
        """
        查找包含的函数
        
        Returns:
            FunctionSymbol: 函数符号，如果不在函数中则返回None
        """
        scope = self.current_scope
        while scope:
            # 检查当前作用域的父作用域中是否有与当前作用域名称相同的函数符号
            if scope.parent:
                # 尝试直接查找函数符号
                symbol = scope.parent.resolve_symbol(scope.name)
                if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                    return symbol
                # 如果当前作用域名称以"generic_"开头，尝试查找去掉前缀后的函数符号
                if scope.name.startswith("generic_"):
                    func_name = scope.name[len("generic_"):]
                    symbol = scope.parent.resolve_symbol(func_name)
                    if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                        return symbol
                # 尝试在当前作用域中查找函数符号
                symbol = scope.resolve_symbol(scope.name)
                if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                    return symbol
                # 尝试在父作用域中查找所有函数符号
                for symbol_name, symbol in scope.parent.symbols.items():
                    if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                        pass
                # 尝试在父作用域的父作用域中查找函数符号
                if scope.parent.parent:
                    symbol = scope.parent.parent.resolve_symbol(scope.name)
                    if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                        return symbol
                    # 如果父作用域的名称以"generic_"开头，尝试查找去掉前缀后的函数符号
                    if scope.parent.name.startswith("generic_"):
                        func_name = scope.parent.name[len("generic_"):]
                        symbol = scope.parent.resolve_symbol(func_name)
                        if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                            return symbol
                        symbol = scope.parent.parent.resolve_symbol(func_name)
                        if isinstance(symbol, (FunctionSymbol, GenericFunctionSymbol)):
                            return symbol
            scope = scope.parent
        return None
    
    def _in_loop(self):
        """
        检查是否在循环中
        
        Returns:
            bool: 是否在循环中
        """
        scope = self.current_scope
        while scope:
            if scope.name in ["for_loop", "while_loop", "loop"]:
                return True
            scope = scope.parent
        return False
    
    def _infer_return_type(self, body):
        """
        推断函数返回类型
        
        Args:
            body: 函数体语句列表
        
        Returns:
            Type: 推断的返回类型，如果没有return语句则返回None
        """
        # 临时作用域，用于记录变量声明
        temp_scope = Scope("temp", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = temp_scope
        
        try:
            for stmt in body:
                # 处理变量声明
                if hasattr(stmt, 'name') and hasattr(stmt, 'var_type'):
                    # 解析变量类型
                    var_type = None
                    if stmt.var_type:
                        var_type = self._resolve_type(stmt.var_type)
                    elif hasattr(stmt, 'value') and stmt.value:
                        # 从值推断类型
                        var_type = self._infer_type(stmt.value)
                    
                    # 创建变量符号
                    if var_type:
                        var_symbol = VariableSymbol(stmt.name, var_type)
                        temp_scope.declare_symbol(var_symbol)
                # 处理return语句
                elif isinstance(stmt, ReturnStatement) and hasattr(stmt, 'value') and stmt.value:
                    return self._infer_type(stmt.value)
        finally:
            # 恢复作用域
            self.current_scope = old_scope
        
        return None
    
    def _check_trait_constraints(self, where_clause, type_param_map):
        """
        检查特质约束
        
        Args:
            where_clause: where子句节点
            type_param_map: 类型参数映射
        
        Raises:
            SemanticError: 如果约束检查失败
        """
        for constraint in where_clause.constraints:
            # 检查类型参数是否存在
            if constraint.type_param not in type_param_map:
                raise SemanticError(
                    constraint.line, constraint.column,
                    f"Unknown type parameter '{constraint.type_param}'"
                )
            
            # 获取类型参数对应的泛型类型
            generic_type = type_param_map[constraint.type_param]
            
            # 检查特质是否存在（支持多个特质约束）
            for trait_name_expr in constraint.trait_names:
                print(f"DEBUG _check_trait_constraints: trait_name_expr = {trait_name_expr}, type = {type(trait_name_expr)}")
                # 检查 trait_name 是否是类型表达式对象
                if hasattr(trait_name_expr, 'accept'):
                    # 是类型表达式对象，使用 accept 方法解析
                    trait_type = trait_name_expr.accept(self)
                    print(f"DEBUG _check_trait_constraints: trait_type = {trait_type}, type = {type(trait_type)}")
                    
                    # 检查是否是 Trait 类型
                    if not isinstance(trait_type, TraitType):
                        # 尝试获取类型名称
                        type_name = getattr(trait_name_expr, 'base_type', str(trait_name_expr))
                        raise SemanticError(
                            constraint.line, constraint.column,
                            f"'{type_name}' is not a trait"
                        )
                    
                    # 将Trait约束信息存储到泛型类型中
                    print(f"DEBUG _check_trait_constraints: adding trait {trait_type} to generic_type {generic_type}")
                    if trait_type not in generic_type.trait_constraints:
                        generic_type.trait_constraints.append(trait_type)
                        print(f"DEBUG _check_trait_constraints: generic_type.trait_constraints = {generic_type.trait_constraints}")
                else:
                    # 是字符串，使用 _resolve_type 解析
                    trait_name = trait_name_expr if isinstance(trait_name_expr, str) else str(trait_name_expr)
                    
                    if trait_name not in self.types:
                        raise SemanticError(
                            constraint.line, constraint.column,
                            f"Unknown trait '{trait_name}'"
                        )
                    
                    # 检查是否是特质类型
                    trait_type = self.types[trait_name]
                    if not isinstance(trait_type, TraitType):
                        raise SemanticError(
                            constraint.line, constraint.column,
                            f"'{trait_name}' is not a trait"
                        )
                    
                    # 将Trait约束信息存储到泛型类型中
                    if trait_type not in generic_type.trait_constraints:
                        generic_type.trait_constraints.append(trait_type)
    
    def _check_trait_implementation(self, impl_block, trait_type):
        """
        检查 Impl 块是否正确实现了 Trait 要求的所有方法
        
        Args:
            impl_block: Impl块节点
            trait_type: Trait类型对象
        
        Raises:
            SemanticError: 如果实现不完整
        """
        # 获取 Trait 中定义的方法
        trait_methods = {}
        for method in trait_type.methods:
            if hasattr(method, 'name'):
                trait_methods[method.name] = method
            elif isinstance(method, tuple) and len(method) > 0:
                # 处理元组形式的方法
                method_name = method[0]
                trait_methods[method_name] = method
        
        # 获取 Impl 块中实现的方法
        impl_methods = {}
        for method in impl_block.methods:
            if hasattr(method, 'name'):
                impl_methods[method.name] = method
            elif isinstance(method, tuple) and len(method) > 0:
                # 处理元组形式的方法
                method_name = method[0]
                impl_methods[method_name] = method
        
        # 检查所有 Trait 方法是否都有实现
        for method_name, trait_method in trait_methods.items():
            if method_name not in impl_methods:
                raise SemanticError(
                    impl_block.line, impl_block.column,
                    f"Trait '{trait_type.name}' requires method '{method_name}' to be implemented"
                )
            
            # 检查方法签名是否匹配
            impl_method = impl_methods[method_name]
            self._check_method_signature(impl_method, trait_method)
    
    def _check_method_signature(self, impl_method, trait_method):
        """
        检查方法签名是否匹配
        
        Args:
            impl_method: 实现的方法
            trait_method: Trait中定义的方法
        
        Raises:
            SemanticError: 如果签名不匹配
        """
        # 获取方法名称
        impl_method_name = getattr(impl_method, 'name', 'unknown')
        
        # 检查参数数量
        impl_params = getattr(impl_method, 'params', [])
        
        # 获取 trait 方法的参数
        if hasattr(trait_method, 'params'):
            trait_params = trait_method.params
        elif isinstance(trait_method, tuple) and len(trait_method) > 1:
            # 处理元组形式的方法
            trait_params = trait_method[1] if len(trait_method) > 1 else []
        else:
            trait_params = []
        
        if len(impl_params) != len(trait_params):
            raise SemanticError(
                getattr(impl_method, 'line', 0), getattr(impl_method, 'column', 0),
                f"Method '{impl_method_name}' has {len(impl_params)} parameters, but Trait requires {len(trait_params)}"
            )
        
        # 检查返回类型
        # 暂时跳过返回类型检查，因为 Trait 中定义的方法可能没有明确的返回类型
        # 后续可以根据需要完善这部分逻辑
        pass
    
    def _resolve_generic_type(self, type_expr):
        """
        解析泛型类型表达式
        
        Args:
            type_expr: 类型表达式（可能是字符串或GenericTypeExpression）
        
        Returns:
            Type: 解析后的类型对象
        """
        if isinstance(type_expr, str):
            # 简单类型
            return self._resolve_type(type_expr)
        elif hasattr(type_expr, 'base_type'):
            # 泛型类型表达式
            base_type = self._resolve_type(type_expr.base_type)
            
            # 检查是否是 Trait 类型
            if isinstance(base_type, TraitType):
                # 对于 Trait 类型，直接返回 Trait 类型本身
                # 简化实现，不处理泛型 Trait 的类型参数
                return base_type
            
            # 解析类型参数
            type_args = []
            for arg in type_expr.type_args:
                type_args.append(self._resolve_generic_type(arg))
            
            # 创建泛型实例类型
            return GenericInstanceType(base_type, type_args)
        elif hasattr(type_expr, 'accept'):
            # 是类型表达式对象，使用 accept 方法解析
            return type_expr.accept(self)
        else:
            return self._resolve_type(type_expr)
