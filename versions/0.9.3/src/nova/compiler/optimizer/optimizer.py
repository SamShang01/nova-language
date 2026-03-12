"""
Nova语言代码优化器主模块
"""

from nova.compiler.parser.ast import Node
from nova.compiler.optimizer.passes import ConstantFolding, DeadCodeElimination, DeferredOperationsOptimization

class Optimizer:
    """
    代码优化器
    
    负责对AST进行各种优化
    """
    
    def __init__(self):
        """
        初始化优化器
        """
        self.passes = [
            DeferredOperationsOptimization(),
            ConstantFolding(),
            DeadCodeElimination()
        ]
    
    def optimize(self, ast):
        """
        优化AST
        
        Args:
            ast: 抽象语法树
        
        Returns:
            Node: 优化后的AST
        """
        optimized_ast = ast
        
        for pass_ in self.passes:
            optimized_ast = pass_.optimize(optimized_ast)
        
        return optimized_ast
    
    def add_pass(self, pass_):
        """
        添加优化pass
        
        Args:
            pass_: 优化pass
        """
        self.passes.append(pass_)
    
    def remove_pass(self, pass_name):
        """
        移除优化pass
        
        Args:
            pass_name: 优化pass名称
        """
        self.passes = [p for p in self.passes if p.__class__.__name__ != pass_name]
