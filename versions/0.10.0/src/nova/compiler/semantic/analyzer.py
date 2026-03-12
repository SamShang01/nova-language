"""
Nova语言语义分析器
"""

from nova.compiler.parser import *
from nova.compiler.semantic.symbols import *
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
        
        # print函数
        print_func = FunctionSymbol(
            "print",
            UNIT_TYPE,
            params=[("value", ANY_TYPE)]
        )
        self.global_scope.declare_symbol(print_func)
        
        # len函数
        len_func = FunctionSymbol(
            "len",
            INT_TYPE,
            params=[("value", STRING_TYPE)]
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
        if hasattr(node, 'where_clause') and node.where_clause:
            self._check_trait_constraints(node.where_clause, type_param_map)
        
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
        # 解析字段类型
        fields = []
        for field_name, field_type in node.fields:
            field_type_obj = self._resolve_type(field_type)
            fields.append((field_name, field_type_obj))
        
        # 创建结构体类型
        struct_type = StructType(node.name, fields)
        self.types[node.name] = struct_type
        
        # 创建类型符号
        type_symbol = TypeSymbol(node.name, struct_type, members=fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 分析结构体方法
        for method in node.methods:
            # 分析方法
            method.accept(self)
    
    def visit_ClassDefinition(self, node):
        """
        访问类定义节点
        """
        # 创建类作用域
        class_scope = Scope(f"class_{node.name}", parent=self.current_scope)
        old_scope = self.current_scope
        self.current_scope = class_scope
        
        # 解析字段类型（包括访问修饰符）
        fields = []
        for field_name, field_type, access_modifier in node.fields:
            field_type_obj = self._resolve_type(field_type)
            fields.append((field_name, field_type_obj, access_modifier))
        
        # 创建类类型
        class_type = StructType(node.name, fields)
        self.types[node.name] = class_type
        
        # 创建类型符号
        type_symbol = TypeSymbol(node.name, class_type, members=fields)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
        
        # 分析方法（包括访问修饰符）
        for method, access_modifier in node.methods:
            method.accept(self)
        
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
        
        # 创建泛型类类型
        class_type = StructType(node.name, node.fields)
        self.types[node.name] = class_type
        
        # 恢复作用域
        self.current_scope = old_scope
        
        # 在全局作用域中声明类型符号
        type_symbol = TypeSymbol(node.name, class_type, members=node.fields)
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
            
            # 为方法添加self参数
            if method.params and method.params[0].name == "self":
                # 为self参数创建符号
                self_symbol = VariableSymbol("self", class_type)
                try:
                    self.current_scope.declare_symbol(self_symbol)
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
        # 创建Trait类型
        trait_type = TraitType(node.name, methods=node.methods)
        self.types[node.name] = trait_type
        
        # 创建类型符号
        type_symbol = TypeSymbol(node.name, trait_type, members=node.methods)
        try:
            self.current_scope.declare_symbol(type_symbol)
        except ValueError as e:
            raise SemanticError(node.line, node.column, str(e))
    
    def visit_ImplBlock(self, node):
        """
        访问Impl块节点
        """
        # 解析类型
        type_obj = self._resolve_type(node.type_name)
        
        # 分析方法
        for method in node.methods:
            method.accept(self)
    
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
            
            # 对于相等/不等比较操作，返回布尔类型
            if node.operator in ("==", "!="):
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
            # 如果类型不存在，返回一个新的类型对象
            return PrimitiveType(node.name)
    
    def visit_GenericTypeExpression(self, node):
        """
        访问泛型类型表达式节点
        """
        # 解析类型参数
        type_args = []
        for type_arg in node.type_args:
            type_args.append(type_arg.accept(self))
        
        # 尝试解析泛型结构体符号
        symbol = self.current_scope.resolve_symbol(node.base_type)
        if symbol and isinstance(symbol, TypeSymbol):
            # 创建泛型实例类型
            return GenericInstanceType(symbol.type, type_args)
        
        # 如果符号不存在，返回一个新的泛型类型对象
        # 简化实现，返回泛型类型
        return GenericType(node.base_type)
    
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
            
            # 如果从作用域中找不到符号，尝试从types中查找类型
            if not symbol and node.callee.name in self.types:
                # 创建一个临时的TypeSymbol对象
                from nova.compiler.semantic.symbols import TypeSymbol
                symbol = TypeSymbol(node.callee.name, self.types[node.callee.name])
            
            # 处理结构体实例化
            if symbol and hasattr(symbol, 'type') and isinstance(symbol.type, StructType):
                # 检查结构体实例化的参数类型
                struct_type = symbol.type
                for i, arg in enumerate(node.arguments):
                    arg_type = self._infer_type(arg)
                    
                    # 获取字段类型
                    if i < len(struct_type.fields):
                        field = struct_type.fields[i]
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
            # 返回泛型类型实例化的类型
            return node.callee.accept(self)
        
        # 处理super方法调用
        if isinstance(node.callee, MemberExpression):
            if hasattr(node.callee.object, 'name') and node.callee.object.name == 'super':
                # super方法调用，返回ANY_TYPE
                return ANY_TYPE
        
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
        
        # 如果是结构体类型，尝试获取成员的类型
        if hasattr(obj_type, 'fields'):
            for field in obj_type.fields:
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
                    return field_type if field_type else obj_type
        
        # 简化实现，返回对象类型
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
        
        # 处理auto类型
        if type_name == "auto":
            return ANY_TYPE
        
        # 简单类型
        if type_name in self.types:
            return self.types[type_name]
        else:
            # 尝试从作用域中解析
            symbol = self.current_scope.resolve_symbol(type_name)
            if isinstance(symbol, TypeSymbol):
                return symbol.type
            else:
                raise SemanticError(0, 0, f"Undefined type '{type_name}'")
    
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
        if type1 == ANY_TYPE or type2 == ANY_TYPE:
            return True
        
        # 严格类型检查：不允许隐式类型转换
        # 只有完全相同的类型才兼容
        return type1 == type2
    
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
            
            # 检查特质是否存在
            if constraint.trait_name not in self.types:
                raise SemanticError(
                    constraint.line, constraint.column,
                    f"Unknown trait '{constraint.trait_name}'"
                )
            
            # 检查是否是特质类型
            trait_type = self.types[constraint.trait_name]
            if not isinstance(trait_type, TraitType):
                raise SemanticError(
                    constraint.line, constraint.column,
                    f"'{constraint.trait_name}' is not a trait"
                )
    
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
            
            # 解析类型参数
            type_args = []
            for arg in type_expr.type_args:
                type_args.append(self._resolve_generic_type(arg))
            
            # 创建泛型实例类型
            return GenericInstanceType(base_type, type_args)
        else:
            return self._resolve_type(type_expr)
