"""
Nova语言代码优化Pass
"""

from nova.compiler.parser.ast import BinaryExpression, LiteralExpression
from nova.compiler.features import get_feature_manager

class OptimizationPass:
    """
    优化Pass基类
    """
    
    def optimize(self, ast):
        """
        优化AST
        
        Args:
            ast: 抽象语法树
        
        Returns:
            Node: 优化后的AST
        """
        raise NotImplementedError

class ConstantFolding(OptimizationPass):
    """
    常量折叠优化
    
    在编译时计算常量表达式
    """
    
    def optimize(self, ast):
        """
        执行常量折叠优化
        
        Args:
            ast: 抽象语法树
        
        Returns:
            Node: 优化后的AST
        """
        return self._fold_constants(ast)
    
    def _fold_constants(self, node):
        """
        递归折叠常量
        
        Args:
            node: AST节点
        
        Returns:
            Node: 折叠后的节点
        """
        from nova.compiler.parser.ast import Node, Program, BinaryExpression, LiteralExpression
        
        if node is None:
            return None
        
        # 处理二元表达式
        if isinstance(node, BinaryExpression):
            left = self._fold_constants(node.left)
            right = self._fold_constants(node.right)
            
            if isinstance(left, LiteralExpression) and isinstance(right, LiteralExpression):
                result = self._evaluate_constant(left, right, node.operator)
                if result is not None:
                    return result
            
            node.left = left
            node.right = right
            return node
        
        # 处理程序节点
        if isinstance(node, Program):
            node.statements = [self._fold_constants(stmt) for stmt in node.statements]
            return node
        
        # 处理表达式语句
        if hasattr(node, 'expression'):
            node.expression = self._fold_constants(node.expression)
            return node
        
        # 递归处理所有子节点
        for attr_name in dir(node):
            if not attr_name.startswith('_'):
                attr_value = getattr(node, attr_name, None)
                if isinstance(attr_value, Node):
                    setattr(node, attr_name, self._fold_constants(attr_value))
                elif isinstance(attr_value, list):
                    setattr(node, attr_name, [self._fold_constants(item) if isinstance(item, Node) else item for item in attr_value])
        
        return node
    
    def _evaluate_constant(self, left, right, operator):
        """
        计算常量表达式
        
        Args:
            left: 左操作数
            right: 右操作数
            operator: 运算符
        
        Returns:
            LiteralExpression: 计算结果
        """
        try:
            # 确定结果类型
            # 如果任一操作数是float，结果就是float
            # 否则保持int类型
            if left.literal_type == 'float' or right.literal_type == 'float':
                result_type = 'float'
            else:
                result_type = 'int'
            
            if operator == '+':
                result = left.value + right.value
                return LiteralExpression(left.line, left.column, result, result_type)
            elif operator == '-':
                result = left.value - right.value
                return LiteralExpression(left.line, left.column, result, result_type)
            elif operator == '*':
                result = left.value * right.value
                return LiteralExpression(left.line, left.column, result, result_type)
            elif operator == '/':
                if right.value != 0:
                    # 除法总是返回float
                    result = left.value / right.value
                    return LiteralExpression(left.line, left.column, result, 'float')
            elif operator == '%':
                if right.value != 0:
                    result = left.value % right.value
                    return LiteralExpression(left.line, left.column, result, result_type)
        except:
            pass
        
        return None

class DeadCodeElimination(OptimizationPass):
    """
    死代码消除优化
    
    移除永远不会执行的代码
    """
    
    def optimize(self, ast):
        """
        执行死代码消除优化
        
        Args:
            ast: 抽象语法树
        
        Returns:
            Node: 优化后的AST
        """
        return self._eliminate_dead_code(ast)
    
    def _eliminate_dead_code(self, node):
        """
        递归消除死代码
        
        Args:
            node: AST节点
        
        Returns:
            Node: 消除死代码后的节点
        """
        if hasattr(node, 'statements'):
            node.statements = [self._eliminate_dead_code(stmt) for stmt in node.statements if stmt is not None]
        
        if hasattr(node, 'body'):
            node.body = self._eliminate_dead_code(node.body)
        
        if hasattr(node, 'then_branch'):
            node.then_branch = self._eliminate_dead_code(node.then_branch)
        
        if hasattr(node, 'else_branch'):
            node.else_branch = self._eliminate_dead_code(node.else_branch)
        
        return node

class DeferredOperationsOptimization(OptimizationPass):
    """
    DeferredOperations优化
    
    当启用DeferredOperations特性时，优化 a+b-b 或 a-b+b 这样的模式
    """
    
    def optimize(self, ast):
        """
        执行DeferredOperations优化
        
        Args:
            ast: 抽象语法树
        
        Returns:
            Node: 优化后的AST
        """
        feature_manager = get_feature_manager()
        if not feature_manager.is_enabled('DeferredOperations'):
            return ast
        
        return self._optimize_deferred_operations(ast)
    
    def _optimize_deferred_operations(self, node):
        """
        递归优化DeferredOperations
        
        Args:
            node: AST节点
        
        Returns:
            Node: 优化后的节点
        """
        if node is None:
            return None
        
        # 处理二元表达式
        if isinstance(node, BinaryExpression):
            # 先递归处理子节点
            node.left = self._optimize_deferred_operations(node.left)
            node.right = self._optimize_deferred_operations(node.right)
            
            # 检查是否是 a+b-b 或 a-b+b 模式
            if self._is_cancellation_pattern(node):
                return self._simplify_cancellation(node)
            
            return node
        
        # 处理程序节点
        if hasattr(node, 'statements'):
            node.statements = [self._optimize_deferred_operations(stmt) for stmt in node.statements]
            return node
        
        # 处理表达式语句
        if hasattr(node, 'expression'):
            node.expression = self._optimize_deferred_operations(node.expression)
            return node
        
        # 递归处理所有子节点
        for attr_name in dir(node):
            if not attr_name.startswith('_'):
                attr_value = getattr(node, attr_name, None)
                if isinstance(attr_value, BinaryExpression):
                    setattr(node, attr_name, self._optimize_deferred_operations(attr_value))
                elif isinstance(attr_value, list):
                    setattr(node, attr_name, [self._optimize_deferred_operations(item) if isinstance(item, BinaryExpression) else item for item in attr_value])
        
        return node
    
    def _is_cancellation_pattern(self, node):
        """
        检查是否是抵消模式 (a+b-b 或 a-b+b)
        
        Args:
            node: 二元表达式节点
        
        Returns:
            bool: 是否是抵消模式
        """
        if not isinstance(node, BinaryExpression):
            return False
        
        # 检查是否是 a+b 或 a-b
        if node.operator not in ('+', '-'):
            return False
        
        # 检查左操作数是否是二元表达式
        if not isinstance(node.left, BinaryExpression):
            return False
        
        # 检查内层操作符
        inner_op = node.left.operator
        if inner_op not in ('+', '-'):
            return False
        
        # 检查操作符组合
        # (a+b)-b: outer=-, inner=+
        # (a-b)+b: outer=+, inner=-
        if (node.operator == '-' and inner_op == '+') or (node.operator == '+' and inner_op == '-'):
            # 检查左操作数的右操作数是否与右操作数相同
            if self._is_same_value(node.left.right, node.right):
                return True
        
        return False
    
    def _is_same_value(self, node1, node2):
        """
        检查两个节点是否表示相同的值
        
        Args:
            node1: 第一个节点
            node2: 第二个节点
        
        Returns:
            bool: 是否相同
        """
        # 如果都是字面量，比较值
        if isinstance(node1, LiteralExpression) and isinstance(node2, LiteralExpression):
            return node1.value == node2.value
        
        # 如果都是标识符，比较名称
        if hasattr(node1, 'name') and hasattr(node2, 'name'):
            return node1.name == node2.name
        
        # 其他情况，比较字符串表示
        return str(node1) == str(node2)
    
    def _simplify_cancellation(self, node):
        """
        简化抵消模式
        
        Args:
            node: 二元表达式节点
        
        Returns:
            Node: 简化后的节点
        """
        # (a+b)-b 或 (a-b)+b -> a
        return node.left.left
