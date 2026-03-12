# 调试类型问题
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.errors import SemanticError
from nova.compiler.semantic.types import FunctionType
from nova.compiler.parser.ast import FunctionTypeExpression

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

# 打印AST中的函数定义
for stmt in ast.statements:
    if hasattr(stmt, 'name') and stmt.name == 'apply':
        print(f"Found function: {stmt.name}")
        print(f"Type params: {stmt.type_params}")
        print(f"Params: {stmt.params}")
        for param in stmt.params:
            if hasattr(param, 'name'):
                print(f"  Param: {param.name}")
                print(f"  Param type: {param.param_type}")
                print(f"  Param type class: {type(param.param_type)}")
                if hasattr(param.param_type, 'param_types'):
                    print(f"  Function param_types: {param.param_type.param_types}")
                if hasattr(param.param_type, 'return_type'):
                    print(f"  Function return_type: {param.param_type.return_type}")
