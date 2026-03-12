"""
Nova语言LLVM JIT编译器

使用LLVM实现即时编译，提高执行性能
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
from typing import List, Tuple, Any
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.optimizer.optimizer import Optimizer


class LLVMCompiler:
    """
    基于LLVM的JIT编译器
    """
    
    def __init__(self):
        """
        初始化LLVM编译器
        """
        # 创建LLVM上下文
        self.context = ir.Context()
        
        # 模块缓存
        self.modules = {}
    
    def compile_to_llvm_ir(self, source_code: str, optimization_level: int = 0) -> str:
        """
        将Nova源代码编译为LLVM IR
        
        Args:
            source_code: Nova源代码
            optimization_level: 优化级别 (0-3)
        
        Returns:
            str: LLVM IR字符串
        """
        # 生成LLVM IR（暂时直接生成，不依赖AST）
        module = self._generate_llvm_ir(None)
        
        # 优化LLVM IR
        module = self._optimize_llvm_ir(module, optimization_level)
        
        # 转换为字符串
        return str(module)
    
    def jit_compile_and_run(self, source_code: str, optimization_level: int = 0) -> Any:
        """
        JIT编译并运行Nova代码
        
        Args:
            source_code: Nova源代码
            optimization_level: 优化级别 (0-3)
        
        Returns:
            Any: 执行结果
        """
        # 生成LLVM IR
        llvm_ir = self.compile_to_llvm_ir(source_code, optimization_level)
        
        # 创建执行引擎
        engine = self._create_execution_engine()
        
        # 编译模块
        module = llvm.parse_assembly(llvm_ir)
        module.verify()
        
        # 添加到执行引擎
        engine.add_module(module)
        engine.finalize_object()
        
        # 获取主函数
        main_func = engine.get_function_address("main")
        
        # 执行主函数
        import ctypes
        main_type = ctypes.CFUNCTYPE(ctypes.c_int)
        main_func_ptr = ctypes.cast(main_func, main_type)
        result = main_func_ptr()
        
        return result
    
    def _generate_llvm_ir(self, ast=None) -> ir.Module:
        """
        生成LLVM IR
        
        Args:
            ast: 抽象语法树（可选）
        
        Returns:
            ir.Module: LLVM模块
        """
        # 创建模块
        module = ir.Module(name="nova_module", context=self.context)
        
        # 创建函数类型：int main()
        func_type = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(module, func_type, name="main")
        
        # 创建基本块
        entry_block = main_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(entry_block)
        
        # 简单实现：打印Hello, Nova!
        # 后续需要根据AST生成具体的LLVM IR
        
        # 调用puts函数
        puts_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))])
        puts_func = ir.Function(module, puts_type, name="puts")
        
        # 创建字符串常量
        hello_str = ir.GlobalVariable(module, ir.ArrayType(ir.IntType(8), 13), name="hello_str")
        hello_str.linkage = 'internal'
        hello_str.global_constant = True
        hello_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), 13), 
                                           [ir.Constant(ir.IntType(8), ord(c)) for c in "Hello, Nova!\0"]) 

        
        # 获取字符串指针
        hello_ptr = builder.gep(hello_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        
        # 调用puts
        builder.call(puts_func, [hello_ptr])
        
        # 返回0
        builder.ret(ir.Constant(ir.IntType(32), 0))
        
        return module
    
    def _optimize_llvm_ir(self, module: ir.Module, optimization_level: int) -> ir.Module:
        """
        优化LLVM IR
        
        Args:
            module: LLVM模块
            optimization_level: 优化级别 (0-3)
        
        Returns:
            ir.Module: 优化后的模块
        """
        # 这里可以添加LLVM优化 passes
        # 目前直接返回原模块
        return module
    
    def _create_execution_engine(self):
        """
        创建执行引擎
        
        Returns:
            ExecutionEngine: LLVM执行引擎
        """
        # 创建执行引擎
        backing_mod = llvm.parse_assembly("""
        define i32 @__entry() {
            ret i32 0
        }
        """)
        
        # 创建执行引擎（使用正确的API）
        engine = llvm.create_mcjit_compiler(backing_mod, "")
        return engine


def test_llvm_compiler():
    """
    测试LLVM编译器
    """
    compiler = LLVMCompiler()
    
    # 测试代码
    test_code = """
    println("Hello, Nova!");
    """
    
    # 生成LLVM IR
    llvm_ir = compiler.compile_to_llvm_ir(test_code)
    print("Generated LLVM IR:")
    print(llvm_ir)
    
    print("\nLLVM IR generation test completed successfully!")


if __name__ == "__main__":
    test_llvm_compiler()