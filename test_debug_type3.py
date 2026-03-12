# 调试类型问题 - 验证self.types
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.types import FunctionType, GenericType

code = """
template func apply<T, U>(value: T, transformer: func(T): U): U {
    let result = transformer(value);
    return result;
}
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 解析代码
parser = Parser(tokens)
ast = parser.parse()

# 创建分析器
analyzer = SemanticAnalyzer()

# 手动添加泛型类型参数到self.types
analyzer.types['T'] = GenericType('T')
analyzer.types['U'] = GenericType('U')

print("self.types after adding generic params:")
for name, type_obj in analyzer.types.items():
    print(f"  {name}: {type_obj}")

# 手动测试_resolve_type
for stmt in ast.statements:
    if hasattr(stmt, 'name') and stmt.name == 'apply':
        for param in stmt.params:
            if hasattr(param, 'name') and param.name == 'transformer':
                print(f"\nTesting _resolve_type for {param.name}")
                
                # 手动调用_resolve_type
                try:
                    resolved = analyzer._resolve_type(param.param_type)
                    print(f"Resolved type: {resolved}")
                    print(f"Resolved type class: {type(resolved)}")
                    print(f"Is FunctionType: {isinstance(resolved, FunctionType)}")
                    if isinstance(resolved, FunctionType):
                        print(f"FunctionType param_types: {resolved.param_types}")
                        print(f"FunctionType return_type: {resolved.return_type}")
                except Exception as e:
                    print(f"Error: {e}")
                    import traceback
                    traceback.print_exc()
