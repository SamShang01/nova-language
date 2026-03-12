"""
测试装饰器语法（复杂版本）
"""

from nova.compiler.lexer import Scanner
from nova.compiler.parser import Parser

# 测试代码（复杂版本）
code = """
@staticmethod
@final
func static_method() -> int {
    return 42;
}

@classmethod
@overload
func class_method(cls: type) -> str {
    return "class method";
}

@overload
func overloaded_func(x: int) -> int {
    return x;
}

@overload
func overloaded_func(x: str) -> str {
    return x;
}

func overloaded_func(x: any) -> any {
    if isinstance(x, int) {
        return x;
    } elif isinstance(x, str) {
        return x;
    } else {
        return None;
    }
}
"""

# 扫描代码生成Token
scanner = Scanner(code)
tokens = scanner.scan_tokens()

# 打印Token
print("Tokens:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type.name}: {token.lexeme}")

# 解析Token生成AST
try:
    parser = Parser(tokens)
    ast = parser.parse()
    print("\n解析成功！")
    print(f"生成的AST: {ast}")
    
    # 打印函数定义及其装饰器
    for statement in ast.statements:
        if hasattr(statement, 'decorators') and statement.decorators:
            print(f"\n函数: {statement.name}")
            print(f"装饰器数量: {len(statement.decorators)}")
            for i, decorator in enumerate(statement.decorators):
                print(f"装饰器 {i+1}: {decorator.decorator}")
except Exception as e:
    print(f"\n解析错误: {e}")