"""
Nova语言特性标志系统

类似于Python的__future__模块，用于管理语言特性的启用和禁用
使用类对象定义特性
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Feature:
    """
    语言特性
    
    Attributes:
        name: 特性名称
        description: 特性描述
        optional_version: 首次引入该特性的版本
        mandatory_version: 该特性成为默认的版本
        enabled: 是否启用
    """
    name: str
    description: str
    optional_version: Tuple[int, int, int]
    mandatory_version: Optional[Tuple[int, int, int]]
    enabled: bool = False
    
    def is_mandatory(self, current_version: Tuple[int, int, int]) -> bool:
        """
        检查该特性在当前版本是否为强制性的
        
        Args:
            current_version: 当前版本号
            
        Returns:
            bool: 是否为强制性
        """
        if self.mandatory_version is None:
            return False
        return current_version >= self.mandatory_version


class FeatureClass:
    """
    Feature类对象
    
    使用类对象定义和管理语言特性
    """
    
    def __init__(self):
        """
        初始化Feature类
        """
        self.features: Dict[str, Feature] = {}
        self.enabled_features: List[str] = []
        self._init_default_features()
    
    def _init_default_features(self):
        """
        初始化默认特性
        """
        # 泛型类型支持
        self.register_feature(
            Feature(
                name="GenericTypes",
                description="泛型类型支持",
                optional_version=(0, 2, 0),
                mandatory_version=(0, 3, 0),
                enabled=True
            )
        )
        
        # 特质系统支持
        self.register_feature(
            Feature(
                name="TraitSystem",
                description="特质系统支持",
                optional_version=(0, 2, 0),
                mandatory_version=(0, 3, 0),
                enabled=True
            )
        )
        
        # 模块导入导出支持
        self.register_feature(
            Feature(
                name="ModuleSystem",
                description="模块导入导出支持",
                optional_version=(0, 2, 0),
                mandatory_version=(0, 3, 0),
                enabled=True
            )
        )
        
        # 异步编程支持
        self.register_feature(
            Feature(
                name="AsyncProgramming",
                description="异步编程支持",
                optional_version=(0, 3, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 模式匹配支持
        self.register_feature(
            Feature(
                name="PatternMatching",
                description="模式匹配支持",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 类型注解
        self.register_feature(
            Feature(
                name="Annotations",
                description="类型注解",
                optional_version=(0, 4, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 字符串插值
        self.register_feature(
            Feature(
                name="StringInterpolation",
                description="字符串插值",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 解构赋值
        self.register_feature(
            Feature(
                name="Destructuring",
                description="解构赋值",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 可选链
        self.register_feature(
            Feature(
                name="OptionalChaining",
                description="可选链",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 空值合并
        self.register_feature(
            Feature(
                name="NullCoalescing",
                description="空值合并",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 高级参数系统
        self.register_feature(
            Feature(
                name="AdvancedParameters",
                description="高级参数系统（可变参数、默认值、关键字参数）",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 类对象系统
        self.register_feature(
            Feature(
                name="ClassObjects",
                description="类对象系统（NovaClass、NovaInstance）",
                optional_version=(0, 5, 0),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 延迟运算支持
        self.register_feature(
            Feature(
                name="DeferredOperations",
                description="延迟运算支持（优化乘法和除法的精度）",
                optional_version=(0, 9, 1),
                mandatory_version=(1, 2, 0),
                enabled=False
            )
        )
        
        # 访问修饰符支持 - private
        self.register_feature(
            Feature(
                name="AccessModifierPrivate",
                description="访问修饰符支持 - private（私有成员，仅类内部可访问）",
                optional_version=(0, 9, 3),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 访问修饰符支持 - protected
        self.register_feature(
            Feature(
                name="AccessModifierProtected",
                description="访问修饰符支持 - protected（受保护成员，类内部和子类可访问）",
                optional_version=(0, 9, 3),
                mandatory_version=None,
                enabled=True
            )
        )
        
        # 访问修饰符支持 - public
        self.register_feature(
            Feature(
                name="AccessModifierPublic",
                description="访问修饰符支持 - public（公有成员，任何地方可访问）",
                optional_version=(0, 9, 3),
                mandatory_version=None,
                enabled=True
            )
        )
    
    def register_feature(self, feature: Feature):
        """
        注册特性
        
        Args:
            feature: 特性对象
        """
        self.features[feature.name] = feature
    
    def enable(self, feature_name: str):
        """
        启用特性
        
        Args:
            feature_name: 特性名称
            
        Raises:
            ValueError: 特性不存在
        """
        if feature_name not in self.features:
            raise ValueError(f"Unknown feature: {feature_name}")
        
        feature = self.features[feature_name]
        feature.enabled = True
        
        if feature_name not in self.enabled_features:
            self.enabled_features.append(feature_name)
    
    def disable(self, feature_name: str):
        """
        禁用特性
        
        Args:
            feature_name: 特性名称
            
        Raises:
            ValueError: 特性不存在或不能禁用
        """
        if feature_name not in self.features:
            raise ValueError(f"Unknown feature: {feature_name}")
        
        feature = self.features[feature_name]
        
        # 检查是否可以禁用
        if feature_name in self.enabled_features:
            feature.enabled = False
            self.enabled_features.remove(feature_name)
    
    def is_enabled(self, feature_name: str) -> bool:
        """
        检查特性是否启用
        
        Args:
            feature_name: 特性名称
            
        Returns:
            bool: 是否启用
        """
        if feature_name not in self.features:
            return False
        
        return self.features[feature_name].enabled
    
    def get(self, feature_name: str) -> Optional[Feature]:
        """
        获取特性
        
        Args:
            feature_name: 特性名称
            
        Returns:
            Optional[Feature]: 特性对象，如果不存在则返回None
        """
        return self.features.get(feature_name)
    
    def list_all(self) -> List[Feature]:
        """
        获取所有特性
        
        Returns:
            List[Feature]: 特性列表
        """
        return list(self.features.values())
    
    def list_enabled(self) -> List[Feature]:
        """
        获取所有启用的特性
        
        Returns:
            List[Feature]: 启用的特性列表
        """
        return [self.features[name] for name in self.enabled_features]
    
    def list_available(self, current_version: Tuple[int, int, int]) -> List[Feature]:
        """
        获取当前版本可用的特性
        
        Args:
            current_version: 当前版本号
            
        Returns:
            List[Feature]: 可用的特性列表
        """
        return [
            feature for feature in self.features.values()
            if current_version >= feature.optional_version
        ]
    
    def list_mandatory(self, current_version: Tuple[int, int, int]) -> List[Feature]:
        """
        获取当前版本强制性的特性
        
        Args:
            current_version: 当前版本号
            
        Returns:
            List[Feature]: 强制性的特性列表
        """
        return [
            feature for feature in self.features.values()
            if feature.is_mandatory(current_version)
        ]
    
    def reset(self):
        """
        重置所有特性状态
        """
        for feature in self.features.values():
            feature.enabled = False
        self.enabled_features.clear()
    
    # 别名方法，用于兼容测试
    def enable_feature(self, feature_name: str):
        """启用特性（别名）"""
        return self.enable(feature_name)
    
    def disable_feature(self, feature_name: str):
        """禁用特性（别名）"""
        return self.disable(feature_name)
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """检查特性是否启用（别名）"""
        return self.is_enabled(feature_name)
    
    def get_feature(self, feature_name: str) -> Optional[Feature]:
        """获取特性（别名）"""
        return self.get(feature_name)
    
    def get_all_features(self) -> List[Feature]:
        """获取所有特性（别名）"""
        return self.list_all()
    
    def get_enabled_features(self) -> List[Feature]:
        """获取启用的特性（别名）"""
        return self.list_enabled()
    
    def get_available_features(self, current_version: Tuple[int, int, int]) -> List[Feature]:
        """获取可用的特性（别名）"""
        return self.list_available(current_version)
    
    def get_mandatory_features(self, current_version: Tuple[int, int, int]) -> List[Feature]:
        """获取强制性的特性（别名）"""
        return self.list_mandatory(current_version)
    
    def import_from_future(self, feature_names: List[str]):
        """从__future__导入特性（别名）"""
        for name in feature_names:
            self.enable(name)
    
    def __repr__(self):
        """
        Feature类的字符串表示
        """
        return f"<FeatureClass features={len(self.features)} enabled={len(self.enabled_features)}>"


# 全局Feature类实例
_global_feature_class: Optional[FeatureClass] = None


def get_feature_class() -> FeatureClass:
    """
    获取全局Feature类
    
    Returns:
        FeatureClass: 全局Feature类
    """
    global _global_feature_class
    if _global_feature_class is None:
        _global_feature_class = FeatureClass()
    return _global_feature_class


def reset_feature_class():
    """
    重置全局Feature类
    """
    global _global_feature_class
    _global_feature_class = None


# 保持向后兼容的FeatureManager别名
FeatureManager = FeatureClass
get_feature_manager = get_feature_class
reset_feature_manager = reset_feature_class
