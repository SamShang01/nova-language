"""
Nova语言增量编译器
负责增量编译，只编译修改的文件
"""

import os
import time
import pickle
from typing import Dict, Optional, Tuple, Set
from nova.compiler.module.manager import ModuleManager, Module
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

class IncrementalCompiler:
    """
    增量编译器
    
    负责跟踪文件修改时间和编译缓存，只编译修改的文件
    """
    
    def __init__(self, cache_dir: str = ".nova_cache"):
        """
        初始化增量编译器
        
        Args:
            cache_dir: 缓存目录
        """
        self.module_manager = ModuleManager()
        self.cache_dir = cache_dir
        self._ensure_cache_dir()
        self._load_cache()
    
    def _ensure_cache_dir(self):
        """
        确保缓存目录存在
        """
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _load_cache(self):
        """
        加载编译缓存
        """
        cache_file = os.path.join(self.cache_dir, "compile_cache.pkl")
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                try:
                    cache_data = pickle.load(f)
                    self.file_mtimes = cache_data.get('file_mtimes', {})
                    self.module_cache = cache_data.get('module_cache', {})
                    self.dependency_graph = cache_data.get('dependency_graph', {})
                except:
                    # 缓存文件损坏，重新初始化
                    self.file_mtimes = {}
                    self.module_cache = {}
                    self.dependency_graph = {}
        else:
            self.file_mtimes = {}
            self.module_cache = {}
            self.dependency_graph = {}
    
    def _save_cache(self):
        """
        保存编译缓存
        """
        cache_file = os.path.join(self.cache_dir, "compile_cache.pkl")
        cache_data = {
            'file_mtimes': self.file_mtimes,
            'module_cache': self.module_cache,
            'dependency_graph': self.dependency_graph
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cache_data, f)
    
    def _get_file_mtime(self, file_path: str) -> float:
        """
        获取文件的修改时间
        
        Args:
            file_path: 文件路径
        
        Returns:
            float: 修改时间戳
        """
        try:
            return os.path.getmtime(file_path)
        except:
            return 0
    
    def _is_file_modified(self, file_path: str) -> bool:
        """
        检查文件是否被修改
        
        Args:
            file_path: 文件路径
        
        Returns:
            bool: 如果文件被修改返回True
        """
        current_mtime = self._get_file_mtime(file_path)
        cached_mtime = self.file_mtimes.get(file_path, 0)
        return current_mtime > cached_mtime
    
    def _update_file_mtime(self, file_path: str):
        """
        更新文件的修改时间
        
        Args:
            file_path: 文件路径
        """
        self.file_mtimes[file_path] = self._get_file_mtime(file_path)
    
    def _get_dependencies(self, file_path: str) -> Set[str]:
        """
        获取文件的依赖
        
        Args:
            file_path: 文件路径
        
        Returns:
            Set[str]: 依赖文件集合
        """
        return self.dependency_graph.get(file_path, set())
    
    def _set_dependencies(self, file_path: str, dependencies: Set[str]):
        """
        设置文件的依赖
        
        Args:
            file_path: 文件路径
            dependencies: 依赖文件集合
        """
        self.dependency_graph[file_path] = dependencies
    
    def compile_file(self, file_path: str) -> Tuple[list, list]:
        """
        编译单个文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            tuple: (指令列表, 常量列表)
        """
        # 检查文件是否被修改或依赖是否被修改
        if not self._is_file_modified(file_path):
            # 检查依赖是否被修改
            dependencies = self._get_dependencies(file_path)
            if not any(self._is_file_modified(dep) for dep in dependencies):
                # 使用缓存的编译结果
                if file_path in self.module_cache:
                    print(f"[增量编译] 使用缓存: {file_path}")
                    return self.module_cache[file_path]
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # 词法分析
        scanner = Scanner(source_code)
        tokens = scanner.scan_tokens()
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 语义分析
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # 代码生成
        generator = CodeGenerator()
        instructions, constants = generator.generate(ast)
        
        # 缓存编译结果
        self.module_cache[file_path] = (instructions, constants)
        self._update_file_mtime(file_path)
        
        # 提取依赖（这里简化处理，实际需要从AST中提取import语句）
        dependencies = self._extract_dependencies(source_code)
        self._set_dependencies(file_path, dependencies)
        
        # 保存缓存
        self._save_cache()
        
        print(f"[增量编译] 重新编译: {file_path}")
        return instructions, constants
    
    def _extract_dependencies(self, source_code: str) -> Set[str]:
        """
        从源代码中提取依赖
        
        Args:
            source_code: 源代码
        
        Returns:
            Set[str]: 依赖文件集合
        """
        dependencies = set()
        # 简单的依赖提取逻辑，实际需要解析import语句
        lines = source_code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('import '):
                # 提取导入的模块名
                module_name = line[7:].strip()
                if module_name:
                    # 尝试解析模块路径
                    module_path = self.module_manager.resolve_module_path(module_name)
                    if module_path:
                        dependencies.add(module_path)
        return dependencies
    
    def compile_project(self, main_file: str) -> Tuple[list, list]:
        """
        编译整个项目
        
        Args:
            main_file: 主文件路径
        
        Returns:
            tuple: (指令列表, 常量列表)
        """
        # 编译主文件及其依赖
        instructions, constants = self.compile_file(main_file)
        
        # 保存缓存
        self._save_cache()
        
        return instructions, constants
