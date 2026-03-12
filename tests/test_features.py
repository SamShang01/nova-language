"""
Nova语言__future__特性测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.features import get_feature_manager, Feature, FeatureManager, reset_feature_manager


class TestFeatureSystem(unittest.TestCase):
    """
    特性系统测试类
    """
    
    def setUp(self):
        """
        测试前准备
        """
        reset_feature_manager()
        self.feature_manager = get_feature_manager()
    
    def test_feature_manager_initialization(self):
        """
        测试特性管理器初始化
        """
        self.assertIsNotNone(self.feature_manager)
        self.assertIsInstance(self.feature_manager, FeatureManager)
    
    def test_register_feature(self):
        """
        测试注册特性
        """
        feature = Feature(
            name="TestFeature",
            description="测试特性",
            optional_version=(0, 1, 0),
            mandatory_version=None
        )
        self.feature_manager.register_feature(feature)
        
        registered = self.feature_manager.get_feature("TestFeature")
        self.assertIsNotNone(registered)
        self.assertEqual(registered.name, "TestFeature")
    
    def test_enable_feature(self):
        """
        测试启用特性
        """
        self.feature_manager.enable_feature("GenericTypes")
        self.assertTrue(self.feature_manager.is_feature_enabled("GenericTypes"))
    
    def test_disable_feature(self):
        """
        测试禁用特性
        """
        self.feature_manager.enable_feature("GenericTypes")
        self.assertTrue(self.feature_manager.is_feature_enabled("GenericTypes"))
        
        self.feature_manager.disable_feature("GenericTypes")
        self.assertFalse(self.feature_manager.is_feature_enabled("GenericTypes"))
    
    def test_enable_unknown_feature(self):
        """
        测试启用不存在的特性
        """
        with self.assertRaises(ValueError):
            self.feature_manager.enable_feature("UnknownFeature")
    
    def test_get_all_features(self):
        """
        测试获取所有特性
        """
        features = self.feature_manager.get_all_features()
        self.assertGreater(len(features), 0)
    
    def test_get_enabled_features(self):
        """
        测试获取启用的特性
        """
        self.feature_manager.enable_feature("GenericTypes")
        self.feature_manager.enable_feature("TraitSystem")
        
        enabled = self.feature_manager.get_enabled_features()
        self.assertEqual(len(enabled), 2)
    
    def test_get_available_features(self):
        """
        测试获取可用的特性
        """
        available = self.feature_manager.get_available_features((0, 3, 0))
        self.assertGreater(len(available), 0)
        
        # 检查是否包含0.2.0引入的特性
        feature_names = [f.name for f in available]
        self.assertIn("GenericTypes", feature_names)
        self.assertIn("TraitSystem", feature_names)
        self.assertIn("ModuleSystem", feature_names)
    
    def test_get_mandatory_features(self):
        """
        测试获取强制性的特性
        """
        mandatory = self.feature_manager.get_mandatory_features((0, 3, 0))
        
        # 0.3.0版本应该有强制性特性
        self.assertGreater(len(mandatory), 0)
        
        # 检查是否包含0.3.0成为默认的特性
        feature_names = [f.name for f in mandatory]
        self.assertIn("GenericTypes", feature_names)
        self.assertIn("TraitSystem", feature_names)
        self.assertIn("ModuleSystem", feature_names)
    
    def test_import_from_future(self):
        """
        测试从__future__导入特性
        """
        self.feature_manager.import_from_future(["GenericTypes", "TraitSystem"])
        
        self.assertTrue(self.feature_manager.is_feature_enabled("GenericTypes"))
        self.assertTrue(self.feature_manager.is_feature_enabled("TraitSystem"))
    
    def test_feature_is_mandatory(self):
        """
        测试特性是否为强制性
        """
        feature = self.feature_manager.get_feature("GenericTypes")
        self.assertIsNotNone(feature)
        
        # 在0.3.0版本应该是强制性的
        self.assertTrue(feature.is_mandatory((0, 3, 0)))
        
        # 在0.2.0版本不应该强制性
        self.assertFalse(feature.is_mandatory((0, 2, 0)))
    
    def test_reset(self):
        """
        测试重置特性管理器
        """
        self.feature_manager.enable_feature("GenericTypes")
        self.feature_manager.enable_feature("TraitSystem")
        
        self.feature_manager.reset()
        
        self.assertFalse(self.feature_manager.is_feature_enabled("GenericTypes"))
        self.assertFalse(self.feature_manager.is_feature_enabled("TraitSystem"))


class TestFutureImport(unittest.TestCase):
    """
    __future__导入测试类
    """
    
    def setUp(self):
        """
        测试前准备
        """
        reset_feature_manager()
    
    def test_parse_future_import(self):
        """
        测试解析from __future__ import语句
        """
        code = """
        from __future__ import GenericTypes;
        
        func main() {
            return 0;
        }
        """
        
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 2)
    
    def test_parse_multiple_future_imports(self):
        """
        测试解析多个from __future__ import语句
        """
        code = """
        from __future__ import GenericTypes;
        from __future__ import TraitSystem;
        from __future__ import ModuleSystem;
        
        func main() {
            return 0;
        }
        """
        
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 4)
    
    def test_semantic_analyze_future_import(self):
        """
        测试语义分析from __future__ import语句
        """
        code = """
        from __future__ import GenericTypes;
        
        func main() {
            return 0;
        }
        """
        
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)
        
        # 检查特性是否被启用
        self.assertTrue(analyzer.feature_manager.is_feature_enabled("GenericTypes"))
    
    def test_semantic_analyze_unknown_feature(self):
        """
        测试语义分析未知的特性
        """
        code = """
        from __future__ import UnknownFeature;
        
        func main() {
            return 0;
        }
        """
        
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        
        # 应该抛出语义错误
        with self.assertRaises(Exception):
            analyzer.analyze(program)
    
    def test_future_import_with_standard_import(self):
        """
        测试__future__导入与标准导入混合使用
        """
        code = """
        from __future__ import GenericTypes;
        use std::io::print;
        
        func main() {
            print("Hello");
            return 0;
        }
        """
        
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        program = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)
        
        # 检查特性是否被启用
        self.assertTrue(analyzer.feature_manager.is_feature_enabled("GenericTypes"))


if __name__ == '__main__':
    unittest.main()
