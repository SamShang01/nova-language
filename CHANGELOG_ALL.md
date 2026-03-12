# Nova 语言完整更新日志

本文档包含Nova语言所有版本的更新记录。

---

## [1.0.0] - 2026-03-12 ✅ 正式发布

### 🎉 Nova语言 1.0.0 正式发布！

这是Nova语言的第一个正式版本，标志着Nova语言已经准备好用于生产环境。

### ✨ 核心功能

#### 1. 完整的编译器系统
- **词法分析器**：支持完整的Nova语法标记化
- **语法分析器**：支持表达式、语句、函数、结构体、类等所有语法结构
- **语义分析器**：完整的类型检查、作用域管理和符号解析
- **代码生成器**：生成高效的虚拟机字节码
- **LLVM JIT编译器**：可选的LLVM后端，提供更高的执行性能

#### 2. 强大的类型系统
- **基本类型**：int、float、bool、string、unit
- **复合类型**：数组、元组、字典、集合
- **自定义类型**：结构体(struct)、类(class)、枚举(enum)
- **泛型系统**：泛型函数、泛型结构体、泛型类
- **Trait系统**：接口-like功能，支持类型约束和多态

#### 3. 丰富的标准库
- **核心模块**：基础函数、类型转换、错误处理
- **IO模块**：文件操作、输入输出流
- **数学模块**：数学函数、随机数生成、统计函数
- **字符串模块**：字符串处理、正则表达式
- **集合模块**：列表、字典、集合等数据结构
- **STL库**：标准模板库，提供通用数据结构和算法

#### 4. 开发工具
- **REPL交互式解释器**：支持命令、自动补全、语法高亮
- **VS Code插件**：语法高亮、代码片段、智能提示
- **Nova IDE**：基于PyQt5的集成开发环境
- **包管理系统**：安装、卸载、更新、管理包
- **调试器**：断点、单步执行、变量查看
- **性能分析器**：代码性能分析和优化建议

#### 5. 编译优化
- **增量编译**：只重新编译修改的文件
- **并行编译**：多线程编译，支持GPU加速
- **编译优化**：常量折叠、死代码消除、尾递归优化
- **缓存系统**：编译缓存，加速重复编译

#### 6. 语言特性
- **模式匹配**：强大的模式匹配功能
- **闭包和Lambda**：支持匿名函数和闭包
- **迭代器**：for-in循环、迭代器协议
- **错误处理**：Result类型、try-catch异常处理
- **模块系统**：import/export、命名空间管理
- **异步编程**：async/await、Future、Task

### 🔒 稳定性和兼容性

- **100+测试用例**：全面的测试覆盖
- **持续集成**：自动化测试和构建
- **向后兼容**：承诺API稳定性
- **长期支持**：1.x版本长期维护

### 版本存档
- 完整版本存档位于 `versions/1.0.0/`
- 包含完整的 src 目录、version.py、CHANGELOG.md、README.md

---

## [0.16.0] - 2026-03-06 ✅ 已完成
### 新增
- **基于LLVM的JIT编译器**：
  - 使用llvmlite库实现即时编译
  - 通过LLVM优化提高Nova代码执行速度
  - 生成LLVM中间表示，支持进一步优化
  - 直接在内存中编译和执行代码

- **包管理系统**：
  - 包安装：支持安装指定版本的包
  - 包卸载：移除已安装的包
  - 包更新：更新包到最新版本
  - 包列表：查看已安装的包
  - 包信息：获取包的详细信息
  - 命令行支持：通过`nova package`命令管理包

- **并行编译能力增强**：
  - 多线程编译：利用多核CPU并行处理多个文件
  - GPU加速：支持使用GPU进行编译加速
  - 增量编译：结合增量编译系统，只重新编译修改的文件
  - 并行编译器管理器：单例模式管理并行编译资源

- **标准库功能完善**：
  - 核心模块：新增更多实用函数，如sorted、reversed、any、all等
  - 字符串模块：增强字符串处理能力，添加capitalize、title、swapcase等方法
  - 数学模块：提供完整的数学函数支持
  - 集合模块：完善列表、字典、集合等数据结构操作

### 版本存档
- 完整版本存档位于 `versions/0.16.0/`
- 包含完整的 src 目录、version.py、CHANGELOG.md、README.md

---

## [0.15.1] - 2026-03-05 ✅ 已完成
### Bug修复
- **Vector实现简化**：使用Python列表作为底层存储，简化NovaVector类
- **修复递归调用问题**：NovaVector.remove()方法中的递归调用导致栈溢出
- **修复数组len方法**：在generator.py中添加对数组类型len方法的特殊处理
- **修复COMPARE_EQ指令**：处理NotImplemented返回值的情况
- **修复跳转指令标签映射**：JUMP、JUMP_IF_TRUE、JUMP_IF_FALSE指令正确转换标签为指令索引
- **代码清理**：删除analyzer.py中未使用的冗余方法

### 测试
- `test_object_compare.nova` - 对象比较测试通过
- `test_multiple_trait_constraints.nova` - 多Trait约束测试通过
- `test_vector_traits.nova` - Vector Trait测试通过

---

## [0.15.0] - 2026-03-04 ✅ 已完成
### 新增
- **泛型Trait系统**：
  - Trait定义：`trait Display<T> { ... }`
  - Impl块：`impl Display<T> for Array<T> { ... }`
  - Trait约束检查
  - Trait方法调用支持

- **编译器优化系统**：
  - 优化级别支持：`-O0`（无优化）、`-O1`（部分优化）、`--O2`（高度优化）、`-O3`（极度优化）
  - ConstantFolding：常量折叠优化
  - DeadCodeElimination：死代码消除优化
  - TailRecursionOptimization：尾递归优化

- **命令行接口增强**：
  - repl命令支持优化级别参数
  - run命令支持优化级别参数
  - compile命令支持优化级别参数

### 改进
- **优化Pass实现**：
  - 常量折叠：编译时计算常量表达式，支持+、-、*、/、%运算
  - 死代码消除：移除永远不会执行的代码
  - 尾递归优化：检测尾递归函数并转换为迭代

### 测试
- `test_0_15_0_simple.nova` - 泛型Trait测试
- `test_constant_folding.nova` - 优化功能测试
- 验证优化级别功能和优化Pass正确性

---

## [0.14.0] - 2026-03-03 ✅ 已完成
### 新增
- **新容器类型**：
  - `Deque<T>` - 双端队列，支持 O(1) 时间复杂度的两端插入删除
  - `Heap<T>` / `MinHeap<T>` / `MaxHeap<T>` - 堆/优先队列，支持最大堆和最小堆
  - `Trie<T>` / `StringTrie` - 前缀树/字典树，高效字符串存储检索

- **高级算法库** (`algorithm_advanced.nova`)：
  - 快速排序（Quick Sort）：平均 O(n log n) 时间复杂度
  - 归并排序（Merge Sort）：稳定排序，O(n log n) 时间复杂度
  - 堆排序（Heap Sort）：原地排序，O(n log n) 时间复杂度
  - 内省排序（Introspective Sort）：结合多种排序优势
  - 快速选择算法（Quick Select）：选择第 k 小元素
  - 三数取中法优化枢轴选择
  - 二分查找（Binary Search）：O(log n) 时间复杂度

- **高级数值算法** (`numeric_advanced.nova`)：
  - `transform` - 对范围内的每个元素应用函数
  - `accumulate` / `reduce` - 累加/归约操作
  - `inner_product` - 计算两个范围的内积
  - `partial_sum` / `adjacent_difference` - 部分和/相邻差值
  - `iota` - 递增序列填充
  - `exclusive_scan` / `inclusive_scan` - 扫描操作
  - `gcd` / `lcm` - 最大公约数/最小公倍数
  - `power` - 快速幂运算
  - `factorial` / `fibonacci` - 数学函数
  - `isPrime` - 素数检查
  - `next_permutation` / `prev_permutation` - 排列生成

- **泛型接口基础** (`test_generic_trait.nova`)：
  - 泛型 Trait 定义：`trait Iterator<T> { ... }`
  - 泛型 Impl 块：`impl<T> Iterator<T> for List<T> { ... }`
  - 泛型函数使用泛型 Trait 约束

### 改进
- **STL 性能优化**：
  - 添加高效排序算法（快速排序、归并排序）
  - 添加内省排序（结合多种排序优势）
  - 优化查找算法（二分查找 O(log n)）

### 测试
- `test_0_14_0_basic.nova` - 基础功能测试（数值计算、条件、循环、字符串、函数）
- `test_generic_trait.nova` - 泛型接口测试

### 版本存档
- 完整版本存档位于 `versions/0.14.0/`
- 包含完整的 src 目录、version.py、CHANGELOG.md、README.md

---

## [0.13.0] - 2026-03-03 ✅ 已完成
### 新增
- **Trait约束参数语法**：
  - 支持 `func printValue(value: Printable)` 简化语法
  - 参数类型为trait时，表示该参数必须实现指定的trait
  - 更简洁的语法，无需显式 `trait` 关键字
  - 与现代语言（Rust、Swift、Kotlin）保持一致
- **Trait约束检查功能**：
  - 实现了完整的 Trait 约束检查系统
  - 记录类型实现的 Trait 映射
  - 检查 Impl 块是否完整实现了 Trait 要求的所有方法
  - 支持泛型函数的 Trait 约束检查
  - 增强类型兼容性检查，支持 Trait 类型

### 改进
- **Trait系统基础**：
  - Trait定义语法：`trait Printable { func toString() -> string; }`
  - Trait方法签名定义
  - Trait类型在语义分析器中的注册

### 测试
- `test_trait_simple.nova` - 基本trait定义和实现测试
- `test_trait_param.nova` - trait约束参数测试
- `test_trait_constraints.nova` - 完整的trait约束检查测试

### 修复
- 修复了 Impl 块方法签名检查的兼容性问题

---

## [0.12.1] - 2026-03-02 ✅ 已完成
### 修复
- **多参数泛型结构体实例化问题**：
  - 修复 Parser 中 `BOOLEAN` token 未处理导致的 "Expect expression" 错误
  - 修复泛型类字段类型未正确解析的问题
  - 修复泛型类方法中 `this` 参数类型未正确设置的问题
  - 现在支持在泛型类方法中实例化多参数泛型结构体：`Node<T>(value, true, null)`

### 测试
- `test_stl_generic_struct.nova` 测试通过
  - 测试 `List<T>` 容器的完整功能
  - 测试 `ListNode<T>` 泛型结构体的多参数实例化

---

## [0.12.0] - 2026-03-01 ✅ 已完成
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
- 添加 `test_generic_function.nova` 测试文件
- 添加 `test_type_inference.nova` 测试文件

---

## [0.11.1] - 2026-03-01 ✅ 已完成
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

## [0.11.0] - 2026-03-01 ✅ 已完成
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

## [0.10.1] - 2026-03-01 ✅ 已完成
### 新增
- **STL库（标准模板库）**：
  - **迭代器系统**：Iterator, RandomAccessIterator, BidirectionalIterator等
  - **函数对象和比较器**：Less, Greater, EqualTo, Plus, Minus等
  - **序列容器**：Vector, List, Stack, Queue, PriorityQueue
  - **关联容器**：Set, Map, Pair
  - **算法库**：sort, reverse, find, binarySearch, count等

---

## [0.10.0] - 2026-03-01 ✅ 已完成
### 新增
- **模板功能**：
  - 添加 `template` 关键字支持泛型编程
  - 支持模板类定义：`template class ClassName<T> { ... }`
  - 支持多个类型参数：`template class ClassName<T, U, V> { ... }`
  - 支持模板类实例化：`ClassName<int>(42)`
  - 支持类型参数在字段和方法中使用
