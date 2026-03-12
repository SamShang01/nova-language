# Nova 语言更新日志

## [0.11.0] - 2026-03-01
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

### 测试
- 添加 `test_generic_struct.nova` 测试文件
  - 测试泛型结构体 `Point<T>` 的创建和实例化
  - 测试多种类型参数（int、float、string）
  - 测试泛型结构体方法的调用

- 添加 `test_generic_function.nova` 测试文件
  - 测试泛型函数 `identity<T>` 的调用
  - 测试多种类型参数（int、float、string）
  - 测试泛型函数返回值

## [0.10.1] - 2026-03-01
### 新增
- **STL库（标准模板库）**：
  - **迭代器系统**：
    - 实现 `Iterator<T>` 基础迭代器
    - 实现 `RandomAccessIterator<T>` 随机访问迭代器
    - 实现 `BidirectionalIterator<T>` 双向迭代器
    - 实现 `ForwardIterator<T>` 前向迭代器
    - 实现 `InputIterator<T>` 输入迭代器
    - 实现 `OutputIterator<T>` 输出迭代器

  - **函数对象和比较器**：
    - 实现比较器：`Less<T>`、`Greater<T>`、`EqualTo<T>`、`NotEqualTo<T>`、`LessEqual<T>`、`GreaterEqual<T>`
    - 实现算术函数对象：`Plus<T>`、`Minus<T>`、`Multiplies<T>`、`Divides<T>`、`Modulus<T>`、`Negate<T>`
    - 实现逻辑函数对象：`LogicalAnd`、`LogicalOr`、`LogicalNot`

  - **序列容器**：
    - 实现 `Vector<T>` 动态数组容器，支持随机访问、动态扩容、排序、反转等操作
    - 实现 `List<T>` 双向链表容器，支持快速插入删除、双向遍历
    - 实现 `Stack<T>` 栈容器，支持后进先出（LIFO）操作
    - 实现 `Queue<T>` 队列容器，支持先进先出（FIFO）操作
    - 实现 `PriorityQueue<T>` 优先队列容器，支持按优先级排序

  - **关联容器**：
    - 实现 `Set<T>` 集合容器，支持唯一元素存储、并集、交集、差集操作
    - 实现 `Map<K, V>` 映射容器，支持键值对存储、快速查找
    - 实现 `Pair<K, V>` 键值对结构体

  - **算法库**：
    - **排序和查找算法**：
      - `sort<T>(data)` 排序算法
      - `reverse<T>(data)` 反转算法
      - `find<T>(data, value)` 查找元素
      - `findIf<T>(data, predicate)` 条件查找
      - `binarySearch<T>(data, value)` 二分查找
      - `lowerBound<T>(data, value)` 下界查找
      - `upperBound<T>(data, value)` 上界查找
      - `count<T>(data, value)` 计数
      - `countIf<T>(data, predicate)` 条件计数
      - `allOf<T>(data, predicate)` 全部满足条件
      - `anyOf<T>(data, predicate)` 任一满足条件
      - `noneOf<T>(data, predicate)` 全部不满足条件
      - `min<T>(a, b)` 最小值
      - `max<T>(a, b)` 最大值
      - `minElement<T>(data)` 最小元素
      - `maxElement<T>(data)` 最大元素
      - `clamp<T>(value, min, max)` 限制范围
