# 调试标签解析
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import NovaFunction
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

# 检查主指令中的跳转目标
print("=== Main Instructions ===")
for i, instr in enumerate(instructions):
    opcode = instr.opcode if hasattr(instr, 'opcode') else str(instr)
    args = instr.args if hasattr(instr, 'args') else ()
    print(f"{i}: {opcode} {args}")

# 检查函数中的指令
print("\n=== Function Instructions ===")
for instr in instructions:
    if isinstance(instr, LOAD_CONST):
        func = instr.args[0]
        if isinstance(func, NovaFunction):
            print(f"\nFunction: {func.name}")
            for i, func_instr in enumerate(func.instructions):
                opcode = func_instr.opcode if hasattr(func_instr, 'opcode') else str(func_instr)
                args = func_instr.args if hasattr(func_instr, 'args') else ()
                print(f"  {i}: {opcode} {args}")
