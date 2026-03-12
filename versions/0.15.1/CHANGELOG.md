# Changelog

所有版本的更新日志都记录在 [CHANGELOG_ALL.md](CHANGELOG_ALL.md) 中。

## [0.15.1] - 2026-03-05

### Bug修复

#### 1. Vector实现简化
- **简化NovaVector类**：使用Python列表作为底层存储，简化实现
- **修复递归调用问题**：NovaVector.remove()方法中的递归调用导致栈溢出，已修复为使用list.remove()

#### 2. 关键Bug修复
- **修复数组len方法**：在generator.py中添加了对数组类型len方法的特殊处理
- **修复COMPARE_EQ指令**：处理NotImplemented返回值的情况
- **修复跳转指令标签映射**：JUMP、JUMP_IF_TRUE、JUMP_IF_FALSE指令现在正确将标签名称转换为指令索引

#### 3. 代码清理
- **删除冗余代码**：删除了analyzer.py中未使用的_parse_stl_files()和_initialize_array_type()方法

### 测试结果
- ✅ test_object_compare.nova - 对象比较测试通过
- ✅ test_multiple_trait_constraints.nova - 多Trait约束测试通过
- ✅ test_vector_traits.nova - Vector Trait测试通过

---

## [0.15.0] - 2026-03-04

### 新增功能

#### 1. 泛型Trait系统
- **Trait定义**
  - 支持泛型Trait定义，如 `trait Display<T>`
  - Trait方法支持泛型参数和返回类型
  - Trait约束检查，确保类型实现所需方法

- **Impl块**
  - 支持为特定类型实现Trait
  - 泛型Impl块，如 `impl Display<T> for Array<T>`
  - Trait方法调用支持

- **标准Traits**
  - Display<T>：提供toString方法
  - Comparable<T>：提供比较方法
  - Iterable<T>：提供迭代功能

#### 2. 编译器优化系统
- **优化级别支持**
  - `-O0`：无优化（默认）
  - `-O1`：部分优化（常量折叠）
  - `-O2`：高度优化（常量折叠 + 死代码消除）
  - `-O3`：极度优化（常量折叠 + 死代码消除 + 尾递归优化）

- **优化Pass实现**
  - **ConstantFolding**：常量折叠优化
    - 在编译时计算常量表达式
    - 支持算术运算：+、-、*、/、%
    - 自动类型推断（int/float）

  - **DeadCodeElimination**：死代码消除优化
    - 移除永远不会执行的代码
    - 清理无用的分支和语句

  - **TailRecursionOptimization**：尾递归优化
    - 检测尾递归函数
    - 将尾递归转换为迭代
    - 避免栈溢出

#### 3. 命令行接口增强
- **repl命令**
  - 支持 `-O0`、`-O1`、`-O2`、`-O3` 参数
  - 示例：`python script.py repl -O1`

- **run命令**
  - 支持优化级别参数
  - 示例：`python script.py run program.nova -O2`

- **compile命令**
  - 支持优化级别参数
  - 示例：`python script.py compile program.nova -O3`

### 测试
- 新增泛型Trait测试用例 test_0_15_0_simple.nova
- 新增优化功能测试用例 test_constant_folding.nova
- 验证优化级别功能和优化Pass正确性
- 所有测试用例均通过

### 版本存档
- 完整版本存档位于 `versions/0.15.0/`
- 包含完整的 src 目录、version.py、CHANGELOG.md、README.md

查看完整更新记录：[CHANGELOG_ALL.md](CHANGELOG_ALL.md)
