# Nova STL 库完整更新日志

本文档包含 Nova STL 库所有版本的更新记录。

---

## [0.1.0] - 2026-03-03 ✅ 已完成

### 新增功能

#### 1. 容器系统
- **Vector<T>** - 动态数组，支持随机访问
  - push, pop, get, set, insert, remove, clear
  - sort, reverse, count, isEmpty

- **List<T>** - 双向链表
  - pushFront, pushBack, popFront, popBack
  - insert, remove, get, set, clear
  - reverse, count, isEmpty

- **Stack<T>** - 栈（LIFO）
  - push, pop, top, isEmpty, clear

- **Queue<T>** - 队列（FIFO）
  - enqueue, dequeue, front, isEmpty, clear

- **Set<T>** - 集合（唯一元素）
  - add, remove, contains, size, isEmpty, clear

- **Map<K, V>** - 映射（键值对）
  - set, get, contains, remove, size, isEmpty, clear

- **Deque<T>** - 双端队列
  - pushFront, pushBack, popFront, popBack
  - front, back, count, isEmpty, clear

- **Heap<T>** - 堆/优先队列
  - push, pop, top, isEmpty, clear
  - 支持最大堆和最小堆

- **Trie<T>** - 前缀树
  - insert, search, contains, delete
  - startsWith, keys, keysWithPrefix

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
- **排序算法**
  - sort - 排序
  - reverse - 反转

- **查找算法**
  - find - 查找元素
  - binarySearch - 二分查找
  - count - 计数

- **修改算法**
  - transform - 元素转换
  - accumulate - 累加
  - inner_product - 内积
  - partial_sum - 部分和
  - adjacent_difference - 相邻差值

- **排列组合**
  - next_permutation - 下一个排列
  - prev_permutation - 上一个排列

#### 5. 数值算法
- **基础运算**
  - gcd - 最大公约数
  - lcm - 最小公倍数
  - power - 快速幂

- **数学函数**
  - factorial - 阶乘
  - fibonacci - 斐波那契数列
  - isPrime - 素数检查

- **序列生成**
  - iota - 递增序列
  - exclusive_scan - 独占扫描
  - inclusive_scan - 包含扫描

#### 6. 类型系统
- **Option<T>** - 可选值类型
  - Some(value) - 有值
  - None - 无值
  - isSome, isNone, unwrap, unwrapOr

- **TypeTraits** - 类型特征
  - 类型检查和类型推断支持

### 版本存档
- 完整版本存档位于 `versions/0.1.0/`
- 包含所有 STL 源代码文件、version.py、CHANGELOG.md、README.md

---

## 版本历史

| 版本号 | 发布日期 | 版本名称 | 状态 |
|---------|----------|----------|------|
| 0.1.0 | 2026-03-03 | Initial STL Release | ✅ 已完成 |
