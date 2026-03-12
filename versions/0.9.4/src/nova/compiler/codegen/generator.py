"""
Nova语言代码生成器
"""

from nova.compiler.parser.ast import *
from nova.vm.instructions import *
from nova.vm.errors import VMError
from nova.vm.double_type import Double
from nova.compiler.features import get_feature_manager
from decimal import Decimal, getcontext

class CodeGenerator:
    """
    代码生成器
    
    负责将AST转换为虚拟机指令
    """
    
    def __init__(self):
        """
        初始化代码生成器
        """
        self.instructions = []
        self.constants = []
        self.label_count = 0
        self.feature_manager = get_feature_manager()  # 特性管理器
    
    def _is_constant_expression(self, node):
        """
        检查表达式是否是常量表达式
        
        Args:
            node: 表达式节点
        
        Returns:
            bool: 是否是常量表达式
        """
        if isinstance(node, LiteralExpression):
            return True
        elif isinstance(node, BinaryExpression):
            return (self._is_constant_expression(node.left) and 
                    self._is_constant_expression(node.right))
        elif isinstance(node, UnaryExpression):
            return self._is_constant_expression(node.operand)
        else:
            return False
    
    def _is_cancellation_pattern(self, node):
        """
        检查表达式是否是抵消模式
        
        只要算式中有 +x 和 -x，就应该被优化
        
        Args:
            node: 表达式节点
        
        Returns:
            bool: 是否是抵消模式
        """
        if not isinstance(node, BinaryExpression):
            return False
        
        # 检查是否是二元表达式
        if node.operator not in ['+', '-']:
            return False
        
        # 提取所有操作
        operations = self._extract_operations(node)
        
        # 检查是否有可以抵消的操作对（+x 和 -x）
        for i in range(len(operations)):
            for j in range(i + 1, len(operations)):
                op1, val1 = operations[i]
                op2, val2 = operations[j]
                
                # 检查操作符是否相反
                if ((op1 == '+' and op2 == '-') or (op1 == '-' and op2 == '+')):
                    # 检查操作数是否相等
                    if isinstance(val1, LiteralExpression) and isinstance(val2, LiteralExpression):
                        if val1.value == val2.value:
                            return True
        
        return False
    
    def _extract_operations(self, node):
        """
        提取表达式中的所有操作
        
        Args:
            node: 表达式节点
        
        Returns:
            list: 操作列表，每个元素是 (操作符, 操作数节点)
        """
        if not isinstance(node, BinaryExpression) or node.operator not in ['+', '-']:
            return [(None, node)]
        
        operations = []
        
        # 递归提取左操作数的操作
        left_ops = self._extract_operations(node.left)
        operations.extend(left_ops)
        
        # 添加当前操作
        operations.append((node.operator, node.right))
        
        return operations
    
    def _evaluate_constant_expression(self, node):
        """
        计算常量表达式的值
        
        Args:
            node: 表达式节点
        
        Returns:
            表达式的值
        """
        if isinstance(node, LiteralExpression):
            if node.literal_type == "float":
                return Double(node.value)
            else:
                return node.value
        elif isinstance(node, BinaryExpression):
            left_value = self._evaluate_constant_expression(node.left)
            right_value = self._evaluate_constant_expression(node.right)
            
            # 检查是否启用了延迟运算特性
            is_deferred_enabled = self.feature_manager.is_enabled('DeferredOperations')
            
            # 检查是否是抵消模式
            is_cancellation = self._is_cancellation_pattern(node)
            
            if is_deferred_enabled and is_cancellation:
                # 启用了延迟运算特性且是抵消模式，使用Double类型进行优化计算
                if not isinstance(left_value, Double):
                    left_value = Double(left_value)
                if not isinstance(right_value, Double):
                    right_value = Double(right_value)
                
                if node.operator == '+':
                    return (left_value + right_value).evaluate()
                elif node.operator == '-':
                    return (left_value - right_value).evaluate()
                else:
                    return None
            else:
                # 未启用延迟运算特性或不是抵消模式，使用Python原生float进行计算，保留浮点数精度问题
                if isinstance(left_value, Double):
                    left_value = float(left_value.value)
                elif isinstance(left_value, (int, float)):
                    left_value = float(left_value)
                else:
                    left_value = 0.0
                
                if isinstance(right_value, Double):
                    right_value = float(right_value.value)
                elif isinstance(right_value, (int, float)):
                    right_value = float(right_value)
                else:
                    right_value = 0.0
                
                # 按照表达式的顺序进行计算，保留浮点数精度问题
                if node.operator == '+':
                    return left_value + right_value
                elif node.operator == '-':
                    return left_value - right_value
                elif node.operator == '*':
                    return left_value * right_value
                elif node.operator == '/':
                    return left_value / right_value
                else:
                    return None
        elif isinstance(node, UnaryExpression):
            operand_value = self._evaluate_constant_expression(node.operand)
            
            # 检查是否启用了延迟运算特性
            if self.feature_manager.is_enabled('DeferredOperations'):
                if not isinstance(operand_value, Double):
                    operand_value = Double(operand_value)
                if node.operator == '-':
                    return (-operand_value).evaluate()
                else:
                    return operand_value.evaluate()
            else:
                # 未启用延迟运算特性，使用Python原生float
                if isinstance(operand_value, Double):
                    operand_value = float(operand_value.value)
                elif not isinstance(operand_value, (int, float)):
                    operand_value = 0.0
                
                if node.operator == '-':
                    return -operand_value
                else:
                    return operand_value
        else:
            return None
    
    def _is_deferred_expression(self, node):
        """
        检查表达式是否可以延迟运算
        
        Args:
            node: 表达式节点
        
        Returns:
            bool: 是否可以延迟运算
        """
        # 对于乘法、除法、加法和减法操作，可以延迟运算
        if isinstance(node, BinaryExpression):
            # 处理乘法和除法
            if node.operator in ['*', '/', '+', '-']:
                # 检查左右操作数是否是字面量或可以延迟运算的表达式
                if (isinstance(node.left, LiteralExpression) or self._is_deferred_expression(node.left)) and \
                   (isinstance(node.right, LiteralExpression) or self._is_deferred_expression(node.right)):
                    return True
        return False
    
    def _optimize_deferred_expression(self, node):
        """
        优化延迟运算表达式
        
        Args:
            node: 表达式节点
        
        Returns:
            优化后的表达式值
        """
        # 直接使用_evaluate_constant_expression进行优化计算
        # 这样可以利用Double类型的优化逻辑
        return self._evaluate_constant_expression(node)
    
    def generate(self, ast):
        """
        生成代码
        
        Args:
            ast: 抽象语法树
        
        Returns:
            tuple: (指令列表, 常量列表)
        """
        self.instructions = []
        self.constants = []
        
        ast.accept(self)
        
        return (self.instructions, self.constants)
    
    def visit_Program(self, node):
        """
        访问程序节点
        """
        has_main = False
        for statement in node.statements:
            statement.accept(self)
            # 检查是否有main函数定义
            if hasattr(statement, 'name') and statement.name == 'main':
                has_main = True
        
        # 只有在有main函数时才生成调用main函数的指令
        # 在REPL环境中，通常没有main函数，所以不会生成调用指令
        if has_main:
            self.instructions.append(LOAD_NAME("main"))
            self.instructions.append(CALL_FUNCTION(0))
    
    def visit_ModuleDeclaration(self, node):
        """
        访问模块声明节点
        """
        pass
    
    def visit_ImportStatement(self, node):
        """
        访问导入语句节点
        """
        pass
    
    def visit_FeatureStatement(self, node):
        """
        访问Feature语句节点
        """
        # 特性启用在语义分析阶段已经处理
        # 这里不需要做任何操作
        pass
    
    def visit_FunctionDefinition(self, node):
        """
        访问函数定义节点
        """
        # 生成函数体的指令
        func_instructions = []
        old_instructions = self.instructions
        self.instructions = func_instructions
        
        # 处理函数体
        if node.body:
            for stmt in node.body:
                stmt.accept(self)
        
        # 恢复原来的指令列表
        self.instructions = old_instructions
        
        # 创建Nova函数对象
        from nova.vm.machine import NovaFunction
        func_obj = NovaFunction(node.name, func_instructions, node.params, is_async=node.is_async)
        
        # 生成指令：加载函数对象，存储到环境
        self.instructions.append(LOAD_CONST(func_obj))
        self.instructions.append(STORE_NAME(node.name))
    
    def visit_GenericFunctionDefinition(self, node):
        """
        访问泛型函数定义节点
        """
        # 泛型函数在运行时进行单态化
        # 这里仅记录函数定义
        pass
    
    def visit_VariableDeclaration(self, node):
        """
        访问变量声明节点
        """
        if node.value:
            node.value.accept(self)
        else:
            # 没有初始值时，使用 None 作为默认值
            self.instructions.append(LOAD_CONST(None))
        self.instructions.append(STORE_NAME(node.name))
    
    def visit_ConstantDeclaration(self, node):
        """
        访问常量声明节点
        """
        if node.value:
            node.value.accept(self)
            self.instructions.append(STORE_NAME(node.name))
    
    def visit_IfStatement(self, node):
        """
        访问If语句节点
        """
        node.condition.accept(self)
        
        else_label = self._new_label()
        end_label = self._new_label()
        
        self.instructions.append(JUMP_IF_FALSE(else_label))
        
        for stmt in node.then_branch:
            stmt.accept(self)
        
        if node.else_branch:
            self.instructions.append(JUMP(end_label))
        
        self.instructions.append(LABEL(else_label))
        
        if node.else_branch:
            if isinstance(node.else_branch, list):
                for stmt in node.else_branch:
                    stmt.accept(self)
            else:
                node.else_branch.accept(self)
        
        self.instructions.append(LABEL(end_label))
    
    def visit_ForLoop(self, node):
        """
        访问For循环节点
        """
        # 简化实现
        node.iterable.accept(self)
        
        start_label = self._new_label()
        end_label = self._new_label()
        
        self.instructions.append(LABEL(start_label))
        # 简化实现：假设iterable是一个列表
        self.instructions.append(JUMP_IF_FALSE(end_label))
        self.instructions.append(STORE_NAME(node.variable))
        
        for stmt in node.body:
            stmt.accept(self)
        
        self.instructions.append(JUMP(start_label))
        self.instructions.append(LABEL(end_label))
    
    def visit_WhileLoop(self, node):
        """
        访问While循环节点
        """
        start_label = self._new_label()
        end_label = self._new_label()
        
        self.instructions.append(LABEL(start_label))
        node.condition.accept(self)
        self.instructions.append(JUMP_IF_FALSE(end_label))
        
        for stmt in node.body:
            stmt.accept(self)
        
        self.instructions.append(JUMP(start_label))
        self.instructions.append(LABEL(end_label))
    
    def visit_LoopStatement(self, node):
        """
        访问Loop语句节点
        """
        start_label = self._new_label()
        end_label = self._new_label()
        
        self.instructions.append(LABEL(start_label))
        
        for stmt in node.body:
            stmt.accept(self)
        
        self.instructions.append(JUMP(start_label))
        self.instructions.append(LABEL(end_label))
    
    def visit_MatchStatement(self, node):
        """
        访问Match语句节点
        """
        node.expression.accept(self)
        
        end_label = self._new_label()
        
        for pattern, case_body in node.cases:
            case_label = self._new_label()
            # 简化实现：直接跳过match
            self.instructions.append(JUMP_IF_FALSE(case_label))
            self.instructions.append(POP_TOP())
            case_body.accept(self)
            self.instructions.append(JUMP(end_label))
            self.instructions.append(LABEL(case_label))
        
        self.instructions.append(POP_TOP())
        self.instructions.append(LABEL(end_label))
    
    def visit_ReturnStatement(self, node):
        """
        访问Return语句节点
        """
        if node.value:
            node.value.accept(self)
        else:
            self.instructions.append(LOAD_CONST(None))
        
        self.instructions.append(RETURN_VALUE())
    
    def visit_AwaitExpression(self, node):
        """
        访问await表达式节点
        """
        # 生成表达式的代码
        node.expression.accept(self)
        # 这里需要添加await指令
        # 暂时简化处理，实际应该调用事件循环处理
        return None
    
    def visit_BreakStatement(self, node):
        """
        访问Break语句节点
        """
        # 简化实现：跳过break
        pass
    
    def visit_ContinueStatement(self, node):
        """
        访问Continue语句节点
        """
        # 简化实现：跳过continue
        pass
    
    def visit_DeleteVariable(self, node):
        """
        访问DeleteVariable节点
        """
        # 生成删除变量的指令
        self.instructions.append(DELETE_NAME(node.name))
    
    def visit_StructDefinition(self, node):
        """
        访问结构体定义节点
        """
        # 创建NovaClass对象
        from nova.vm.machine import NovaClass
        
        # 提取字段
        fields = []
        for field in node.fields:
            if isinstance(field, tuple):
                fields.append(field)
            else:
                # field是VariableDeclaration节点
                fields.append((field.name, field.var_type))
        
        # 提取方法指令
        method_instructions_list = []
        for method in node.methods:
            if hasattr(method, 'name'):
                # 创建方法函数
                method_instructions = []
                old_instructions = self.instructions
                self.instructions = method_instructions
                
                # 处理方法体
                if method.body:
                    for stmt in method.body:
                        stmt.accept(self)
                
                # 恢复原来的指令列表
                self.instructions = old_instructions
                method_instructions_list.append((method.name, method_instructions, method.params))
        
        # 创建NovaClass对象
        nova_class = NovaClass(node.name, fields, [])
        
        # 创建方法函数并添加到methods列表
        methods = []
        for method_name, method_instructions, method_params in method_instructions_list:
            # 创建NovaFunction对象
            from nova.vm.machine import NovaFunction
            method_func = NovaFunction(method_name, method_instructions, method_params)
            # 确保方法函数的环境包含结构体名称
            if node.name is not None:
                if method_func.environment is None:
                    method_func.environment = {}
                method_func.environment[node.name] = nova_class
            methods.append((method_name, method_func))
        
        # 更新nova_class的methods属性
        nova_class.methods = methods
        
        # 生成指令：加载类对象
        self.instructions.append(LOAD_CONST(nova_class))
        
        # 如果是命名结构体，存储到环境
        if node.name is not None:
            self.instructions.append(STORE_NAME(node.name))
    
    def visit_ClassDefinition(self, node):
        """
        访问类定义节点
        """
        # 创建NovaClass对象
        from nova.vm.machine import NovaClass
        
        # 提取字段（包括访问修饰符）
        fields = []
        for field in node.fields:
            if isinstance(field, tuple):
                field_name, field_type, access_modifier = field
                fields.append((field_name, field_type, access_modifier))
            else:
                # field是VariableDeclaration节点
                fields.append((field.name, field.var_type, 'public'))
        
        # 提取方法指令（包括访问修饰符）
        method_instructions_list = []
        for method_info in node.methods:
            if isinstance(method_info, tuple):
                method, access_modifier = method_info
            else:
                method = method_info
                access_modifier = 'public'
            
            if hasattr(method, 'name'):
                # 跳过抽象方法（没有方法体）
                if hasattr(method, 'is_abstract') and method.is_abstract:
                    method_instructions_list.append((method.name, [], method.params, access_modifier, True))
                    continue
                
                # 创建方法函数
                method_instructions = []
                old_instructions = self.instructions
                self.instructions = method_instructions
                
                # 处理方法体
                if method.body:
                    for stmt in method.body:
                        stmt.accept(self)
                
                # 恢复原来的指令列表
                self.instructions = old_instructions
                method_instructions_list.append((method.name, method_instructions, method.params, access_modifier, False))
        
        # 处理构造函数（init方法）
        init_func = None
        if node.init_method and hasattr(node.init_method, 'name'):
            init_instructions = []
            old_instructions = self.instructions
            self.instructions = init_instructions
            
            # 处理构造函数体
            if node.init_method.body:
                for stmt in node.init_method.body:
                    stmt.accept(self)
            
            # 恢复原来的指令列表
            self.instructions = old_instructions
            
            # 创建构造函数函数
            from nova.vm.machine import NovaFunction
            init_func = NovaFunction('init', init_instructions, node.init_method.params)
        
        # 创建NovaClass对象
        nova_class = NovaClass(node.name, fields, [])
        
        # 设置抽象类标志
        nova_class.is_abstract = node.is_abstract
        
        # 设置父类名称（如果有继承）
        # 实际的父类对象将在运行时解析
        if node.parent:
            nova_class.parent_name = node.parent
        
        # 设置构造函数
        nova_class.init_method = init_func
        
        # 创建方法函数并添加到methods列表
        methods = []
        for method_name, method_instructions, method_params, access_modifier, is_abstract in method_instructions_list:
            # 抽象方法没有函数体，设置为None
            if is_abstract:
                methods.append((method_name, None, access_modifier, True))
            else:
                # 创建NovaFunction对象
                from nova.vm.machine import NovaFunction
                method_func = NovaFunction(method_name, method_instructions, method_params)
                # 确保方法函数的环境包含类名称
                if node.name is not None:
                    if method_func.environment is None:
                        method_func.environment = {}
                    method_func.environment[node.name] = nova_class
                methods.append((method_name, method_func, access_modifier, False))
        
        # 更新nova_class的methods属性
        nova_class.methods = methods
        
        # 处理静态字段（只记录字段名，初始值将在运行时设置）
        for static_field in node.static_fields:
            field_name, field_type, access_modifier, initial_value = static_field
            nova_class.static_fields[field_name] = None  # 初始值为None，将在类加载后设置
        
        # 处理静态方法
        for static_method_info in node.static_methods:
            if isinstance(static_method_info, tuple):
                static_method, access_modifier = static_method_info
            else:
                static_method = static_method_info
                access_modifier = 'public'
            
            if hasattr(static_method, 'name'):
                # 创建静态方法函数
                static_method_instructions = []
                old_instructions = self.instructions
                self.instructions = static_method_instructions
                
                # 处理方法体
                if static_method.body:
                    for stmt in static_method.body:
                        stmt.accept(self)
                
                # 恢复原来的指令列表
                self.instructions = old_instructions
                
                # 创建NovaFunction对象
                from nova.vm.machine import NovaFunction
                static_method_func = NovaFunction(static_method.name, static_method_instructions, static_method.params)
                # 确保静态方法函数的环境包含类名称
                if node.name is not None:
                    if static_method_func.environment is None:
                        static_method_func.environment = {}
                    static_method_func.environment[node.name] = nova_class
                nova_class.static_methods[static_method.name] = (static_method_func, access_modifier)
        
        # 生成指令：加载类对象
        self.instructions.append(LOAD_CONST(nova_class))
        
        # 如果是命名类，存储到环境
        if node.name is not None:
            self.instructions.append(STORE_NAME(node.name))
    
    def visit_GenericStructDefinition(self, node):
        """
        访问泛型结构体定义节点
        """
        # 泛型结构体在运行时进行单态化
        # 这里仅记录结构体定义
        pass
    
    def visit_EnumDefinition(self, node):
        """
        访问枚举定义节点
        """
        # 创建NovaEnum对象
        from nova.vm.machine import NovaEnum
        
        # 创建NovaEnum对象
        nova_enum = NovaEnum(node.name, node.variants)
        
        # 生成指令：加载枚举对象
        self.instructions.append(LOAD_CONST(nova_enum))
        
        # 如果是命名枚举，存储到环境
        if node.name is not None:
            self.instructions.append(STORE_NAME(node.name))
    
    def visit_UnionDefinition(self, node):
        """
        访问联合体定义节点
        """
        # 创建NovaUnion对象
        from nova.vm.machine import NovaUnion
        
        # 创建NovaUnion对象
        nova_union = NovaUnion(node.name, node.variants)
        
        # 生成指令：加载联合体对象
        self.instructions.append(LOAD_CONST(nova_union))
        
        # 如果是命名联合体，存储到环境
        if node.name is not None:
            self.instructions.append(STORE_NAME(node.name))
    
    def visit_TraitDefinition(self, node):
        """
        访问Trait定义节点
        """
        # 简化实现，仅记录Trait定义
        pass
    
    def visit_ImplBlock(self, node):
        """
        访问Impl块节点
        """
        # 简化实现，仅记录Impl块
        pass
    
    def visit_BinaryExpression(self, node):
        """
        访问二元表达式节点
        """
        if node.operator == '=':
            # 特殊处理赋值操作：x = y 或 this.x = y
            # 对于赋值，我们需要先计算右侧的值，然后存储到左侧的变量
            if isinstance(node.left, IdentifierExpression):
                # 计算右侧表达式
                node.right.accept(self)
                # 存储到变量
                self.instructions.append(STORE_NAME(node.left.name))
            elif isinstance(node.left, MemberExpression):
                # 成员赋值：this.name = value
                # 先计算右侧的值
                node.right.accept(self)
                # 加载对象（this）
                node.left.object.accept(self)
                # 存储到成员
                from nova.vm.instructions import STORE_ATTR
                self.instructions.append(STORE_ATTR(node.left.member))
            else:
                raise VMError(f"Invalid assignment target at line {node.line}, column {node.column}")
        else:
            # 其他二元操作
            node.left.accept(self)
            node.right.accept(self)
            
            operator_map = {
                '+': BINARY_ADD(),
                '-': BINARY_SUB(),
                '*': BINARY_MUL(),
                '/': BINARY_DIV(),
                '%': BINARY_DIV(),
                '==': COMPARE_EQ(),
                '!=': COMPARE_NE(),
                '<': COMPARE_LT(),
                '<=': COMPARE_LE(),
                '>': COMPARE_GT(),
                '>=': COMPARE_GE(),
                '&&': COMPARE_EQ(),
                '||': COMPARE_NE(),
            }
            
            if node.operator in operator_map:
                self.instructions.append(operator_map[node.operator])
            else:
                raise VMError(f"Unknown operator '{node.operator}' at line {node.line}, column {node.column}")
    
    def visit_UnaryExpression(self, node):
        """
        访问一元表达式节点
        """
        node.operand.accept(self)
        
        if node.operator == '-':
            # 简化实现：乘以-1
            self.instructions.append(LOAD_CONST(-1))
            self.instructions.append(BINARY_MUL())
        elif node.operator == '!':
            # 简化实现：使用比较
            self.instructions.append(LOAD_CONST(False))
            self.instructions.append(COMPARE_EQ())
    
    def visit_LiteralExpression(self, node):
        """
        访问字面量表达式节点
        """
        # 如果是浮点数类型，转换为自定义的Double类型
        if node.literal_type == "float":
            value = Double(node.value)
        else:
            value = node.value
        self.instructions.append(LOAD_CONST(value))
    
    def visit_IdentifierExpression(self, node):
        """
        访问标识符表达式节点
        """
        # 特殊处理super关键字
        if node.name == 'super':
            # super实际上是对this的引用，在运行时通过this.super访问
            self.instructions.append(LOAD_NAME('this'))
        else:
            self.instructions.append(LOAD_NAME(node.name))
    
    def visit_CallExpression(self, node):
        """
        访问调用表达式节点
        """
        # 先压入函数
        node.callee.accept(self)
        
        # 处理参数：分离位置参数和命名参数
        positional_count = 0
        keyword_arg_names = []
        
        for arg in node.arguments:
            if isinstance(arg, NamedArgumentExpression):
                # 命名参数：先求值参数值
                arg.value.accept(self)
                keyword_arg_names.append(arg.name)
            else:
                # 位置参数
                arg.accept(self)
                positional_count += 1
        
        # 生成调用指令
        self.instructions.append(CALL_FUNCTION(positional_count, keyword_arg_names))
    
    def visit_NamedArgumentExpression(self, node):
        """
        访问命名参数表达式节点
        """
        # 命名参数的值已经在visit_CallExpression中处理
        pass
    
    def visit_MemberExpression(self, node):
        """
        访问成员表达式节点
        """
        # 特殊处理super访问
        if hasattr(node.object, 'name') and node.object.name == 'super':
            # super.member 转换为 this.super.member
            # 先生成this的代码
            self.instructions.append(LOAD_NAME('this'))
            # 然后获取super属性
            from nova.vm.machine import BuiltinFunction
            
            def get_super_attr(obj, attr_name):
                if hasattr(obj, 'super'):
                    super_obj = obj.super
                    if hasattr(super_obj, attr_name):
                        return getattr(super_obj, attr_name)
                raise AttributeError(f"'super' object has no attribute '{attr_name}'")
            
            self.instructions.append(LOAD_CONST(BuiltinFunction("get_super_attr", get_super_attr)))
            self.instructions.append(LOAD_NAME('this'))
            self.instructions.append(LOAD_CONST(node.member))
            self.instructions.append(CALL_FUNCTION(2))
            return
        
        # 生成获取成员的代码
        # 这里使用一个特殊的函数来获取成员
        from nova.vm.machine import BuiltinFunction
        
        # 创建一个获取成员的函数
        def get_attr(obj, attr_name):
            if hasattr(obj, attr_name):
                return getattr(obj, attr_name)
            elif hasattr(obj, "fields") and attr_name in obj.fields:
                return obj.fields[attr_name]
            elif hasattr(obj, "nova_class") and hasattr(obj.nova_class, "get_method"):
                # 尝试从类中获取方法
                method = obj.nova_class.get_method(attr_name)
                if method:
                    return method
                else:
                    raise AttributeError(f"'{obj.__class__.__name__}' object has no attribute '{attr_name}'")
            else:
                raise AttributeError(f"'{obj.__class__.__name__}' object has no attribute '{attr_name}'")
        
        # 生成LOAD_CONST指令加载函数
        self.instructions.append(LOAD_CONST(BuiltinFunction("getattr", get_attr)))
        # 生成对象的代码
        node.object.accept(self)
        # 生成LOAD_CONST指令加载属性名
        self.instructions.append(LOAD_CONST(node.member))
        # 生成CALL_FUNCTION指令调用函数
        self.instructions.append(CALL_FUNCTION(2))
    
    def visit_IndexExpression(self, node):
        """
        访问索引表达式节点
        """
        # 简化实现：跳过索引访问
        node.object.accept(self)
    
    def visit_LambdaExpression(self, node):
        """
        访问Lambda表达式节点
        """
        # 简化实现
        pass
    
    def _new_label(self):
        """
        生成新标签
        
        Returns:
            str: 标签名称
        """
        label = f"label_{self.label_count}"
        self.label_count += 1
        return label
