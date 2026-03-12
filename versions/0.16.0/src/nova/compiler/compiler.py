"""
Nova语言编译器
负责将Nova代码编译为可执行文件
"""

import os
import sys
import tempfile
import shutil
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.compiler.optimizer.optimizer import Optimizer
from nova.compiler.incremental import IncrementalCompiler
from nova.compiler.llvm_compiler import LLVMCompiler
from nova.compiler.parallel import ParallelCompiler, ParallelCompilerManager
from nova.vm.machine import VirtualMachine

class Compiler:
    """
    Nova语言编译器
    """
    
    def __init__(self):
        """
        初始化编译器
        """
        self.vm = VirtualMachine()
        self.optimizer = Optimizer()
        self.incremental_compiler = IncrementalCompiler()
        self.llvm_compiler = LLVMCompiler()
        self.parallel_compiler = ParallelCompilerManager.get_instance()
    
    def compile_to_bytecode(self, source_code, optimization_level=0):
        """
        将Nova源代码编译为字节码
        
        Args:
            source_code: Nova源代码
            optimization_level: 优化级别 (0-3)
        
        Returns:
            tuple: (指令列表, 常量列表)
        """
        # 词法分析
        scanner = Scanner(source_code)
        tokens = scanner.scan_tokens()
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 语义分析
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # 优化
        ast = self.optimizer.optimize(ast, optimization_level)
        
        # 代码生成
        generator = CodeGenerator()
        instructions, constants = generator.generate(ast)
        
        return instructions, constants
    
    def compile_to_python(self, source_code, output_path, optimization_level=0):
        """
        将Nova源代码编译为Python可执行文件
        
        Args:
            source_code: Nova源代码
            output_path: 输出文件路径
            optimization_level: 优化级别 (0-3)
        """
        # 编译为字节码
        instructions, constants = self.compile_to_bytecode(source_code, optimization_level)
        
        # 生成Python包装器
        python_code = self._generate_python_wrapper(instructions, constants)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        # 设置可执行权限（Unix-like系统）
        if os.name != 'nt':
            os.chmod(output_path, 0o755)
    
    def compile_to_executable(self, source_code, output_path, optimization_level=0):
        """
        将Nova源代码编译为独立可执行文件
        
        Args:
            source_code: Nova源代码
            output_path: 输出文件路径
            optimization_level: 优化级别 (0-3)
        """
        # 编译为字节码
        instructions, constants = self.compile_to_bytecode(source_code, optimization_level)
        
        # 生成Python包装器
        python_code = self._generate_python_wrapper(instructions, constants)
        
        # 创建临时Python文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(python_code)
            tmp_file_path = tmp_file.name
        
        try:
            # 使用PyInstaller或py2exe打包
            # 这里使用Python解释器作为可执行文件
            python_exe = sys.executable
            
            # 创建可执行脚本
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"#!{python_exe}\n")
                f.write(python_code)
            
            # 设置可执行权限（Unix-like系统）
            if os.name != 'nt':
                os.chmod(output_path, 0o755)
            
            print(f"编译成功: {output_path}")
            print(f"使用方法: {output_path}")
            
        finally:
            # 清理临时文件
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
    
    def compile_file_incrementally(self, file_path):
        """
        增量编译单个文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            tuple: (指令列表, 常量列表)
        """
        return self.incremental_compiler.compile_file(file_path)
    
    def compile_project_incrementally(self, main_file):
        """
        增量编译整个项目
        
        Args:
            main_file: 主文件路径
        
        Returns:
            tuple: (指令列表, 常量列表)
        """
        return self.incremental_compiler.compile_project(main_file)
    
    def _generate_python_wrapper(self, instructions, constants):
        """
        生成Python包装器代码
        
        Args:
            instructions: 指令列表
            constants: 常量列表
        
        Returns:
            str: Python代码
        """
        code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova语言编译生成的可执行文件
"""

import sys
import os

# 添加Nova库路径
nova_path = os.path.join(os.path.dirname(__file__), 'src', 'nova')
if os.path.exists(nova_path):
    sys.path.insert(0, os.path.dirname(os.path.dirname(nova_path)))

from nova.vm.machine import VirtualMachine

def main():
    """
    主函数
    """
    vm = VirtualMachine()
    
    # 加载指令
    instructions = []
'''
        
        # 添加指令
        for instr in instructions:
            code += f"    instructions.append({repr(instr)})\n"
        
        code += '''
    
    # 执行程序
    try:
        vm.load(instructions)
        result = vm.run()
        if result is not None:
            print(result)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
        
        return code
    
    def run(self, source_code):
        """
        直接运行Nova代码
        
        Args:
            source_code: Nova源代码
        
        Returns:
            Any: 执行结果
        """
        # 编译为字节码
        instructions, constants = self.compile_to_bytecode(source_code)
        
        # 执行
        self.vm.load(instructions)
        return self.vm.run()
    
    def compile_to_llvm_ir(self, source_code, optimization_level=0):
        """
        将Nova源代码编译为LLVM IR
        
        Args:
            source_code: Nova源代码
            optimization_level: 优化级别 (0-3)
        
        Returns:
            str: LLVM IR字符串
        """
        return self.llvm_compiler.compile_to_llvm_ir(source_code, optimization_level)
    
    def jit_compile_and_run(self, source_code, optimization_level=0):
        """
        使用LLVM JIT编译并运行Nova代码
        
        Args:
            source_code: Nova源代码
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Any: 执行结果
        """
        return self.llvm_compiler.jit_compile_and_run(source_code, optimization_level)
    
    def compile_files_parallel(self, file_paths, optimization_level=0):
        """
        并行编译多个文件
        
        Args:
            file_paths: 文件路径列表
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Dict[str, Tuple[List, List]]: 文件名到(指令列表, 常量列表)的映射
        """
        return self.parallel_compiler.compile_files(file_paths, optimization_level)
    
    def compile_project_parallel(self, main_file, optimization_level=0):
        """
        并行编译整个项目
        
        Args:
            main_file: 主文件路径
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Tuple[List, List]: (指令列表, 常量列表)
        """
        return self.parallel_compiler.compile_project(main_file, optimization_level)
    
    def gpu_accelerate(self, instructions):
        """
        使用GPU加速编译后的指令
        
        Args:
            instructions: 指令列表
        
        Returns:
            List: 加速后的指令列表
        """
        return self.parallel_compiler.gpu_accelerate(instructions)
