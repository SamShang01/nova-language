# 详细调试泛型实例化检测（修正版）
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.lexer.tokens import TokenType

code = """
let n = Node<int>(42, true);
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("=== All Tokens ===")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type}: '{token.lexeme}'")

print("\n=== Simulating _is_valid_generic_instantiation ===")

# 手动模拟 _is_valid_generic_instantiation
# 当调用 _is_valid_generic_instantiation 时，current 在 Node（token 3）
# peek() 返回 <（token 4）
# advance() 会跳过 <，current 变成 4，peek() 返回 int（token 5）

current = 3  # Node 的位置

print(f"Starting at token {current}: {tokens[current].type}: '{tokens[current].lexeme}'")
print(f"peek() would return token {current + 1}: {tokens[current + 1].type}: '{tokens[current + 1].lexeme}'")

# 模拟 advance() 跳过 <
current += 1  # 现在 current 在 <
print(f"After advance(), current = {current}: {tokens[current].type}: '{tokens[current].lexeme}'")
print(f"peek() would return token {current + 1}: {tokens[current + 1].type}: '{tokens[current + 1].lexeme}'")

# 检查是否是 IDENTIFIER
if tokens[current + 1].type != TokenType.IDENTIFIER:
    print(f"ERROR: Expected IDENTIFIER, got {tokens[current + 1].type}")
else:
    print(f"OK: Token is IDENTIFIER")
    
    # 消费类型名
    current += 1  # 现在 current 在 int
    print(f"After consuming type name, current = {current}: {tokens[current].type}: '{tokens[current].lexeme}'")
    print(f"peek() would return token {current + 1}: {tokens[current + 1].type}: '{tokens[current + 1].lexeme}'")
    
    # 检查是否有嵌套的泛型类型
    if tokens[current + 1].type == TokenType.LESS_THAN:
        print("Has nested generic type")
    else:
        print("No nested generic type")
        
        # 检查是否有更多类型参数（逗号分隔）
        if tokens[current + 1].type == TokenType.COMMA:
            print("Has more type parameters")
        else:
            print("No more type parameters")
            
            # 检查是否以 > 结束
            if tokens[current + 1].type == TokenType.GREATER_THAN:
                print("OK: Token is GREATER_THAN")
                
                # 消费 >
                current += 1  # 现在 current 在 >
                print(f"After consuming '>', current = {current}: {tokens[current].type}: '{tokens[current].lexeme}'")
                print(f"peek() would return token {current + 1}: {tokens[current + 1].type}: '{tokens[current + 1].lexeme}'")
                
                # 检查后面是否是 ( 或 .
                if tokens[current + 1].type == TokenType.LPAREN:
                    print("OK: Next token is LPAREN - This is a valid generic instantiation!")
                elif tokens[current + 1].type == TokenType.DOT:
                    print("OK: Next token is DOT - This is a valid generic instantiation!")
                else:
                    print(f"ERROR: Expected LPAREN or DOT, got {tokens[current + 1].type}")
            else:
                print(f"ERROR: Expected GREATER_THAN, got {tokens[current + 1].type}")
