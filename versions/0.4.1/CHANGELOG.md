# Nova语言版本0.4.1变更日志

## 版本信息
- 版本号: 0.4.1
- 发布日期: 2026-02-26
- 版本类型: 小版本更新（bugfix）

## 主要变更

### 新增功能
- **NovaFunction类**: 创建了Nova专用的函数代理对象，替代Python函数
  - 封装函数名、指令和参数
  - 支持位置参数和关键字参数
  - 提供清晰的函数表示

- **参数系统增强**:
  - 支持位置参数
  - 支持关键字参数
  - 支持默认值参数
  - 支持可变参数（*args）
  - 支持关键字可变参数（**kwargs）

- **ParameterDefinition AST节点**: 新增参数定义节点，支持复杂的参数类型

### 改进
- **REPL多行模式**: 改进代码完整性检测，支持自动退出多行模式
  - 检查括号平衡（圆括号、方括号、花括号）
  - 检查冒号和逗号结尾
  - 更智能的代码完整性判断

- **函数参数绑定**: 修复函数调用时参数未定义的问题
  - 正确处理位置参数
  - 正确处理关键字参数
  - 参数不足时使用默认值None

### 修复
- 修复REPL函数定义后无法调用的问题
- 修复:type命令找不到变量的问题
- 修复控制字符导致词法错误的问题
- 修复VMError参数错误的问题
- 修复函数调用时参数未定义的错误
- 修复Unknown operator错误
- 修复泛型类型解析错误

## 技术细节

### NovaFunction类
```python
class NovaFunction:
    def __init__(self, name, instructions, params):
        self.name = name
        self.instructions = instructions
        self.params = params
        self._parse_params()
    
    def __call__(self, *args, **kwargs):
        # 处理位置参数
        # 处理可变参数
        # 处理关键字参数
        # 执行函数体
```

### ParameterDefinition类
```python
class ParameterDefinition(Node):
    def __init__(self, line, column, name, param_type, 
                 default_value=None, is_varargs=False, is_kwargs=False):
        self.name = name
        self.param_type = param_type
        self.default_value = default_value
        self.is_varargs = is_varargs
        self.is_kwargs = is_kwargs
```

## 兼容性
- 向后兼容0.4.0版本
- 保持API稳定性
- 不破坏现有代码

## 已知问题
- 无

## 升级指南
从0.4.0升级到0.4.1无需任何代码更改，所有现有代码将继续正常工作。

## 下一步计划
- 实现类对象系统
- 完善feature系统（使用类对象定义）
- 实现完整的编译器版本存档系统
