# Nova STL 库

Nova STL (Standard Template Library) 是为Nova语言设计的标准模板库，提供了丰富的泛型容器、算法和函数对象。

## 目录结构

```
src/nova/stdlib/stl/
├── iterator.nova      # 迭代器系统
├── functional.nova    # 函数对象和比较器
├── vector.nova       # 动态数组容器
├── list.nova         # 双向链表容器
├── stack_queue.nova   # 栈和队列容器
├── set_map.nova      # 集合和映射容器
├── algorithm.nova     # 排序和查找算法
└── numeric.nova      # 变换和数值算法
```

## 核心组件

### 1. 迭代器系统

提供了多种迭代器类型，用于遍历容器：

- `Iterator<T>`: 基础迭代器
- `RandomAccessIterator<T>`: 随机访问迭代器
- `BidirectionalIterator<T>`: 双向迭代器
- `ForwardIterator<T>`: 前向迭代器
- `InputIterator<T>`: 输入迭代器
- `OutputIterator<T>`: 输出迭代器

### 2. 函数对象和比较器

提供了常用的函数对象和比较器：

#### 比较器
- `Less<T>`: 小于比较
- `Greater<T>`: 大于比较
- `EqualTo<T>`: 等于比较
- `NotEqualTo<T>`: 不等于比较
- `LessEqual<T>`: 小于等于比较
- `GreaterEqual<T>`: 大于等于比较

#### 算术函数对象
- `Plus<T>`: 加法
- `Minus<T>`: 减法
- `Multiplies<T>`: 乘法
- `Divides<T>`: 除法
- `Modulus<T>`: 取模
- `Negate<T>`: 取反

#### 逻辑函数对象
- `LogicalAnd`: 逻辑与
- `LogicalOr`: 逻辑或
- `LogicalNot`: 逻辑非

### 3. 序列容器

#### Vector<T>
动态数组容器，支持随机访问。

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(3);
print(vec.get(0));  // 输出: 1
print(vec.count()); // 输出: 3
```

**主要方法：**
- `push(value)`: 添加元素到末尾
- `pop()`: 移除并返回末尾元素
- `get(index)`: 获取指定索引的元素
- `set(index, value)`: 设置指定索引的元素
- `insert(index, value)`: 在指定位置插入元素
- `remove(index)`: 移除指定位置的元素
- `clear()`: 清空容器
- `isEmpty()`: 判断是否为空
- `contains(value)`: 判断是否包含指定元素
- `indexOf(value)`: 查找元素的索引
- `sort()`: 排序
- `reverse()`: 反转
- `toArray()`: 转换为数组

#### List<T>
双向链表容器，支持快速插入和删除。

```nova
var list = List<int>();
list.pushBack(1);
list.pushBack(2);
list.pushFront(0);
print(list.front());  // 输出: 0
print(list.back());   // 输出: 2
```

**主要方法：**
- `pushFront(value)`: 添加元素到头部
- `pushBack(value)`: 添加元素到尾部
- `popFront()`: 移除并返回头部元素
- `popBack()`: 移除并返回尾部元素
- `front()`: 获取头部元素
- `back()`: 获取尾部元素
- `insert(index, value)`: 在指定位置插入元素
- `remove(index)`: 移除指定位置的元素
- `reverse()`: 反转链表

#### Stack<T>
栈容器，后进先出（LIFO）。

```nova
var stack = Stack<int>();
stack.push(1);
stack.push(2);
print(stack.top());  // 输出: 2
print(stack.pop()); // 输出: 2
```

**主要方法：**
- `push(value)`: 压入元素
- `pop()`: 弹出元素
- `top()`: 获取栈顶元素
- `isEmpty()`: 判断是否为空
- `size()`: 获取大小

#### Queue<T>
队列容器，先进先出（FIFO）。

```nova
var queue = Queue<int>();
queue.enqueue(1);
queue.enqueue(2);
print(queue.front());  // 输出: 1
print(queue.dequeue()); // 输出: 1
```

**主要方法：**
- `enqueue(value)`: 入队
- `dequeue()`: 出队
- `front()`: 获取队首元素
- `back()`: 获取队尾元素
- `isEmpty()`: 判断是否为空
- `size()`: 获取大小

#### PriorityQueue<T>
优先队列容器，元素按优先级排序。

```nova
var pq = PriorityQueue<int>();
pq.push(3);
pq.push(1);
pq.push(2);
print(pq.top());  // 输出: 3
print(pq.pop()); // 输出: 3
```

**主要方法：**
- `push(value)`: 插入元素
- `pop()`: 移除并返回最高优先级元素
- `top()`: 获取最高优先级元素
- `isEmpty()`: 判断是否为空
- `size()`: 获取大小

### 4. 关联容器

#### Set<T>
集合容器，存储唯一元素。

```nova
var set = Set<int>();
set.insert(1);
set.insert(2);
set.insert(1);  // 重复元素不会被添加
print(set.size());  // 输出: 2
print(set.contains(1));  // 输出: true
```

**主要方法：**
- `insert(value)`: 插入元素
- `remove(value)`: 移除元素
- `contains(value)`: 判断是否包含元素
- `size()`: 获取大小
- `union(other)`: 并集
- `intersection(other)`: 交集
- `difference(other)`: 差集
- `isSubset(other)`: 判断是否为子集

#### Map<K, V>
映射容器，存储键值对。

```nova
var map = Map<string, int>();
map.insert("one", 1);
map.insert("two", 2);
print(map.get("one"));  // 输出: 1
print(map.contains("two"));  // 输出: true
```

**主要方法：**
- `insert(key, value)`: 插入键值对
- `get(key)`: 获取键对应的值
- `remove(key)`: 移除键值对
- `contains(key)`: 判断是否包含键
- `size()`: 获取大小
- `keys()`: 获取所有键
- `values()`: 获取所有值
- `entries()`: 获取所有键值对

### 5. 算法库

#### 排序和查找算法

```nova
var vec = Vector<int>();
vec.push(3);
vec.push(1);
vec.push(2);

sort(vec);  // 排序
var index = find(vec, 2);  // 查找元素
var minVal = minElement(vec);  // 最小值
var maxVal = maxElement(vec);  // 最大值
```

**主要算法：**
- `sort(data)`: 排序
- `reverse(data)`: 反转
- `find(data, value)`: 查找元素
- `findIf(data, predicate)`: 根据条件查找
- `binarySearch(data, value)`: 二分查找
- `lowerBound(data, value)`: 下界
- `upperBound(data, value)`: 上界
- `count(data, value)`: 计数
- `countIf(data, predicate)`: 根据条件计数
- `min(a, b)`: 最小值
- `max(a, b)`: 最大值
- `minElement(data)`: 最小元素
- `maxElement(data)`: 最大元素
- `clamp(value, min, max)`: 限制范围

#### 变换和数值算法

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(3);

var doubled = map(vec, func(x: int): int {
    return x * 2;
});  // 映射

var filtered = filter(vec, func(x: int): bool {
    return x > 1;
});  // 过滤

var sum = accumulate(vec, 0);  // 求和
```

**主要算法：**
- `transform(data, fn)`: 变换
- `map(data, fn)`: 映射
- `filter(data, predicate)`: 过滤
- `reduce(data, initial, reducer)`: 归约
- `accumulate(data, initial)`: 累加
- `forEach(data, fn)`: 遍历
- `copy(source, destination, count)`: 复制
- `fill(data, value, count)`: 填充
- `rotate(data, first, middle, last)`: 旋转
- `partition(data, predicate)`: 分区
- `iota(data, start, step)`: 生成序列

## 使用示例

### 完整示例

```nova
func main() {
    // 使用Vector
    var vec = Vector<int>();
    vec.push(1);
    vec.push(2);
    vec.push(3);
    print("Vector: " + vec.toArray().toString());
    
    // 使用List
    var list = List<int>();
    list.pushBack(1);
    list.pushBack(2);
    print("List: " + list.toArray().toString());
    
    // 使用Stack
    var stack = Stack<int>();
    stack.push(1);
    stack.push(2);
    print("Stack top: " + stack.top());
    
    // 使用Queue
    var queue = Queue<int>();
    queue.enqueue(1);
    queue.enqueue(2);
    print("Queue front: " + queue.front());
    
    // 使用Set
    var set = Set<int>();
    set.insert(1);
    set.insert(2);
    print("Set size: " + set.size());
    
    // 使用Map
    var map = Map<string, int>();
    map.insert("one", 1);
    map.insert("two", 2);
    print("Map get: " + map.get("one"));
    
    // 使用算法
    sort(vec);
    print("Sorted: " + vec.toArray().toString());
    
    var filtered = filter(vec, func(x: int): bool {
        return x > 1;
    });
    print("Filtered: " + filtered.toArray().toString());
}
```

## 设计特点

1. **完全自定义设计**: 根据Nova语言的特点设计，不直接模仿C++ STL
2. **泛型支持**: 所有容器和算法都支持泛型类型参数
3. **类型安全**: 编译时类型检查，确保类型安全
4. **易于使用**: 提供简洁直观的API
5. **高性能**: 针对Nova语言优化，提供良好的性能

## 运行测试

要运行STL库的测试用例：

```bash
python -m nova run examples/stl_test.nova
```

## 版本信息

- 当前版本: 0.10.1
- 发布日期: 2026-03-01
- 状态: 开发中

## 未来计划

1. 添加更多容器（如Deque、HashSet、HashMap）
2. 实现更高效的算法（如快速排序、归并排序）
3. 添加更多迭代器功能
4. 提供更多的函数对象
5. 优化性能和内存使用

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

MIT License
