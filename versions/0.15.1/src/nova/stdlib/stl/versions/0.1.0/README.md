# Nova STL 库 0.1.0 - Initial STL Release

## 库概述

Nova STL（Standard Template Library）是 Nova 语言的标准模板库，提供了一套完整的数据结构和算法实现，帮助开发者高效地编写代码。

## 主要特性

### 1. 容器系统

#### 序列容器
- **Vector<T>** - 动态数组，支持随机访问和动态扩容
- **List<T>** - 双向链表，支持高效的插入和删除
- **Deque<T>** - 双端队列，支持两端高效操作

#### 适配器容器
- **Stack<T>** - 栈（LIFO - 后进先出）
- **Queue<T>** - 队列（FIFO - 先进先出）

#### 关联容器
- **Set<T>** - 集合，存储唯一元素
- **Map<K, V>** - 映射，存储键值对

#### 特殊容器
- **Heap<T>** - 堆/优先队列，支持最大堆和最小堆
- **Trie<T>** - 前缀树，高效字符串存储和检索

### 2. 迭代器系统

- **Iterator<T>** - 基础迭代器接口
- **RandomAccessIterator<T>** - 随机访问迭代器
- **BidirectionalIterator<T>** - 双向迭代器

### 3. 函数对象和比较器

- **Less<T>** - 小于比较
- **Greater<T>** - 大于比较
- **EqualTo<T>** - 等于比较
- **Plus<T>** - 加法
- **Minus<T>** - 减法
- **Multiplies<T>** - 乘法
- **Divides<T>** - 除法

### 4. 算法库

#### 排序算法
- **sort** - 排序
- **reverse** - 反转

#### 查找算法
- **find** - 查找元素
- **binarySearch** - 二分查找
- **count** - 计数

#### 修改算法
- **transform** - 元素转换
- **accumulate** - 累加
- **inner_product** - 内积
- **partial_sum** - 部分和
- **adjacent_difference** - 相邻差值

#### 排列组合
- **next_permutation** - 下一个排列
- **prev_permutation** - 上一个排列

### 5. 数值算法

#### 基础运算
- **gcd** - 最大公约数
- **lcm** - 最小公倍数
- **power** - 快速幂

#### 数学函数
- **factorial** - 阶乘
- **fibonacci** - 斐波那契数列
- **isPrime** - 素数检查

#### 序列生成
- **iota** - 递增序列
- **exclusive_scan** - 独占扫描
- **inclusive_scan** - 包含扫描

### 6. 类型系统

- **Option<T>** - 可选值类型
  - Some(value) - 有值
  - None - 无值
  - isSome, isNone, unwrap, unwrapOr

- **TypeTraits** - 类型特征
  - 类型检查和类型推断支持

## 使用示例

### Vector 使用
```nova
var vec = Vector<int>();
vec.push(10);
vec.push(20);
vec.push(30);
print(vec.get(0)); // 10
```

### Map 使用
```nova
var map = Map<string, int>();
map.set("apple", 1);
map.set("banana", 2);
print(map.get("apple")); // 1
```

### Stack 使用
```nova
var stack = Stack<int>();
stack.push(10);
stack.push(20);
print(stack.pop()); // 20
```

### 算法使用
```nova
var vec = Vector<int>();
vec.push(3);
vec.push(1);
vec.push(4);
vec.push(1);
vec.push(5);
vec.sort();
// vec: [1, 1, 3, 4, 5]
```

## 文件结构

```
src/nova/stdlib/stl/versions/0.1.0/
├── algorithm.nova              # 基础算法
├── algorithm_advanced.nova      # 高级算法
├── algorithm_template.nova      # 算法模板
├── deque.nova                 # 双端队列
├── functional.nova            # 函数对象
├── heap.nova                 # 堆/优先队列
├── iterator.nova              # 迭代器
├── list.nova                 # 双向链表
├── numeric.nova              # 基础数值算法
├── numeric_advanced.nova      # 高级数值算法
├── numeric_template.nova      # 数值算法模板
├── option.nova               # 可选值类型
├── set_map.nova             # 集合和映射
├── stack_queue.nova          # 栈和队列
├── trie.nova                # 前缀树
├── type_traits.nova          # 类型特征
├── vector.nova               # 动态数组
├── version.py               # 版本信息
├── CHANGELOG.md             # 版本变更日志
└── README.md                # 版本说明
```

## 版本信息

- **版本号**: 0.1.0
- **发布日期**: 2026-03-03
- **版本名称**: Initial STL Release
- **状态**: ✅ 已发布

## 兼容性

- 适用于 Nova 编译器 0.10.0 及以上版本
- 支持泛型编程特性
- 支持模板类和模板函数

## 后续计划

- 0.2.0: 添加更多容器（如 BTree、Graph）
- 0.3.0: 优化算法性能
- 0.4.0: 添加并发容器
