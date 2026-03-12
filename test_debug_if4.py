# 调试if语句问题
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

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
        if hasattr(instr, 'args') and instr.args:
            arg_str = str(instr.args)
            # 检查是否是函数对象
            if 'function' in arg_str.lower() or 'nova' in arg_str.lower():
                print(f"{i}: {instr.name} <function object>")
            else:
                print(f"{i}: {instr.name} {instr.args}")
        else:
            print(f"{i}: {instr.name}")
    else:
        print(f"{i}: {instr}")

# 查找函数对象 - 在指令的args中
print("\n=== Looking for function objects in instructions ===")
for i, instr in enumerate(instructions):
    if hasattr(instr, 'name') and instr.name == 'LOAD_CONST':
        if hasattr(instr, 'args') and instr.args:
            const_val = instr.args[0]
            print(f"Instruction {i}: LOAD_CONST {type(const_val).__name__}")
            if hasattr(const_val, 'instructions'):
                print(f"  Function '{const_val.name}' instructions:")
                for j, func_instr in enumerate(const_val.instructions):
                    if hasattr(func_instr, 'name'):
                        if hasattr(func_instr, 'args') and func_instr.args:
                            print(f"    {j}: {func_instr.name} {func_instr.args}")
                        else:
                            print(f"    {j}: {func_instr.name}")
                    else:
                        print(f"    {j}: {func_instr}")
            elif hasattr(const_val, 'name'):
                print(f"  Name: {const_val.name}")
