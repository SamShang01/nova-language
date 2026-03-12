# 调试虚拟机执行
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

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

# 创建虚拟机并执行
vm = VirtualMachine()
vm.load(instructions, constants)

# 手动执行指令，打印每一步的状态
print("=== Manual Execution ===")
from nova.vm.instructions import JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE, CALL_FUNCTION, RETURN_VALUE

jump_instruction_types = (JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE)

vm.running = True
step = 0
while vm.running and step < 50:  # 限制步数防止无限循环
    if vm.pc >= len(vm.instructions):
        vm.running = False
        break
    
    instruction = vm.instructions[vm.pc]
    print(f"\nStep {step}: PC={vm.pc}, Stack={vm.stack}")
    print(f"  Instruction: {instruction.name if hasattr(instruction, 'name') else instruction}")
    
    try:
        instruction.execute(vm)
        print(f"  After execution: Stack={vm.stack}")
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        break
    
    # 除了跳转指令，其他指令自动递增PC
    if not isinstance(instruction, jump_instruction_types):
        vm.pc += 1
    
    step += 1

print(f"\n=== Final Result ===")
print(f"Stack: {vm.stack}")
print(f"Environment: {vm.environment}")
