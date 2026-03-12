"""
Nova语言语义分析器
"""

from .analyzer import SemanticAnalyzer
from .symbols import Symbol, VariableSymbol, FunctionSymbol, TypeSymbol
from .types import Type, PrimitiveType, StructType, EnumType, TraitType
from .scope import Scope
from .errors import SemanticError

__all__ = [
    'SemanticAnalyzer',
    'Symbol',
    'VariableSymbol',
    'FunctionSymbol',
    'TypeSymbol',
    'Type',
    'PrimitiveType',
    'StructType',
    'EnumType',
    'TraitType',
    'Scope',
    'SemanticError'
]
