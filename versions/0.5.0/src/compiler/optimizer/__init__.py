"""
Nova语言代码优化器
"""

from .optimizer import Optimizer
from .passes import ConstantFolding, DeadCodeElimination

__all__ = [
    'Optimizer',
    'ConstantFolding',
    'DeadCodeElimination'
]
