# 调试泛型类字段类型解析
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer

code = """
template class Container<T> {
    var value: T;
    var isValid: bool;
    
    init(v: T) {
        this.value = v;
        this.isValid = true;
    }
    
    func check() {
        if this.isValid {
            print("Valid");
        }
    }
}

func main() {
    let c = Container<int>(42);
    c.check();
}

main();
"""

# 词法分析
scanner = Scanner(code)
tokens = scanner.scan_tokens()

print("=== Parsing ===")
parser = Parser(tokens)
ast = parser.parse()

print("\n=== AST Structure ===")
for stmt in ast.statements:
    print(f"Statement type: {type(stmt).__name__}")
    if hasattr(stmt, 'name'):
        print(f"  Name: {stmt.name}")
    if hasattr(stmt, 'fields'):
        print(f"  Fields:")
        for field in stmt.fields:
            print(f"    {field}")
            if len(field) >= 2:
                field_name, field_type = field[0], field[1]
                print(f"      Name: {field_name}, Type: {field_type} (type: {type(field_type).__name__})")
                if hasattr(field_type, 'name'):
                    print(f"      Type.name: {field_type.name}")

print("\n=== Semantic Analysis ===")
try:
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("Semantic analysis passed!")
except Exception as e:
    print(f"Semantic error: {e}")
    import traceback
    traceback.print_exc()
