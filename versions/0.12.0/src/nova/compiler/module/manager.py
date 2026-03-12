"""
Nova语言模块管理器
"""

import os
from typing import Dict, Optional

class Module:
    """
    模块类
    
    Attributes:
        name: 模块名称
        path: 模块路径
        ast: 模块的AST
        symbols: 模块导出的符号
        dependencies: 模块依赖
    """
    
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.ast = None
        self.symbols = {}
        self.dependencies = []

class ModuleManager:
    """
    模块管理器
    
    负责管理所有已加载的模块
    """
    
    def __init__(self):
        """
        初始化模块管理器
        """
        self.modules: Dict[str, Module] = {}
        self.search_paths = []
    
    def add_search_path(self, path: str):
        """
        添加模块搜索路径
        
        Args:
            path: 搜索路径
        """
        if os.path.isdir(path) and path not in self.search_paths:
            self.search_paths.append(path)
    
    def get_module(self, name: str) -> Optional[Module]:
        """
        获取模块
        
        Args:
            name: 模块名称
        
        Returns:
            Module: 模块对象，如果不存在则返回None
        """
        return self.modules.get(name)
    
    def register_module(self, module: Module):
        """
        注册模块
        
        Args:
            module: 模块对象
        """
        self.modules[module.name] = module
    
    def resolve_module_path(self, name: str) -> Optional[str]:
        """
        解析模块路径
        
        Args:
            name: 模块名称
        
        Returns:
            str: 模块路径，如果找不到则返回None
        """
        # 处理嵌套模块（如 std::io::file）
        parts = name.split('::')
        
        for search_path in self.search_paths:
            # 尝试作为单个文件
            module_path = os.path.join(search_path, f"{name}.nova")
            if os.path.isfile(module_path):
                return module_path
            
            # 尝试作为包（目录 + __init__.nova）
            module_path = os.path.join(search_path, *parts, "__init__.nova")
            if os.path.isfile(module_path):
                return module_path
            
            # 尝试作为目录中的文件
            if len(parts) > 1:
                module_path = os.path.join(search_path, *parts[:-1], f"{parts[-1]}.nova")
                if os.path.isfile(module_path):
                    return module_path
        
        return None
    
    def get_module_dependencies(self, module_name: str) -> list:
        """
        获取模块的依赖
        
        Args:
            module_name: 模块名称
        
        Returns:
            list: 依赖列表
        """
        module = self.get_module(module_name)
        if not module:
            return []
        return module.dependencies
    
    def check_circular_dependency(self, module_name: str) -> bool:
        """
        检查模块是否存在循环依赖
        
        Args:
            module_name: 模块名称
        
        Returns:
            bool: 如果存在循环依赖则返回True，否则返回False
        """
        visited = set()
        stack = set()
        
        def has_cycle(name):
            if name in stack:
                return True
            if name in visited:
                return False
            
            visited.add(name)
            stack.add(name)
            
            module = self.get_module(name)
            if module:
                for dep_name in module.dependencies:
                    if isinstance(dep_name, list):
                        dep_name = '.'.join(dep_name)
                    if has_cycle(dep_name):
                        return True
            
            stack.remove(name)
            return False
        
        return has_cycle(module_name)
