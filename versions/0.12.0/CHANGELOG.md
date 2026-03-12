# Nova 语言更新日志

## [0.12.0] - 2026-03-01
### 新增
- **模板结构体功能**（Generic Structs）：
  - 支持 `template struct StructName<T>` 语法定义泛型结构体
  - 支持类型参数在结构体字段中使用
  - 支持泛型结构体方法定义
  - 支持泛型结构体实例化：`StructName<int>(...)`
  - 支持多种类型实例化（int、float、string等）
  - 创建 `GenericStructDefinition` AST节点
  - 实现解析器对 `template struct` 语法的支持
  - 实现语义分析器对泛型结构体的类型检查
  - 实现代码生成器对泛型结构体的代码生成

- **模板函数功能**（Generic Functions）：
  - 支持 `template func funcName<T>(param: T): T` 语法定义泛型函数
  - 支持类型参数在函数参数和返回值中使用
  - 支持泛型函数调用：`funcName<int>(...)`
  - 支持多种类型实例化（int、float、string等）
  - 创建 `GenericFunctionDefinition` AST节点
  - 实现解析器对 `template func` 语法的支持
  - 实现语义分析器对泛型函数的类型检查
  - 实现代码生成器对泛型函数的代码生成
  - 修复比较操作（`<`, `>`, `<=`, `>=`）返回类型问题，现在正确返回 `bool` 类型

- **类型推断功能**（Type Inference）：
  - 支持泛型结构体的自动类型推断：`Point(10, 20)` 自动推断为 `Point<int>`
  - 支持泛型函数的自动类型推断：`identity(42)` 自动推断为 `identity<int>`
  - 支持多种类型的自动推断（int、float、string等）
  - 推断失败时提供清晰的错误提示，建议使用显式类型指定
  - 保持向后兼容，显式类型指定仍然支持
  - 在 `parser.py` 中支持不带类型参数的泛型调用
  - 在 `analyzer.py` 中添加类型推断逻辑
  - 添加 `_infer_generic_type_from_args` 方法实现类型推断算法

### 测试
- 添加 `test_generic_struct.nova` 测试文件
  - 测试泛型结构体 `Point<T>` 的创建和实例化
  - 测试多种类型参数（int、float、string）
  - 测试泛型结构体方法的调用

- 添加 `test_generic_function.nova` 测试文件
  - 测试泛型函数 `identity<T>` 的调用
  - 测试多种类型参数（int、float、string）
  - 测试泛型函数返回值

- 添加 `test_type_inference.nova` 测试文件
  - 测试泛型结构体的自动类型推断（int、float、string）
  - 测试泛型函数的自动类型推断（int、float、string）
  - 测试显式类型指定（向后兼容性）

---

**查看所有版本历史，请参阅 [CHANGELOG_ALL.md](CHANGELOG_ALL.md)**
