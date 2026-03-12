# Changelog

所有版本的更新日志都记录在 [CHANGELOG_ALL.md](CHANGELOG_ALL.md) 中。

## [0.1.0] - 2026-03-03

### 新增功能

#### 1. 容器系统
- **Vector<T>** - 动态数组，支持随机访问
- **List<T>** - 双向链表
- **Stack<T>** - 栈（LIFO）
- **Queue<T>** - 队列（FIFO）
- **Set<T>** - 集合（唯一元素）
- **Map<K, V>** - 映射（键值对）
- **Deque<T>** - 双端队列
- **Heap<T>** - 堆/优先队列
- **Trie<T>** - 前缀树

#### 2. 迭代器系统
- **Iterator<T>** - 基础迭代器接口
- **RandomAccessIterator<T>** - 随机访问迭代器
- **BidirectionalIterator<T>** - 双向迭代器

#### 3. 函数对象和比较器
- **Less<T>** - 小于比较
- **Greater<T>** - 大于比较
- **EqualTo<T>** - 等于比较
- **Plus<T>** - 加法
- **Minus<T>** - 减法
- **Multiplies<T>** - 乘法
- **Divides<T>** - 除法

#### 4. 算法库
- **排序算法**：sort, reverse
- **查找算法**：find, binarySearch, count
- **修改算法**：transform, accumulate, inner_product, partial_sum, adjacent_difference
- **排列组合**：next_permutation, prev_permutation

#### 5. 数值算法
- **基础运算**：gcd, lcm, power
- **数学函数**：factorial, fibonacci, isPrime
- **序列生成**：iota, exclusive_scan, inclusive_scan

#### 6. 类型系统
- **Option<T>** - 可选值类型
- **TypeTraits** - 类型特征

### 版本存档
- 完整版本存档位于 `versions/0.1.0/`
- 包含所有 STL 源代码文件、version.py、CHANGELOG.md、README.md

查看完整更新记录：[CHANGELOG_ALL.md](CHANGELOG_ALL.md)
