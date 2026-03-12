# 调试类型问题 - 完整语义分析
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.errors import SemanticError

code = """
template func apply<T, U>(value: T, transformer: func(T): U): U {
    let result = transformer(value);
    return result;
}

func intToString(x: int): string {
    return "number";
}

func main() {
    let result1 = apply<int, string>(42, intToString);
}

main();
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 解析代码
parser = Parser(tokens)
ast = parser.parse()

# 语义分析
analyzer = SemanticAnalyzer()
try:
    analyzer.analyze(ast)
    print("Semantic analysis passed!")
except SemanticError as e:
    print(f"Semantic error: {e}")
    
    # 打印当前的self.types
    print("\nself.types at error time:")
    for name, type_obj in analyzer.types.items():
        print(f"  {name}: {type_obj}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
