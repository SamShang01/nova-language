"""
Nova语言模块解析器
"""

from typing import List, Optional
from nova.compiler.parser.parser import Parser
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.module.manager import Module

class ModuleResolver:
    """
    模块解析器
    
    负责解析模块文件并生成AST
    """
    
    def __init__(self, module_manager):
        """
        初始化模块解析器
        
        Args:
            module_manager: 模块管理器
        """
        self.module_manager = module_manager
    
    def resolve(self, module_name: str) -> Optional[Module]:
        """
        解析模块
        
        Args:
            module_name: 模块名称
        
        Returns:
            Module: 解析后的模块，如果失败则返回None
        """
        module_path = self.module_manager.resolve_module_path(module_name)
        if not module_path:
            return None
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            scanner = Scanner(source)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            ast = parser.parse()
            
            module = Module(module_name, module_path)
            module.ast = ast
            
            self._extract_dependencies(module, ast)
            self._extract_symbols(module, ast)
            
            return module
        except Exception as e:
            print(f"Error resolving module {module_name}: {e}")
            return None
    
    def _extract_dependencies(self, module: Module, ast):
        """
        提取模块依赖
        
        Args:
            module: 模块对象
            ast: 抽象语法树
        """
        from ..parser.ast import ImportStatement
        
        for statement in ast.statements:
            if isinstance(statement, ImportStatement):
                # 将路径列表转换为模块名称字符串
                if isinstance(statement.path, list):
                    module_name = '.'.join(statement.path)
                else:
                    module_name = statement.path
                module.dependencies.append(module_name)
    
    def _extract_symbols(self, module: Module, ast):
        """
        提取模块导出的符号
        
        Args:
            module: 模块对象
            ast: 抽象语法树
        """
        from ..parser.ast import FunctionDefinition, VariableDeclaration, ConstantDeclaration, StructDefinition, TraitDefinition
        
        for statement in ast.statements:
            if isinstance(statement, FunctionDefinition):
                module.symbols[statement.name] = 'function'
            elif isinstance(statement, VariableDeclaration):
                module.symbols[statement.name] = 'variable'
            elif isinstance(statement, ConstantDeclaration):
                module.symbols[statement.name] = 'constant'
            elif isinstance(statement, StructDefinition):
                module.symbols[statement.name] = 'struct'
            elif isinstance(statement, TraitDefinition):
                module.symbols[statement.name] = 'trait'
