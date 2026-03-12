"""
数学模块测试用例
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator

class TestMathModule(unittest.TestCase):
    """
    数学模块测试类
    """
    
    def test_trigonometric_functions(self):
        """
        测试三角函数
        """
        source = """
        use std::math;
        
        func main() {
            let angle = 3.14159265359 / 4;
            let sin_value = sin(angle);
            let cos_value = cos(angle);
            let tan_value = tan(angle);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_math_operations(self):
        """
        测试数学运算函数
        """
        source = """
        use std::math;
        
        func main() {
            let sqrt_value = sqrt(16);
            let pow_value = pow(2, 10);
            let abs_value = abs(-5);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_rounding_functions(self):
        """
        测试取整函数
        """
        source = """
        use std::math;
        
        func main() {
            let x = 3.7;
            let floor_value = floor(x);
            let ceil_value = ceil(x);
            let round_value = round(x);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_comparison_functions(self):
        """
        测试比较函数
        """
        source = """
        use std::math;
        
        func main() {
            let min_value = min(10, 20);
            let max_value = max(10, 20);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_constants(self):
        """
        测试数学常量
        """
        source = """
        use std::math;
        
        func main() {
            let pi_value = PI;
            let e_value = E;
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_circle_calculations(self):
        """
        测试圆的计算
        """
        source = """
        use std::math;
        
        func circle_area(radius: float) -> float {
            return PI * radius * radius;
        }
        
        func circle_circumference(radius: float) -> float {
            return 2 * PI * radius;
        }
        
        func main() {
            let radius = 5;
            let area = circle_area(radius);
            let circumference = circle_circumference(radius);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_distance_calculation(self):
        """
        测试距离计算
        """
        source = """
        use std::math;
        
        func distance(x1: float, y1: float, x2: float, y2: float) -> float {
            let dx = x2 - x1;
            let dy = y2 - y1;
            return sqrt(dx * dx + dy * dy);
        }
        
        func main() {
            let dist = distance(0, 0, 3, 4);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)
    
    def test_math_module_code_generation(self):
        """
        测试数学模块代码生成
        """
        source = """
        use std::math;
        
        func main() {
            let x = sqrt(16);
            let y = pow(2, 10);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(ast)
        
        self.assertIsInstance(instructions, list)
        self.assertIsInstance(constants, list)
    
    def test_complex_math_expression(self):
        """
        测试复杂数学表达式
        """
        source = """
        use std::math;
        
        func main() {
            let angle = PI / 6;
            let result = sin(angle) * sin(angle) + cos(angle) * cos(angle);
        }
        """
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        self.assertIsNotNone(analyzed_ast)

if __name__ == '__main__':
    unittest.main()
