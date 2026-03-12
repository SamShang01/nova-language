# 调试虚拟机执行 - 跟踪myMin函数
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine, NovaFunction
from nova.vm.instructions import JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE, CALL_FUNCTION, RETURN_VALUE

# 自定义NovaFunction来跟踪执行
class DebugNovaFunction(NovaFunction):
    def __call__(self, *args, **kwargs):
        print(f"\n=== Calling function '{self.name}' with args={args} ===")
        print(f"Function instructions:")
        for i, instr in enumerate(self.instructions):
            name = instr.name if hasattr(instr, 'name') else str(instr)
            args_str = f" {instr.args}" if hasattr(instr, 'args') and instr.args else ""
            print(f"  {i}: {name}{args_str}")
        
        # 创建一个新的虚拟机实例来执行函数体
        from nova.vm.machine import VirtualMachine
        func_vm = VirtualMachine()
        
        # 复制环境
        if self.environment:
            func_vm.environment.update(self.environment)
        
        # 处理位置参数
        used_args = 0
        if args and hasattr(args[0], 'nova_class'):
            func_vm.environment['this'] = args[0]
            used_args = 1
        
        for param_name, param_type in self.normal_params:
            if used_args < len(args):
                func_vm.environment[param_name] = args[used_args]
                used_args += 1
            elif param_name in self.default_values:
                func_vm.environment[param_name] = self.default_values[param_name]
            elif param_name in self.mandatory_params:
                raise TypeError(f"Missing mandatory argument '{param_name}' for function '{self.name}'")
            else:
                func_vm.environment[param_name] = None
        
        print(f"Environment after binding: {func_vm.environment}")
        
        # 手动执行指令
        func_vm.load(self.instructions)
        
        jump_instruction_types = (JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE)
        func_vm.running = True
        step = 0
        
        while func_vm.running and step < 20:
            if func_vm.pc >= len(func_vm.instructions):
                func_vm.running = False
                break
            
            instruction = func_vm.instructions[func_vm.pc]
            print(f"\n  Step {step}: PC={func_vm.pc}, Stack={func_vm.stack}")
            name = instruction.name if hasattr(instruction, 'name') else str(instruction)
            args_str = f" {instruction.args}" if hasattr(instruction, 'args') and instruction.args else ""
            print(f"    Instruction: {name}{args_str}")
            
            try:
                instruction.execute(func_vm)
                print(f"    After: Stack={func_vm.stack}")
            except Exception as e:
                print(f"    ERROR: {e}")
                import traceback
                traceback.print_exc()
                break
            
            if not isinstance(instruction, jump_instruction_types):
                func_vm.pc += 1
            
            step += 1
        
        result = func_vm.stack[-1] if func_vm.stack else None
        print(f"\n=== Function '{self.name}' returned: {result} ===")
        return result

code = """
template func myMin<T>(a: T, b: T): T {
    if a < b {
        return a;
    }
    return b;
}

func main() {
    let result = myMin<int>(10, 20);
    print(result);
}
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 解析代码
parser = Parser(tokens)
ast = parser.parse()

# 语义分析
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

# 代码生成
generator = CodeGenerator()
instructions, constants = generator.generate(ast)

# 替换NovaFunction为DebugNovaFunction
for i, instr in enumerate(instructions):
    if hasattr(instr, 'name') and instr.name == 'LOAD_CONST':
        if instr.args and isinstance(instr.args[0], NovaFunction):
            func = instr.args[0]
            # 创建DebugNovaFunction
            debug_func = DebugNovaFunction(
                func.name,
                func.instructions,
                func.params,
                func.is_async,
                func.environment
            )
            instr.args = (debug_func,)

# 创建虚拟机并执行
print("=== Starting Execution ===")
vm = VirtualMachine()
vm.load(instructions, constants)

# 手动执行主指令
jump_instruction_types = (JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE)
vm.running = True
step = 0

while vm.running and step < 10:
    if vm.pc >= len(vm.instructions):
        vm.running = False
        break
    
    instruction = vm.instructions[vm.pc]
    print(f"\nStep {step}: PC={vm.pc}, Stack={vm.stack}")
    name = instruction.name if hasattr(instruction, 'name') else str(instruction)
    args_str = f" {instruction.args}" if hasattr(instruction, 'args') and instruction.args else ""
    print(f"  Instruction: {name}{args_str}")
    
    try:
        instruction.execute(vm)
        print(f"  After: Stack={vm.stack}")
    except Exception as e:
        print(f"  ERROR: {e}")
        break
    
    if not isinstance(instruction, jump_instruction_types):
        vm.pc += 1
    
    step += 1

print(f"\n=== Final Result ===")
print(f"Stack: {vm.stack}")
