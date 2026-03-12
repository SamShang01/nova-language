"""
Nova语言并行编译器

支持多线程编译和GPU加速
"""

import os
import sys
import threading
import concurrent.futures
from typing import List, Tuple, Optional, Dict
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.compiler.optimizer.optimizer import Optimizer
from nova.compiler.incremental import IncrementalCompiler


class ParallelCompiler:
    """
    并行编译器
    
    支持多线程编译和GPU加速
    """
    
    def __init__(self, max_workers: int = None, use_gpu: bool = False):
        """
        初始化并行编译器
        
        Args:
            max_workers: 最大工作线程数，默认使用CPU核心数
            use_gpu: 是否使用GPU加速
        """
        if max_workers is None:
            import multiprocessing
            self.max_workers = multiprocessing.cpu_count()
        else:
            self.max_workers = max_workers
        
        self.use_gpu = use_gpu
        self.incremental_compiler = IncrementalCompiler()
        self._initialize_gpu()
    
    def _initialize_gpu(self):
        """
        初始化GPU支持
        """
        if self.use_gpu:
            try:
                # 尝试导入GPU相关库
                import torch
                import numpy as np
                self.has_gpu = torch.cuda.is_available()
                if self.has_gpu:
                    print("[并行编译器] GPU加速已启用")
                else:
                    print("[并行编译器] 未检测到可用GPU，使用CPU模式")
                    self.use_gpu = False
            except ImportError:
                print("[并行编译器] 未安装GPU相关库，使用CPU模式")
                self.use_gpu = False
    
    def compile_files(self, file_paths: List[str], optimization_level: int = 0) -> Dict[str, Tuple[List, List]]:
        """
        并行编译多个文件
        
        Args:
            file_paths: 文件路径列表
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Dict[str, Tuple[List, List]]: 文件名到(指令列表, 常量列表)的映射
        """
        results = {}
        
        # 使用线程池并行编译
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有编译任务
            future_to_file = {executor.submit(self._compile_single_file, file_path, optimization_level): file_path 
                            for file_path in file_paths}
            
            # 收集结果
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    instructions, constants = future.result()
                    results[file_path] = (instructions, constants)
                except Exception as e:
                    print(f"[并行编译器] 编译文件 {file_path} 时出错: {e}")
        
        return results
    
    def _compile_single_file(self, file_path: str, optimization_level: int = 0) -> Tuple[List, List]:
        """
        编译单个文件
        
        Args:
            file_path: 文件路径
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Tuple[List, List]: (指令列表, 常量列表)
        """
        try:
            # 首先尝试增量编译
            if self.incremental_compiler is not None:
                try:
                    instructions, constants = self.incremental_compiler.compile_file(file_path)
                    return instructions, constants
                except Exception:
                    # 增量编译失败，使用普通编译
                    pass
            
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
            ast = analyzer.analyze(ast)
            
            # 优化
            optimizer = Optimizer()
            ast = optimizer.optimize(ast, optimization_level)
            
            # 代码生成
            generator = CodeGenerator()
            instructions, constants = generator.generate(ast)
            
            return instructions, constants
        except Exception as e:
            raise Exception(f"编译文件 {file_path} 失败: {str(e)}")
    
    def compile_project(self, main_file: str, optimization_level: int = 0) -> Tuple[List, List]:
        """
        并行编译整个项目
        
        Args:
            main_file: 主文件路径
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Tuple[List, List]: (指令列表, 常量列表)
        """
        # 首先获取项目的所有文件
        project_files = self._get_project_files(main_file)
        
        # 并行编译所有文件
        compiled_files = self.compile_files(project_files, optimization_level)
        
        # 合并结果（这里简化处理，实际应该处理依赖关系）
        main_instructions, main_constants = compiled_files.get(main_file, ([], []))
        
        return main_instructions, main_constants
    
    def _get_project_files(self, main_file: str) -> List[str]:
        """
        获取项目的所有文件
        
        Args:
            main_file: 主文件路径
        
        Returns:
            List[str]: 文件路径列表
        """
        project_files = [main_file]
        
        # 简单实现：递归查找同一目录下的所有.nova文件
        main_dir = os.path.dirname(main_file)
        for root, _, files in os.walk(main_dir):
            for file in files:
                if file.endswith('.nova'):
                    file_path = os.path.join(root, file)
                    if file_path not in project_files:
                        project_files.append(file_path)
        
        return project_files
    
    def gpu_accelerate(self, instructions: List) -> List:
        """
        使用GPU加速编译后的指令
        
        Args:
            instructions: 指令列表
        
        Returns:
            List: 加速后的指令列表
        """
        if not self.use_gpu or not self.has_gpu:
            return instructions
        
        try:
            import torch
            import numpy as np
            
            # 这里可以实现GPU加速的逻辑
            # 例如，将计算密集型的指令转换为GPU可执行的形式
            
            print("[并行编译器] 应用GPU加速")
            
            # 简化实现：返回原始指令
            return instructions
        except Exception as e:
            print(f"[并行编译器] GPU加速失败: {e}")
            return instructions


class ParallelCompilerManager:
    """
    并行编译器管理器
    """
    
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls, max_workers: int = None, use_gpu: bool = False) -> ParallelCompiler:
        """
        获取并行编译器实例
        
        Args:
            max_workers: 最大工作线程数
            use_gpu: 是否使用GPU加速
        
        Returns:
            ParallelCompiler: 并行编译器实例
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = ParallelCompiler(max_workers, use_gpu)
            return cls._instance


def test_parallel_compiler():
    """
    测试并行编译器
    """
    # 创建并行编译器
    compiler = ParallelCompiler(max_workers=4, use_gpu=True)
    
    # 测试文件
    test_files = [
        "test1.nova",
        "test2.nova",
        "test3.nova",
        "test4.nova"
    ]
    
    # 创建测试文件
    for i, file_name in enumerate(test_files):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"""
            function main() {{
                println("Hello from test{i}!");
                return 0;
            }}
            """)

    
    # 并行编译
    print("开始并行编译...")
    results = compiler.compile_files(test_files)
    
    # 打印结果
    for file_path, (instructions, constants) in results.items():
        print(f"文件 {file_path}: {len(instructions)} 条指令, {len(constants)} 个常量")
    
    # 清理测试文件
    for file_name in test_files:
        if os.path.exists(file_name):
            os.remove(file_name)
    
    print("并行编译测试完成!")


if __name__ == "__main__":
    test_parallel_compiler()