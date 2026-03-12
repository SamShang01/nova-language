"""
Nova语言模块导入器
"""

from typing import Optional
from .manager import ModuleManager
from .resolver import ModuleResolver

class ModuleImporter:
    """
    模块导入器
    
    负责导入和管理模块
    """
    
    def __init__(self, module_manager: ModuleManager):
        """
        初始化模块导入器
        
        Args:
            module_manager: 模块管理器
        """
        self.module_manager = module_manager
        self.resolver = ModuleResolver(module_manager)
    
    def import_module(self, module_name: str, alias: Optional[str] = None):
        """
        导入模块
        
        Args:
            module_name: 模块名称
            alias: 模块别名（可选）
        
        Returns:
            Module: 导入的模块，如果失败则返回None
        """
        module = self.module_manager.get_module(module_name)
        
        if module is None:
            module = self.resolver.resolve(module_name)
            
            if module is None:
                print(f"Error: Module '{module_name}' not found")
                return None
            
            self.module_manager.register_module(module)
            
            if self.module_manager.check_circular_dependency(module_name):
                print(f"Error: Circular dependency detected for module '{module_name}'")
                return None
        
        return module
    
    def import_symbol(self, module_name: str, symbol_name: str):
        """
        从模块导入特定符号
        
        Args:
            module_name: 模块名称
            symbol_name: 符号名称
        
        Returns:
            tuple: (模块, 符号类型)，如果失败则返回None
        """
        # 处理嵌套模块路径
        if '::' in module_name:
            # 对于嵌套模块，解析到最内层模块
            parts = module_name.split('::')
            current_module = None
            
            # 从根模块开始，逐级导入
            for i in range(1, len(parts) + 1):
                current_module_name = '::'.join(parts[:i])
                current_module = self.import_module(current_module_name)
                
                if current_module is None:
                    return None
        else:
            current_module = self.import_module(module_name)
        
        if current_module is None:
            return None
        
        symbol_type = current_module.symbols.get(symbol_name)
        
        if symbol_type is None:
            print(f"Error: Symbol '{symbol_name}' not found in module '{module_name}'")
            return None
        
        return (current_module, symbol_type)
