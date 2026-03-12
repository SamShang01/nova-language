# 调试参数绑定
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine, NovaFunction
from nova.vm.instructions import LOAD_CONST, LOAD_NAME, COMPARE_LT, JUMP_IF_FALSE, RETURN_VALUE

code = """
template func myMin<T>(a: T, b: T): T {
    if a < b {
        return a;
    }
    return b;
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

# 获取myMin函数
myMin_func = None
for instr in instructions:
    if isinstance(instr, LOAD_CONST):
        func = instr.args[0]
        if isinstance(func, NovaFunction) and func.name == 'myMin':
            myMin_func = func
            break

if myMin_func:
    print(f"=== Function: {myMin_func.name} ===")
    print(f"Params: {myMin_func.params}")
    print(f"Normal params: {myMin_func.normal_params}")
    
    # 手动调用函数
    print(f"\n=== Calling myMin(10, 20) ===")
    
    # 创建虚拟机
    vm = VirtualMachine()
    
    # 绑定参数
    vm.environment['a'] = 10
    vm.environment['b'] = 20
    
    print(f"Environment: {vm.environment}")
    
    # 加载指令
    vm.load(myMin_func.instructions)
    
    # 手动执行
    from nova.vm.instructions import JUMP, JUMP_IF_TRUE
    jump_instruction_types = (JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE)
    
    vm.running = True
    step = 0
    
    while vm.running and step < 15:
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
            import traceback
            traceback.print_exc()
            break
        
        if not isinstance(instruction, jump_instruction_types):
            vm.pc += 1
        
        step += 1
    
    print(f"\n=== Final Result ===")
    print(f"Stack: {vm.stack}")
    if vm.stack:
        print(f"Result: {vm.stack[-1]}")
