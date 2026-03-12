"""
Nova语言代码生成器
"""

from nova.compiler.parser.ast import *
from nova.vm.instructions import *
from nova.vm.errors import VMError
from nova.vm.double_type import Double
from nova.vm.machine import NovaFunction
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
        self.environment = {}  # 全局环境，用于存储类和函数
    
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
        
        # 解析标签为指令索引
        self._resolve_labels()
        
        return (self.instructions, self.constants)
    
    def _resolve_labels(self):
        """
        将标签名称解析为实际的指令索引
        """
        # 解析主指令列表中的标签
        self._resolve_labels_in_instructions(self.instructions)
        
        # 解析函数内部的标签
        for instr in self.instructions:
            if instr.opcode == "LOAD_CONST":
                func = instr.args[0]
                if isinstance(func, NovaFunction):
                    self._resolve_labels_in_instructions(func.instructions)
    
    def _resolve_labels_in_instructions(self, instructions):
        """
        在指令列表中解析标签
        
        Args:
            instructions: 指令列表
        """
        # 首先收集所有标签的位置
        label_positions = {}
        for i, instr in enumerate(instructions):
            if instr.opcode == "LABEL":
                label_name = instr.args[0]
                label_positions[label_name] = i
        
        # 然后更新跳转指令的目标
        for instr in instructions:
            if instr.opcode in ("JUMP", "JUMP_IF_TRUE", "JUMP_IF_FALSE"):
                label_name = instr.args[0]
                if label_name in label_positions:
                    instr.args = (label_positions[label_name],)
                else:
                    raise CodeGenError(f"Undefined label: {label_name}")
    
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
        func_instructions = []
        old_instructions = self.instructions
        self.instructions = func_instructions
        
        if node.body:
            for stmt in node.body:
                stmt.accept(self)
        
        self.instructions = old_instructions
        
        from nova.vm.machine import NovaFunction
        func_obj = NovaFunction(node.name, func_instructions, node.params, is_async=node.is_async)
        func_obj.type_params = node.type_params
        
        self.instructions.append(LOAD_CONST(func_obj))
        self.instructions.append(STORE_NAME(node.name))
    
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
        from nova.vm.machine import NovaClass
        
        fields = []
        for field in node.fields:
            if isinstance(field, tuple):
                fields.append(field)
            else:
                fields.append((field.name, field.var_type))
        
        method_instructions_list = []
        for method in node.methods:
            if hasattr(method, 'name'):
                method_instructions = []
                old_instructions = self.instructions
                self.instructions = method_instructions
                
                if method.body:
                    for stmt in method.body:
                        stmt.accept(self)
                
                self.instructions = old_instructions
                method_instructions_list.append((method.name, method_instructions, method.params))
        
        nova_class = NovaClass(node.name, fields, [])
        
        methods = []
        for method_name, method_instructions, method_params in method_instructions_list:
            from nova.vm.machine import NovaFunction
            method_func = NovaFunction(method_name, method_instructions, method_params)
            if node.name is not None:
                if method_func.environment is None:
                    method_func.environment = {}
                method_func.environment[node.name] = nova_class
            methods.append((method_name, method_func))
        
        nova_class.methods = methods
        
        self.instructions.append(LOAD_CONST(nova_class))
        
        if node.name is not None:
            self.instructions.append(STORE_NAME(node.name))
            # 将类添加到环境中，供 Impl 块使用
            self.environment[node.name] = nova_class
    
    def visit_GenericStructDefinition(self, node):
        """
        访问泛型结构体定义节点
        """
        from nova.vm.machine import NovaClass
        
        fields = []
        for field in node.fields:
            if isinstance(field, tuple):
                fields.append(field)
            else:
                fields.append((field.name, field.var_type))
        
        method_instructions_list = []
        for method in node.methods:
            if hasattr(method, 'name'):
                method_instructions = []
                old_instructions = self.instructions
                self.instructions = method_instructions
                
                if method.body:
                    for stmt in method.body:
                        stmt.accept(self)
                
                self.instructions = old_instructions
                method_instructions_list.append((method.name, method_instructions, method.params))
        
        nova_class = NovaClass(node.name, fields, [])
        nova_class.is_value_type = True
        nova_class.type_params = node.type_params
        
        methods = []
        for method_name, method_instructions, method_params in method_instructions_list:
            from nova.vm.machine import NovaFunction
            method_func = NovaFunction(method_name, method_instructions, method_params)
            if node.name is not None:
                if method_func.environment is None:
                    method_func.environment = {}
                method_func.environment[node.name] = nova_class
            methods.append((method_name, method_func))
        
        nova_class.methods = methods
        
        self.instructions.append(LOAD_CONST(nova_class))
        
        if node.name is not None:
            self.instructions.append(STORE_NAME(node.name))
            # 将类添加到环境中，供 Impl 块使用
            self.environment[node.name] = nova_class
    
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
                # 检查方法是否已经有self参数
                has_self = False
                if method_params:
                    if isinstance(method_params[0], tuple):
                        has_self = method_params[0][0] == 'self'
                    elif hasattr(method_params[0], 'name'):
                        has_self = method_params[0].name == 'self'
                
                # 如果方法没有self参数，自动添加self参数
                if not has_self:
                    # 创建self参数
                    from nova.compiler.parser.ast import ParameterDefinition
                    self_param = ParameterDefinition(0, 0, 'self', None)
                    method_params = [self_param] + list(method_params)
                
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
    
    def visit_GenericClassDefinition(self, node):
        """
        访问泛型类定义节点
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
        
        # 存储类型参数信息
        nova_class.type_params = node.type_params
        
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
        # 调试信息
        print(f"[DEBUG visit_ImplBlock] node.type_name: {node.type_name}")
        print(f"[DEBUG visit_ImplBlock] node.type_name type: {type(node.type_name)}")
        
        # 获取类型名称
        type_name = None
        if hasattr(node.type_name, 'name'):
            type_name = node.type_name.name
            print(f"[DEBUG visit_ImplBlock] type_name from name attribute: {type_name}")
        elif isinstance(node.type_name, str):
            type_name = node.type_name
            print(f"[DEBUG visit_ImplBlock] type_name from str: {type_name}")
        elif hasattr(node.type_name, 'base_type'):
            # GenericTypeExpression，提取基础类型名称
            base_type = node.type_name.base_type
            if isinstance(base_type, str):
                type_name = base_type
            elif hasattr(base_type, 'name'):
                type_name = base_type.name
            print(f"[DEBUG visit_ImplBlock] type_name from GenericTypeExpression.base_type: {type_name}")
        else:
            # 无法识别的类型，暂时跳过
            print(f"[DEBUG visit_ImplBlock] Cannot extract type_name, skipping")
            return
        
        # 查找对应的类
        from nova.vm.machine import NovaClass
        nova_class = None
        
        # 调试信息
        print(f"[DEBUG visit_ImplBlock] Looking for class: {type_name}")
        print(f"[DEBUG visit_ImplBlock] self.environment: {getattr(self, 'environment', None)}")
        
        # 从全局环境中查找类
        if hasattr(self, 'environment') and self.environment:
            print(f"[DEBUG visit_ImplBlock] Checking environment for {type_name}")
            if type_name in self.environment:
                obj = self.environment[type_name]
                print(f"[DEBUG visit_ImplBlock] Found in environment: {obj}, type: {type(obj)}")
                if isinstance(obj, NovaClass):
                    nova_class = obj
                    print(f"[DEBUG visit_ImplBlock] Successfully found NovaClass: {nova_class}")
        
        # 如果找不到，从指令中查找
        if nova_class is None:
            print(f"[DEBUG visit_ImplBlock] Searching in instructions")
            # 遍历指令，寻找LOAD_CONST后跟STORE_NAME的模式
            i = len(self.instructions) - 1
            while i >= 0:
                instr = self.instructions[i]
                # 检查是否是STORE_NAME指令
                if hasattr(instr, 'opcode') and instr.opcode == 'STORE_NAME':
                    # 检查前一个指令是否是LOAD_CONST
                    if i > 0:
                        prev_instr = self.instructions[i-1]
                        if hasattr(prev_instr, 'opcode') and prev_instr.opcode == 'LOAD_CONST':
                            # 检查LOAD_CONST的值是否是NovaClass
                            if len(prev_instr.args) > 0 and isinstance(prev_instr.args[0], NovaClass):
                                loaded_class = prev_instr.args[0]
                                # 检查类名是否匹配
                                if loaded_class.name == type_name:
                                    nova_class = loaded_class
                                    print(f"[DEBUG visit_ImplBlock] Found in instructions: {nova_class}")
                                    break
                i -= 1
        
        if nova_class is None:
            # 找不到类，跳过
            print(f"[DEBUG visit_ImplBlock] Could not find class {type_name}, skipping")
            return
        
        # 处理 Impl 块中的方法
        for method in node.methods:
            if hasattr(method, 'name'):
                method_instructions = []
                old_instructions = self.instructions
                self.instructions = method_instructions
                
                if method.body:
                    for stmt in method.body:
                        stmt.accept(self)
                
                self.instructions = old_instructions
                
                # 创建方法函数
                from nova.vm.machine import NovaFunction
                # impl 块中的方法应该已经包含 self 参数
                # 不需要再添加 self 参数
                method_func = NovaFunction(method.name, method_instructions, method.params)
                if type_name is not None:
                    if method_func.environment is None:
                        method_func.environment = {}
                    method_func.environment[type_name] = nova_class
                
                # 将方法添加到类中
                # 按照与visit_ClassDefinition相同的格式添加方法
                nova_class.methods.append((method.name, method_func, 'public', False))
    
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
                # 先加载对象（this）
                node.left.object.accept(self)
                # 再计算右侧的值
                node.right.accept(self)
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
    
    def visit_AddressOfExpression(self, node):
        """
        访问取地址表达式节点 (&x)
        """
        # 获取操作数的变量名
        if isinstance(node.operand, IdentifierExpression):
            name = node.operand.name
            self.instructions.append(ADDR_OF(name))
        else:
            raise CodeGenError("Can only take address of variables")
    
    def visit_DereferenceExpression(self, node):
        """
        访问解引用表达式节点 (*ptr)
        """
        # 生成操作数的代码
        node.operand.accept(self)
        # 添加解引用指令
        self.instructions.append(DEREF())
    
    def visit_LiteralExpression(self, node):
        """
        访问字面量表达式节点
        """
        # 处理字面量类型转换
        if node.literal_type == "float":
            value = Double(node.value)
        elif node.literal_type == "integer":
            # 确保值是整数类型
            if isinstance(node.value, str):
                value = int(node.value)
            else:
                value = node.value
        else:
            value = node.value
        self.instructions.append(LOAD_CONST(value))
    
    def visit_ArrayLiteralExpression(self, node):
        """
        访问数组字面量表达式节点
        """
        # 生成数组元素的代码
        for element in node.elements:
            element.accept(self)
        
        # 创建数组
        from nova.vm.instructions import BUILD_LIST
        self.instructions.append(BUILD_LIST(len(node.elements)))
    
    def visit_TupleLiteralExpression(self, node):
        """
        访问元组字面量表达式节点
        """
        # 生成元组元素的代码
        for element in node.elements:
            element.accept(self)
        
        # 创建元组
        from nova.vm.instructions import BUILD_TUPLE
        self.instructions.append(BUILD_TUPLE(len(node.elements)))
    
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
            # 特殊处理数组的len方法
            if isinstance(obj, list) and attr_name == "len":
                return lambda: len(obj)
            
            # 直接使用getattr，触发对象的__getattribute__方法
            # 这样可以确保类型转换逻辑被正确执行
            return getattr(obj, attr_name)
        
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
    
    def visit_GenericTypeExpression(self, node):
        """
        访问泛型类型表达式节点
        """
        # 生成加载类型的代码
        # 这里需要加载类型名称，然后将类型参数作为参数传递
        # 暂时简化处理，直接加载类型名称
        self.instructions.append(LOAD_NAME(node.base_type))
    
    def _new_label(self):
        """
        生成新标签
        
        Returns:
            str: 标签名称
        """
        label = f"label_{self.label_count}"
        self.label_count += 1
        return label
