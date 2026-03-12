# STL 容器 Trait 实现方案

## 概述

本文档描述了如何为 STL 容器实现标准 Traits，以支持泛型接口和更好的类型安全。

## 标准 Traits 定义

已定义的标准 Traits（位于 traits.nova）：

### 迭代器 Traits
- `Iterator<T>` - 基础迭代器
- `RandomAccessIterator<T>` - 随机访问迭代器
- `BidirectionalIterator<T>` - 双向迭代器
- `ForwardIterator<T>` - 前向迭代器
- `InputIterator<T>` - 输入迭代器
- `OutputIterator<T>` - 输出迭代器

### 比较 Traits
- `Comparable<T>` - 可比较
- `Equatable<T>` - 可相等比较

### 复制 Traits
- `Cloneable<T>` - 可复制
- `Default<T>` - 默认值

### 其他 Traits
- `Hashable` - 可哈希
- `Printable` - 可打印
- `Sized` - 可获取大小
- `Container<T>` - 容器
- `Sequence<T>` - 序列
- `Collection<T>` - 集合

## 容器 Trait 实现计划

### 1. Vector<T>

**需要实现的 Traits**:
- `RandomAccessIterator<T>` - 通过 VectorIterator<T>
- `Sized` - 提供 size() 和 isEmpty()
- `Container<T>` - 提供 clear() 和 contains()
- `Sequence<T>` - 提供 first() 和 last()
- `Collection<T>` - 提供 add()、remove() 和 toArray()

**实现方式**:
```nova
impl<T> RandomAccessIterator<T> for VectorIterator<T> {
    func next(): T { ... }
    func hasNext(): bool { ... }
    func prev(): T { ... }
    func hasPrev(): bool { ... }
    func get(index: int): T { ... }
    func set(index: int, value: T) { ... }
}

impl<T> Sized for Vector<T> {
    func size(): int { return this.count(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<T> Container<T> for Vector<T> {
    func clear() { this.clear(); }
    func contains(value: T): bool { return this.contains(value); }
}

impl<T> Sequence<T> for Vector<T> {
    func first(): T { return this.front(); }
    func last(): T { return this.back(); }
}

impl<T> Collection<T> for Vector<T> {
    func add(value: T) { this.push(value); }
    func remove(value: T) { this.remove(this.indexOf(value)); }
    func toArray(): [T] { return this.toArray(); }
}
```

### 2. List<T>

**需要实现的 Traits**:
- `BidirectionalIterator<T>` - 通过 ListIterator<T>
- `Sized` - 提供 size() 和 isEmpty()
- `Container<T>` - 提供 clear() 和 contains()
- `Sequence<T>` - 提供 first() 和 last()
- `Collection<T>` - 提供 add()、remove() 和 toArray()

**实现方式**:
```nova
impl<T> BidirectionalIterator<T> for ListIterator<T> {
    func next(): T { ... }
    func hasNext(): bool { ... }
    func prev(): T { ... }
    func hasPrev(): bool { ... }
}

impl<T> Sized for List<T> {
    func size(): int { return this.count(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<T> Container<T> for List<T> {
    func clear() { this.clear(); }
    func contains(value: T): bool { return this.contains(value); }
}

impl<T> Sequence<T> for List<T> {
    func first(): T { return this.front(); }
    func last(): T { return this.back(); }
}

impl<T> Collection<T> for List<T> {
    func add(value: T) { this.pushBack(value); }
    func remove(value: T) { this.remove(this.indexOf(value)); }
    func toArray(): [T] { return this.toArray(); }
}
```

### 3. Deque<T>

**需要实现的 Traits**:
- `RandomAccessIterator<T>` - 通过 DequeIterator<T>
- `Sized` - 提供 size() 和 isEmpty()
- `Container<T>` - 提供 clear() 和 contains()
- `Sequence<T>` - 提供 first() 和 last()
- `Collection<T>` - 提供 add()、remove() 和 toArray()

**实现方式**:
```nova
impl<T> RandomAccessIterator<T> for DequeIterator<T> {
    func next(): T { ... }
    func hasNext(): bool { ... }
    func prev(): T { ... }
    func hasPrev(): bool { ... }
    func get(index: int): T { ... }
    func set(index: int, value: T) { ... }
}

impl<T> Sized for Deque<T> {
    func size(): int { return this.count(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<T> Container<T> for Deque<T> {
    func clear() { this.clear(); }
    func contains(value: T): bool { return this.contains(value); }
}

impl<T> Sequence<T> for Deque<T> {
    func first(): T { return this.front(); }
    func last(): T { return this.back(); }
}

impl<T> Collection<T> for Deque<T> {
    func add(value: T) { this.pushBack(value); }
    func remove(value: T) { this.remove(this.indexOf(value)); }
    func toArray(): [T] { return this.toArray(); }
}
```

### 4. Stack<T>

**需要实现的 Traits**:
- `Sized` - 提供 size() 和 isEmpty()
- `Container<T>` - 提供 clear() 和 contains()

**实现方式**:
```nova
impl<T> Sized for Stack<T> {
    func size(): int { return this.count(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<T> Container<T> for Stack<T> {
    func clear() { this.clear(); }
    func contains(value: T): bool { return this.contains(value); }
}
```

### 5. Queue<T>

**需要实现的 Traits**:
- `Sized` - 提供 size() 和 isEmpty()
- `Container<T>` - 提供 clear() 和 contains()

**实现方式**:
```nova
impl<T> Sized for Queue<T> {
    func size(): int { return this.count(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<T> Container<T> for Queue<T> {
    func clear() { this.clear(); }
    func contains(value: T): bool { return this.contains(value); }
}
```

### 6. Set<T>

**需要实现的 Traits**:
- `Sized` - 提供 size() 和 isEmpty()
- `Container<T>` - 提供 clear() 和 contains()
- `Collection<T>` - 提供 add()、remove() 和 toArray()

**实现方式**:
```nova
impl<T> Sized for Set<T> {
    func size(): int { return this.size(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<T> Container<T> for Set<T> {
    func clear() { this.clear(); }
    func contains(value: T): bool { return this.contains(value); }
}

impl<T> Collection<T> for Set<T> {
    func add(value: T) { this.add(value); }
    func remove(value: T) { this.remove(value); }
    func toArray(): [T] { return this.toArray(); }
}
```

### 7. Map<K, V>

**需要实现的 Traits**:
- `Sized` - 提供 size() 和 isEmpty()
- `Container<K>` - 提供 clear() 和 contains()

**实现方式**:
```nova
impl<K, V> Sized for Map<K, V> {
    func size(): int { return this.size(); }
    func isEmpty(): bool { return this.isEmpty(); }
}

impl<K, V> Container<K> for Map<K, V> {
    func clear() { this.clear(); }
    func contains(key: K): bool { return this.contains(key); }
}
```

## 算法库 Trait 约束

### 排序算法

```nova
generic func sort<T>(list: List<T>)
where T: Comparable<T>
{
    // 使用 T.compareTo() 进行排序
}
```

### 查找算法

```nova
generic func find<T>(list: List<T>, value: T): int
where T: Equatable<T>
{
    // 使用 T.equals() 进行查找
}
```

### 映射算法

```nova
generic func map<T, U>(list: List<T>, f: func(T): U): List<U> {
    var result = List<U>();
    var iter = list.iterator();
    while iter.hasNext() {
        result.pushBack(f(iter.next()));
    }
    return result;
}
```

### 过滤算法

```nova
generic func filter<T>(list: List<T>, predicate: func(T): bool): List<T> {
    var result = List<T>();
    var iter = list.iterator();
    while iter.hasNext() {
        var value = iter.next();
        if predicate(value) {
            result.pushBack(value);
        }
    }
    return result;
}
```

### 归约算法

```nova
generic func reduce<T, U>(list: List<T>, initial: U, f: func(U, T): U): U {
    var result = initial;
    var iter = list.iterator();
    while iter.hasNext() {
        result = f(result, iter.next());
    }
    return result;
}
```

## 实现优先级

### 第一阶段（高优先级）
1. 实现 Vector<T> 的 Traits
2. 实现 List<T> 的 Traits
3. 实现基础算法的 Trait 约束

### 第二阶段（中优先级）
1. 实现 Deque<T> 的 Traits
2. 实现 Set<T> 和 Map<K, V> 的 Traits
3. 实现 Stack<T> 和 Queue<T> 的 Traits
4. 完善算法库的 Trait 约束

### 第三阶段（低优先级）
1. 实现高级 Traits（Cloneable、Default、Hashable）
2. 性能优化
3. 代码重构和清理

## 依赖关系

### 依赖泛型程序员的功能
- 泛型 Trait 定义语法：`trait Iterator<T> { ... }`
- 泛型 Impl 块语法：`impl<T> Iterator<T> for List<T> { ... }`
- 泛型函数 Trait 约束：`generic func sort<T>(list: List<T>) where T: Comparable<T>`

### 泛型程序员依赖 STL 程序员的功能
- 标准 Traits 定义
- STL 容器的 Trait 实现
- 算法库的 Trait 约束示例

## 测试计划

### 单元测试
1. 测试每个容器的 Trait 实现
2. 测试每个算法的 Trait 约束
3. 测试 Trait 约束检查的正确性

### 集成测试
1. 测试 Trait 约束的泛型函数
2. 测试 Trait 约束的算法库
3. 测试 Trait 约束的类型推断

### 联合测试
1. 编写 `test_0_15_0_generic_traits.nova`
2. 测试泛型 Trait 和 STL 实现的协同工作
3. 测试完整的 Trait 约束检查流程

## 注意事项

1. **类型安全**: 确保 Trait 约束在编译时正确检查
2. **性能**: 避免不必要的类型转换和包装
3. **兼容性**: 保持与现有 STL 代码的兼容性
4. **可扩展性**: 设计易于扩展的 Trait 系统
5. **文档**: 为每个 Trait 提供清晰的文档和示例

## 后续工作

1. 实现更多标准 Traits（如 Hashable、Cloneable）
2. 为更多容器实现 Traits
3. 优化 Trait 约束检查性能
4. 提供更详细的 Trait 错误信息
5. 实现 Trait 继承和组合
