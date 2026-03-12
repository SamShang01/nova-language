# 调试虚拟机执行 - 简化版本
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine, NovaFunction
from nova.vm.instructions import LOAD_CONST

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

# 检查LOAD_CONST指令
print("=== Checking LOAD_CONST instructions ===")
for i, instr in enumerate(instructions):
    if isinstance(instr, LOAD_CONST):
        func = instr.args[0]
        print(f"\nInstruction {i}: LOAD_CONST")
        print(f"  Type: {type(func).__name__}")
        print(f"  Name: {func.name if hasattr(func, 'name') else 'N/A'}")
        print(f"  Is NovaFunction: {isinstance(func, NovaFunction)}")
        
        if hasattr(func, 'instructions'):
            print(f"  Instructions:")
            for j, func_instr in enumerate(func.instructions):
                name = func_instr.name if hasattr(func_instr, 'name') else str(func_instr)
                print(f"    {j}: {name}")
