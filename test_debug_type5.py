# 调试类型问题 - 调试visit_CallExpression
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.errors import SemanticError
from nova.compiler.semantic.types import FunctionType
from nova.compiler.parser.ast import IdentifierExpression

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

# 创建调试分析器
class DebugAnalyzer(SemanticAnalyzer):
    def visit_CallExpression(self, node):
        print(f"\n=== visit_CallExpression ===")
        if hasattr(node.callee, 'name'):
            print(f"Callee name: {node.callee.name}")
            
            symbol = self.current_scope.resolve_symbol(node.callee.name)
            if symbol:
                print(f"Symbol found: {symbol}")
                print(f"Symbol type: {type(symbol)}")
                if hasattr(symbol, 'type'):
                    print(f"Symbol.type: {symbol.type}")
                    print(f"Symbol.type type: {type(symbol.type)}")
                    print(f"Is FunctionType: {isinstance(symbol.type, FunctionType)}")
        
        result = super().visit_CallExpression(node)
        print(f"Return type: {result}")
        print(f"Return type class: {type(result)}")
        return result

analyzer = DebugAnalyzer()
try:
    analyzer.analyze(ast)
    print("Semantic analysis passed!")
except SemanticError as e:
    print(f"\nSemantic error: {e}")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
