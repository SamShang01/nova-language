# 详细调试泛型实例化检测（使用实际Parser + 更多调试）
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
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

# 创建一个修改过的Parser类来添加调试输出
class DebugParser(Parser):
    def _is_valid_generic_instantiation(self):
        print(f"\n=== _is_valid_generic_instantiation called ===")
        print(f"Current position: {self.current}")
        print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
        result = super()._is_valid_generic_instantiation()
        print(f"_is_valid_generic_instantiation returned: {result}")
        print(f"Current position after: {self.current}")
        return result
    
    def consume(self, type, message):
        print(f"\n=== consume called ===")
        print(f"Expecting: {type}")
        print(f"Current position: {self.current}")
        print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
        result = super().consume(type, message)
        print(f"Consumed: {result.type}: '{result.lexeme}'")
        print(f"Current position after: {self.current}")
        return result
    
    def parse_type(self):
        print(f"\n=== parse_type called ===")
        print(f"Current position: {self.current}")
        print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
        result = super().parse_type()
        print(f"parse_type returned: {result}")
        print(f"Current position after: {self.current}")
        return result
    
    def parse_call(self, callee, consume_lparen=True):
        print(f"\n=== parse_call called ===")
        print(f"callee: {callee}")
        print(f"Current position: {self.current}")
        print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
        result = super().parse_call(callee, consume_lparen)
        print(f"parse_call returned: {result}")
        return result
    
    def parse_expression(self):
        print(f"\n=== parse_expression called ===")
        print(f"Current position: {self.current}")
        print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
        result = super().parse_expression()
        print(f"parse_expression returned: {result}")
        print(f"Current position after: {self.current}")
        return result

print("\n=== Parsing with Debug ===")
try:
    parser = DebugParser(tokens)
    ast = parser.parse()
    print("\nParse successful!")
except Exception as e:
    print(f"\nParse error: {e}")
    import traceback
    traceback.print_exc()
