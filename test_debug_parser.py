# 详细调试泛型实例化检测（使用实际Parser）
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
        """
        检查当前位置是否是有效的泛型类型实例化
        """
        print(f"\n=== _is_valid_generic_instantiation called ===")
        print(f"Current position: {self.current}")
        print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
        
        saved_current = self.current
        
        try:
            print(f"Calling advance()...")
            self.advance()
            print(f"After advance(), current = {self.current}")
            print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
            
            while not self.is_at_end():
                print(f"\nChecking type parameter...")
                print(f"check(IDENTIFIER) = {self.check(TokenType.IDENTIFIER)}")
                
                if not self.check(TokenType.IDENTIFIER):
                    print("Not IDENTIFIER, returning False")
                    return False
                
                print(f"Consuming type name...")
                self.advance()
                print(f"After consuming, current = {self.current}")
                print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
                
                if self.check(TokenType.LESS_THAN):
                    print("Has nested generic, skipping...")
                    if not self._skip_nested_generic():
                        print("Failed to skip nested generic, returning False")
                        return False
                
                if self.check(TokenType.COMMA):
                    print("Found comma, continuing...")
                    self.advance()
                    continue
                
                if self.check(TokenType.GREATER_THAN):
                    print("Found GREATER_THAN, consuming...")
                    self.advance()
                    print(f"After consuming '>', current = {self.current}")
                    print(f"peek() = {self.peek().type}: '{self.peek().lexeme}'")
                    
                    if self.check(TokenType.LPAREN):
                        print("Next is LPAREN, returning True")
                        return True
                    elif self.check(TokenType.DOT):
                        print("Next is DOT, returning True")
                        return True
                    else:
                        print(f"Next is {self.peek().type}, returning False")
                        return False
                
                print("Unexpected token, returning False")
                return False
            
            return False
            
        finally:
            self.current = saved_current
            print(f"\nRestored current to {saved_current}")

print("\n=== Parsing with Debug ===")
try:
    parser = DebugParser(tokens)
    ast = parser.parse()
    print("\nParse successful!")
except Exception as e:
    print(f"\nParse error: {e}")
