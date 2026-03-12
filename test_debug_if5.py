# 调试if语句问题
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
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

# 打印指令
print("=== Generated Instructions ===")
for i, instr in enumerate(instructions):
    if hasattr(instr, 'name'):
        print(f"{i}: {instr.name}")

# 查找函数对象 - 直接访问指令的args
print("\n=== Looking for function objects ===")
for i, instr in enumerate(instructions):
    if isinstance(instr, LOAD_CONST):
        if instr.args:
            func_obj = instr.args[0]
            print(f"\nInstruction {i}: LOAD_CONST")
            print(f"  Type: {type(func_obj).__name__}")
            if hasattr(func_obj, 'name'):
                print(f"  Name: {func_obj.name}")
            if hasattr(func_obj, 'instructions'):
                print(f"  Instructions:")
                for j, func_instr in enumerate(func_obj.instructions):
                    if hasattr(func_instr, 'name'):
                        if hasattr(func_instr, 'args') and func_instr.args:
                            print(f"    {j}: {func_instr.name} {func_instr.args}")
                        else:
                            print(f"    {j}: {func_instr.name}")
                    else:
                        print(f"    {j}: {func_instr}")
