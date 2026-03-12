# 调试泛型类字段类型解析（详细版）
import sys
sys.path.insert(0, 'src')

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.semantic.types import StructType

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

print("\n=== Semantic Analysis with Debug ===")

# 自定义分析器来添加调试信息
class DebugAnalyzer(SemanticAnalyzer):
    def visit_GenericClassDefinition(self, node):
        print(f"\n=== visit_GenericClassDefinition: {node.name} ===")
        result = super().visit_GenericClassDefinition(node)
        
        # 检查创建的类型
        class_type = self.types.get(node.name)
        if class_type:
            print(f"Class type: {class_type}")
            if hasattr(class_type, 'fields'):
                print(f"Fields:")
                for field in class_type.fields:
                    print(f"  {field}")
        
        # 检查符号
        symbol = self.current_scope.resolve_symbol(node.name)
        if symbol:
            print(f"Symbol: {symbol}")
            if hasattr(symbol, 'members'):
                print(f"Members:")
                for member in symbol.members:
                    print(f"  {member}")
        
        return result
    
    def visit_MemberExpression(self, node):
        print(f"\n=== visit_MemberExpression ===")
        print(f"Object: {node.object}")
        print(f"Member: {node.member}")
        
        obj_type = self._infer_type(node.object)
        print(f"Object type: {obj_type}")
        
        if hasattr(obj_type, 'fields'):
            print(f"Object type fields:")
            for field in obj_type.fields:
                print(f"  {field}")
        
        result = super().visit_MemberExpression(node)
        print(f"MemberExpression result: {result}")
        return result

try:
    analyzer = DebugAnalyzer()
    analyzer.analyze(ast)
    print("\nSemantic analysis passed!")
except Exception as e:
    print(f"\nSemantic error: {e}")
    import traceback
    traceback.print_exc()
