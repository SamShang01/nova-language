"""
Nova语言代码生成器
"""

from nova.compiler.parser.ast import *
from nova.vm.instructions import *
from nova.vm.errors import VMError

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
        for statement in node.statements:
            statement.accept(self)
    
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
        # 简化实现，feature语句在编译时处理
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
        func_obj = NovaFunction(node.name, func_instructions, node.params)
        
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
    
    def visit_StructDefinition(self, node):
        """
        访问结构体定义节点
        """
        # 简化实现，仅记录结构体定义
        pass
    
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
        # 简化实现，仅记录枚举定义
        pass
    
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
        self.instructions.append(LOAD_CONST(node.value))
    
    def visit_IdentifierExpression(self, node):
        """
        访问标识符表达式节点
        """
        self.instructions.append(LOAD_NAME(node.name))
    
    def visit_CallExpression(self, node):
        """
        访问调用表达式节点
        """
        # 先压入函数
        node.callee.accept(self)
        # 然后压入参数
        for arg in node.arguments:
            arg.accept(self)
        
        self.instructions.append(CALL_FUNCTION(len(node.arguments)))
    
    def visit_MemberExpression(self, node):
        """
        访问成员表达式节点
        """
        # 简化实现：跳过成员访问
        node.object.accept(self)
    
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
