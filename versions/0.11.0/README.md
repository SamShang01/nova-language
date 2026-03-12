# Nova 语言 0.11.0 版本说明

## 版本信息
- **版本号**: 0.11.0
- **发布日期**: 2026-03-01
- **版本类型**: 功能更新版本

## 主要更新内容

### 1. 模板结构体功能（Generic Structs）

#### 功能概述
Nova 语言现在支持模板结构体，允许开发者定义带类型参数的结构体，实现类型安全的泛型编程。

#### 语法示例
```nova
template struct Point<T> {
    var x: T;
    var y: T;
}

// 使用
let p = Point<int>(10, 20);
```

#### 支持的特性
- ✅ 类型参数在结构体字段中使用
- ✅ 泛型结构体方法定义
- ✅ 多种类型实例化（int、float、string等）
- ✅ 值类型语义（栈分配）

### 2. 模板函数功能（Generic Functions）

#### 功能概述
Nova 语言现在支持模板函数，允许开发者定义带类型参数的函数，实现代码复用和类型安全。

#### 语法示例
```nova
template func identity<T>(value: T): T {
    return value;
}

// 使用
let id = identity<int>(42);
```

#### 支持的特性
- ✅ 类型参数在函数参数和返回值中使用
- ✅ 多种类型实例化（int、float、string等）
- ✅ 显式类型指定（类型推断将在后续版本添加）

## 技术实现

### AST节点
- `GenericStructDefinition`: 泛型结构体定义节点
- `GenericFunctionDefinition`: 泛型函数定义节点

### 编译器组件
- **词法分析器**: 支持 `template` 关键字
- **语法分析器**: 解析 `template struct` 和 `template func` 语法
- **语义分析器**: 类型参数检查和验证
- **代码生成器**: 生成泛型代码的实例化版本

## 测试用例

### 模板结构体测试
- 测试文件: `test_generic_struct.nova`
- 测试内容: Point<T> 结构体的创建和实例化

### 模板函数测试
- 测试文件: `test_generic_function.nova`
- 测试内容: identity<T> 函数的调用和返回值

## 已知限制

1. **类型推断**: 当前版本需要显式指定类型参数，类型推断功能将在后续版本添加
2. **Trait约束**: 当前版本不支持 trait 约束（如 `T: Numeric`），将在后续版本添加
3. **模板特化**: 不支持模板特化功能

## 后续计划

### 0.12.0 版本（计划中）
- 类型推断功能
- Trait约束模板
- 更完善的错误信息

## 相关文件

- `src/nova/compiler/parser/ast.py` - AST节点定义
- `src/nova/compiler/parser/parser.py` - 语法分析器
- `src/nova/compiler/semantic/analyzer.py` - 语义分析器
- `src/nova/compiler/codegen/generator.py` - 代码生成器
- `CHANGELOG.md` - 详细更新日志

## 贡献者

- 泛型程序员: 模板结构体和模板函数的实现
- AI助手: 架构设计和STL库支持

---

**注意**: 这是 Nova 语言的重要版本更新，标志着泛型编程功能的完整实现。
