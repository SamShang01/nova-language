# Nova 语言版本规划

## 版本规划概览

本文档规划了Nova语言从0.10.0到0.15.0的发展路线图。

## 版本生命周期说明

每个版本都会经历以下阶段：

1. **计划中** - 版本功能规划阶段，确定要实现的功能
2. **开发中** - 功能开发阶段，实现新功能和修复bug
3. **功能锁定** - 不再添加新功能，只修复bug和优化
4. **测试中** - 全面测试阶段，确保稳定性
5. **已发布** - 正式发布版本
6. **生命周期结束** - 不再维护的版本

---

## [0.12.0] - 2026-03-01 ✅ 已发布
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

---

## [0.11.1] - 2026-03-01 ✅ 已发布
### 修复
- **比较操作符解析修复**：
  - 修复模板函数体中比较操作符（`<`, `>`, `<=`, `>=`）的解析问题
  - 修复 `parse_primary` 方法中泛型类型实例化和比较操作符的冲突
  - 添加 `_is_valid_generic_instantiation` 方法判断是否为有效的泛型类型实例化
  - 添加 `_skip_nested_generic` 方法跳过嵌套的泛型类型
  - 现在可以正确解析 `if a < b` 等比较表达式

- **Template Class多类型参数支持**：
  - 修复 `parse_generic_class_definition` 方法支持多个类型参数
  - 支持逗号分隔的类型参数列表：`template class Pair<T, U>`
  - 支持三个或更多类型参数：`template class Triple<T, U, V>`
  - 正确处理类型参数的解析和结束符 `>`

- **函数类型参数解析修复**：
  - 修复函数类型作为参数的解析问题：`fn: func(T): U`
  - 修复 `parse_primary` 方法中函数调用的解析逻辑
  - 将 `identifier(...)` 正确解析为 `IdentifierExpression` 而不是 `GenericTypeExpression`
  - 在 `analyzer.py` 中添加函数类型变量的处理逻辑
  - 支持高阶函数（如 `apply`, `map`, `filter`）的正常调用

- **模板函数运行时错误修复**：
  - 修复模板函数的代码生成问题
  - 确保类型参数正确替换
  - 修复运行时错误，使模板函数可以正常执行

---

## [0.11.0] - 2026-03-01 ✅ 已发布
### 新增
- **模板结构体**：
  - 支持模板结构体定义：`template struct StructName<T> { ... }`
  - 支持模板结构体实例化
  - 支持类型参数在结构体字段中使用
  - 支持值类型语义（栈上分配，值拷贝）

- **模板函数**：
  - 支持模板函数定义：`template func funcName<T>(param: T): T { ... }`
  - 支持模板函数调用
  - 支持类型参数在函数参数和返回值中使用
  - 支持急切实例化策略

- **类型推断**：
  - 支持泛型结构体的自动类型推断
  - 支持泛型函数的自动类型推断
  - 推断失败时提供清晰的错误提示

- **STL库优化**：
  - 将 `ListNode<T>` 改为模板结构体实现
  - 优化内存布局，使用值类型特性
  - 提升性能，减少堆分配
  - 添加 `Option<T>` 类型用于处理可选值

---

## [0.10.1] - 2026-03-01 ✅ 已发布
### 新增
- **STL库（标准模板库）**：
  - **迭代器系统**：Iterator, RandomAccessIterator, BidirectionalIterator等
  - **函数对象和比较器**：Less, Greater, EqualTo, Plus, Minus等
  - **序列容器**：Vector, List, Stack, Queue, PriorityQueue
  - **关联容器**：Set, Map, Pair
  - **算法库**：sort, reverse, find, binarySearch, count等

---

## [0.10.0] - 2026-03-01 ✅ 已发布
### 新增
- **模板功能**：
  - 添加 `template` 关键字支持泛型编程
  - 支持模板类定义：`template class ClassName<T> { ... }`
  - 支持多个类型参数：`template class ClassName<T, U, V> { ... }`
  - 支持模板类实例化：`ClassName<int>(42)`
  - 支持类型参数在字段和方法中使用

---

## [0.13.0] - 2026-03-03 ✅ 已发布
### 新增
- **Trait约束参数语法**：
  - 支持 `func printValue(value: Printable)` 简化语法
  - 参数类型为trait时，表示该参数必须实现指定的trait
  - 更简洁的语法，无需显式 `trait` 关键字
  - 与现代语言（Rust、Swift、Kotlin）保持一致

### 改进
- **Trait系统基础**：
  - Trait定义语法：`trait Printable { func toString() -> string; }`
  - Trait方法签名定义
  - Trait类型在语义分析器中的注册

### 已知限制
- Trait约束检查功能正在开发中
- Impl块检查功能正在开发中
- 当前版本支持trait定义和基本使用，完整约束检查将在后续版本实现

---

## [0.14.0] - 计划中
### 新增
- **泛型集合库**：
  - 实现 `List<T>` 泛型列表
  - 实现 `Map<K, V>` 泛型映射
  - 实现 `Set<T>` 泛型集合
  - 实现 `Array<T>` 泛型数组

- **泛型算法**：
  - 实现 `sort<T: Comparable>(list: List<T>)` 排序函数
  - 实现 `filter<T>(list: List<T>, predicate: func(T): bool)` 过滤函数
  - 实现 `map<T, U>(list: List<T>, transform: func(T): U)` 映射函数
  - 实现 `reduce<T>(list: List<T>, initial: T, reducer: func(T, T): T)` 归约函数

- **Trait约束检查**：
  - 实现完整的trait约束检查功能
  - 检查类型是否实现了指定的trait
  - 提供清晰的错误提示

### 示例
```nova
let numbers = List<int>();
numbers.push(1);
numbers.push(2);
numbers.push(3);

let sorted = sort<int>(numbers);
let filtered = filter<int>(numbers, func(x: int): bool {
    return x > 1;
});
```

---

## [0.15.0] - 计划中
### 优化
- **编译时类型检查**：
  - 增强泛型类型的编译时类型检查
  - 提供更详细的类型错误信息
  - 支持类型推断

- **性能优化**：
  - 优化模板实例化性能
  - 减少模板代码生成开销
  - 实现模板代码缓存

### 新增
- **泛型接口**：
  - 支持泛型trait定义：`trait Iterator<T> { ... }`
  - 支持泛型impl块：`impl<T> Iterator<T> for List<T> { ... }`

### 示例
```nova
trait Iterator<T> {
    func next(): T;
    func hasNext(): bool;
}

impl<T> Iterator<T> for List<T> {
    func next(): T {
        return this.current;
    }
    
    func hasNext(): bool {
        return this.index < this.length;
    }
}
```

---

## [0.16.0] - 计划中
### 新增
- **高级泛型特性**：
  - 支持变长类型参数：`template class Tuple<T...> { ... }`
  - 支持类型参数递归：`template class Node<T: Node<T>> { ... }`
  - 支持类型别名：`type IntList = List<int>`

- **元编程**：
  - 支持编译时类型计算
  - 支持类型级别的函数
  - 支持类型级别的条件判断

### 示例
```nova
template class Tuple<T...> {
    var values: T...;
    
    func get(index: int): any {
        return this.values[index];
    }
}

type IntList = List<int>;
type StringMap = Map<string, int>;

let list = IntList();
list.push(1);
list.push(2);
```

### 生态系统扩展
- **包管理器增强**：
  - 支持泛型包的发布和安装
  - 支持泛型库的版本管理
  - 支持泛型代码的文档生成

- **开发工具**：
  - 增强IDE对泛型的支持
  - 提供泛型代码的智能提示
  - 提供泛型代码的重构工具

---

## 版本发布时间表

| 版本 | 计划发布日期 | 主要功能 |
|------|--------------|----------|
| 0.10.0 | 2026-03-01 | ✅ 模板类 |
| 0.11.0 | 2026-03-01 | ✅ 模板结构体、函数和trait限制 |
| 0.12.0 | 2026-03-01 | ✅ 类型约束增强和默认类型参数 |
| 0.13.0 | 2026-03-03 | ✅ Trait约束参数语法 |
| 0.14.0 | 2026-04-15 | 泛型集合库和算法 |
| 0.15.0 | 2026-05-01 | 性能优化和泛型接口 |
| 0.16.0 | 2026-05-15 | 高级泛型特性和元编程 |

---

## 优先级说明

### 高优先级（必须实现）
- 0.11.0: ✅ 模板结构体、函数和trait限制
- 0.12.0: ✅ 类型约束增强
- 0.13.0: ✅ Trait约束参数语法
- 0.14.0: 泛型集合库

### 中优先级（重要但可延后）
- 0.12.0: ✅ 默认类型参数
- 0.15.0: 性能优化
- 0.15.0: 泛型接口

### 低优先级（可选功能）
- 0.16.0: 变长类型参数
- 0.16.0: 元编程
- 0.16.0: 生态系统扩展

---

## 技术债务

在实现上述功能时，需要解决以下技术债务：

1. **类型系统增强**
   - 完善类型推断算法
   - 增强类型错误诊断
   - 支持更复杂的类型关系

2. **编译器优化**
   - 优化模板实例化流程
   - 减少代码生成开销
   - 实现更好的错误恢复

3. **文档和测试**
   - 完善泛型功能文档
   - 增加泛型功能测试用例
   - 提供更多示例代码

---

## 社区参与

欢迎社区参与以下方面：

1. **功能设计**
   - 讨论API设计
   - 提出功能建议
   - 参与架构讨论

2. **代码贡献**
   - 实现新功能
   - 修复bug
   - 优化性能

3. **文档和测试**
   - 编写文档
   - 添加测试用例
   - 提供示例代码

4. **反馈和问题**
   - 报告bug
   - 提出改进建议
   - 分享使用经验

---

## 变更说明

本规划可能会根据以下因素进行调整：

1. **用户反馈**
   - 根据用户需求调整功能优先级
   - 根据使用情况优化功能设计

2. **技术挑战**
   - 某些功能可能需要更多时间实现
   - 可能需要重新设计某些功能

3. **资源分配**
   - 根据开发资源调整发布时间表
   - 可能需要合并或拆分某些版本

---

**最后更新时间：2026-03-01**
