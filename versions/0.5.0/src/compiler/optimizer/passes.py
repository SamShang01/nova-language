"""
Nova语言代码优化Pass
"""

from nova.compiler.parser.ast import BinaryExpression, LiteralExpression

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
            if operator == 'PLUS':
                return LiteralExpression(left.line, left.column, left.value + right.value, type(left.value).__name__)
            elif operator == 'MINUS':
                return LiteralExpression(left.line, left.column, left.value - right.value, type(left.value).__name__)
            elif operator == 'MULTIPLY':
                return LiteralExpression(left.line, left.column, left.value * right.value, type(left.value).__name__)
            elif operator == 'DIVIDE':
                if right.value != 0:
                    return LiteralExpression(left.line, left.column, left.value / right.value, type(left.value).__name__)
            elif operator == 'MODULO':
                if right.value != 0:
                    return LiteralExpression(left.line, left.column, left.value % right.value, type(left.value).__name__)
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
