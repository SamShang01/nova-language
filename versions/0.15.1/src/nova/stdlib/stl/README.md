# Nova STL 库 0.12.0

Nova STL (Standard Template Library) 是为Nova语言设计的标准模板库，提供了丰富的泛型容器、算法和函数对象。

## 版本信息

- **当前版本**: 0.12.0
- **发布日期**: 2026-03-01
- **状态**: 已发布

## 新特性（0.12.0）

### 🎉 模板结构体支持

支持使用模板结构体定义泛型数据结构，具有值类型特性。

```nova
template struct Point<T> {
    var x: T;
    var y: T;
    
    func getX(): T {
        return this.x;
    }
    
    func getY(): T {
        return this.y;
    }
}
```

**特性**:
- ✅ 值类型语义（栈上分配）
- ✅ 类型参数支持
- ✅ 类型推断
- ✅ 方法定义

### 🎉 模板函数支持

支持使用模板函数定义泛型算法。

```nova
template func add<T>(a: T, b: T): T {
    return a + b;
}

template func transform<T, U>(data: Vector<T>, fn: func(T): U): Vector<U> {
    var result = Vector<U>();
    var i = 0;
    while i < data.count() {
        result.push(fn(data.get(i)));
        i = i + 1;
    }
    return result;
}
```

**特性**:
- ✅ 单类型参数支持
- ✅ 类型推断
- ✅ 函数类型参数支持
- ✅ 高阶函数支持

### 🎉 类型推断

自动推断类型参数，简化代码编写。

```nova
// 类型推断
let p = Point(10, 20);           // 推断为 Point<int>
let s = identity("hello");         // 推断为 string
let f = identity(3.14);            // 推断为 float

// 显式指定（仍然支持）
let p2 = Point<int>(100, 200);    // 显式指定类型
```

**特性**:
- ✅ 泛型结构体实例化推断
- ✅ 泛型函数调用推断
- ✅ 多种类型支持（int, float, string等）
- ✅ 向后兼容显式指定

### 🎉 函数类型参数

支持函数作为参数，实现高阶函数。

```nova
template func apply<T, U>(value: T, transformer: func(T): U): U {
    return transformer(value);
}

func double(x: int): int {
    return x * 2;
}

let result = apply<int, int>(5, double);  // 输出: 10
```

**特性**:
- ✅ 函数类型语法：`func(T): U`
- ✅ 高阶函数调用
- ✅ 类型参数推断
- ✅ 多类型参数支持

### 🎉 Option<T> 类型

新增可选值类型，用于处理可能不存在的值。

```nova
var someValue = Option<int>.some(42);
var noneValue = Option<int>.none();

if someValue.isSome() {
    print(someValue.unwrap());  // 输出: 42
}
```

**特性**:
- ✅ Some和None两种状态
- ✅ 安全解包
- ✅ map和filter方法
- ✅ 错误处理

---

## 目录结构

```
src/nova/stdlib/stl/
├── iterator.nova          # 迭代器系统
├── functional.nova        # 函数对象和比较器
├── vector.nova           # 动态数组容器
├── list.nova             # 双向链表容器（模板结构体）
├── stack_queue.nova       # 栈和队列容器
├── set_map.nova          # 集合和映射容器
├── algorithm.nova         # 排序和查找算法
├── algorithm_template.nova  # 模板算法
├── numeric.nova          # 变换和数值算法
├── numeric_template.nova   # 模板数值算法
├── option.nova           # Option<T>类型
└── README.md            # 本文件
```

---

## 核心组件

### 1. 迭代器系统

提供了多种迭代器类型，用于遍历容器：

- `Iterator<T>`: 基础迭代器
- `RandomAccessIterator<T>`: 随机访问迭代器
- `BidirectionalIterator<T>`: 双向迭代器
- `ForwardIterator<T>`: 前向迭代器
- `InputIterator<T>`: 输入迭代器
- `OutputIterator<T>`: 输出迭代器

**使用示例**:
```nova
var vec = Vector<int>();
vec.push(10);
vec.push(20);
vec.push(30);

var it = vec.begin();
while it != vec.end() {
    print(it.value());
    it.next();
}
// 输出: 10, 20, 30
```

---

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

**使用示例**:
```nova
let result = less(10, 20);
print(result);  // 输出: true

let sum = plus(10, 20);
print(sum);  // 输出: 30
```

---

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
双向链表容器（模板结构体），支持快速插入和删除。

```nova
var list = List<int>();
list.push(1);
list.push(2);
list.push(3);
print(list.get(0));  // 输出: 1
print(list.count()); // 输出: 3
```

**主要方法：**
- `push(value)`: 添加元素到末尾
- `get(index)`: 获取指定索引的元素
- `remove(index)`: 移除指定位置的元素
- `clear()`: 清空容器
- `isEmpty()`: 判断是否为空
- `contains(value)`: 判断是否包含指定元素
- `count()`: 获取大小
- `reverse()`: 反转链表

**新特性（0.12.0）**:
- ✅ 使用模板结构体实现
- ✅ 值类型语义
- ✅ 优化的内存布局

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
- `count()`: 获取大小

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
- `isEmpty()`: 判断是否为空
- `count()`: 获取大小

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
- `count()`: 获取大小

---

### 4. 关联容器

#### Set<T>
集合容器，存储唯一元素。

```nova
var set = Set<int>();
set.add(1);
set.add(2);
set.add(1);  // 重复元素不会被添加
print(set.count());  // 输出: 2
print(set.contains(1));  // 输出: true
```

**主要方法：**
- `add(value)`: 添加元素
- `remove(value)`: 移除元素
- `contains(value)`: 判断是否包含元素
- `count()`: 获取大小
- `union(other)`: 并集
- `intersection(other)`: 交集
- `difference(other)`: 差集
- `isSubset(other)`: 判断是否为子集

#### Map<K, V>
映射容器，存储键值对。

```nova
var map = Map<string, int>();
map.set("one", 1);
map.set("two", 2);
print(map.get("one"));  // 输出: 1
print(map.containsKey("two"));  // 输出: true
```

**主要方法：**
- `set(key, value)`: 设置键值对
- `get(key)`: 获取键对应的值
- `remove(key)`: 移除键值对
- `containsKey(key)`: 判断是否包含键
- `count()`: 获取大小
- `keys()`: 获取所有键
- `values()`: 获取所有值
- `entries()`: 获取所有键值对

---

### 5. 算法库

#### 排序和查找算法

```nova
var vec = Vector<int>();
vec.push(3);
vec.push(1);
vec.push(2);

sort(vec);  // 排序
var index = find(vec, 2);  // 查找元素
var minVal = min(vec);  // 最小值
var maxVal = max(vec);  // 最大值
```

**主要算法：**
- `sort(data)`: 排序
- `reverse(data)`: 反转
- `find(data, value)`: 查找元素
- `findIf(data, predicate)`: 根据条件查找
- `binarySearch(data, value)`: 二分查找
- `count(data, value)`: 计数
- `countIf(data, predicate)`: 根据条件计数
- `min(a, b)`: 最小值
- `max(a, b)`: 最大值
- `minElement(data)`: 最小元素
- `maxElement(data)`: 最大元素
- `isSorted(data)`: 检查是否已排序

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
- `innerProduct(data1, data2)`: 内积

---

### 6. Option<T> 类型

新增的可选值类型，用于安全地处理可能不存在的值。

```nova
var someValue = Option<int>.some(42);
var noneValue = Option<int>.none();

print(someValue.isSome());  // 输出: true
print(someValue.unwrap());  // 输出: 42

print(noneValue.isSome());  // 输出: false

var mapped = someValue.map(func(x: int): int {
    return x * 2;
});
print(mapped.unwrap());  // 输出: 84
```

**主要方法：**
- `Option.some(value)`: 创建Some值
- `Option.none()`: 创建None值
- `isSome()`: 判断是否为Some
- `isNone()`: 判断是否为None
- `unwrap()`: 解包值（如果为None则报错）
- `unwrapOr(default)`: 解包值或返回默认值
- `map(fn)`: 映射值
- `filter(predicate)`: 过滤值
- `flatMap(fn)`: 平铺映射

---

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
    list.push(1);
    list.push(2);
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
    set.add(1);
    set.add(2);
    print("Set size: " + set.count());
    
    // 使用Map
    var map = Map<string, int>();
    map.set("one", 1);
    map.set("two", 2);
    print("Map get: " + map.get("one"));
    
    // 使用算法
    sort(vec);
    print("Sorted: " + vec.toArray().toString());
    
    var filtered = filter(vec, func(x: int): bool {
        return x > 1;
    });
    print("Filtered: " + filtered.toArray().toString());
    
    // 使用模板结构体
    var p = Point(10, 20);
    print("Point x: " + p.getX());
    print("Point y: " + p.getY());
    
    // 使用Option类型
    var value = Option<int>.some(42);
    if value.isSome() {
        print("Value: " + value.unwrap());
    }
}
```

---

## 设计特点

1. **完全自定义设计**: 根据Nova语言的特点设计，不直接模仿C++ STL
2. **泛型支持**: 所有容器和算法都支持泛型类型参数
3. **类型安全**: 编译时类型检查，确保类型安全
4. **易于使用**: 提供简洁直观的API
5. **高性能**: 针对Nova语言优化，提供良好的性能
6. **模板结构体**: 支持值类型的泛型数据结构
7. **模板函数**: 支持泛型算法和高阶函数
8. **类型推断**: 自动推断类型参数，简化代码编写
9. **函数类型参数**: 支持函数式编程模式

---

## 运行测试

要运行STL库的测试用例：

```bash
# 运行完整测试
python -m nova run test_stl_comprehensive.nova

# 运行特定测试
python -m nova run test_generic_struct.nova
python -m nova run test_template_functions_comprehensive.nova
python -m nova run test_type_inference.nova
python -m nova run test_stl_algorithms.nova
```

---

## 测试报告

详细的测试报告请参考：[STL_TEST_REPORT.md](../../STL_TEST_REPORT.md)

### 测试覆盖

| 功能 | 测试状态 | 测试文件 |
|------|----------|----------|
| 模板结构体 | ✅ 通过 | test_generic_struct.nova |
| 模板函数 | ✅ 通过 | test_template_functions_comprehensive.nova |
| 类型推断 | ✅ 通过 | test_type_inference.nova |
| 比较操作符 | ✅ 通过 | test_compare_bug.nova |
| Template Class多类型参数 | ✅ 通过 | test_multi_type_params.nova |
| 函数类型参数 | ✅ 通过 | test_debug_func_type.nova |
| STL容器 | ✅ 通过 | test_stl_comprehensive.nova |
| STL算法 | ✅ 通过 | test_stl_algorithms.nova |
| 数值算法 | ✅ 通过 | test_stl_algorithms.nova |
| 函数对象 | ✅ 通过 | test_stl_comprehensive.nova |
| 迭代器 | ✅ 通过 | test_stl_comprehensive.nova |
| Option类型 | ✅ 通过 | test_stl_comprehensive.nova |

---

## 文档

- **[STL_USER_GUIDE.md](../../STL_USER_GUIDE.md)** - STL库使用指南
- **[STL_TEST_REPORT.md](../../STL_TEST_REPORT.md)** - STL库测试报告
- **[TEMPLATE_GUIDE.md](../../TEMPLATE_GUIDE.md)** - 模板功能指南
- **[TEMPLATE_IMPLEMENTATION_GUIDE.md](../../TEMPLATE_IMPLEMENTATION_GUIDE.md)** - 模板实现指南
- **[GENERIC_FEATURES_TEST_REPORT.md](../../GENERIC_FEATURES_TEST_REPORT.md)** - 泛型功能测试报告

---

## 已知问题

### Template Func多类型参数

**状态**: 待修复

**问题**: `template func transform<T, U>` 解析失败

**错误信息**: `Parser error at 1:4: Expect parameter name`

**影响**: 无法实现需要多个类型参数的模板函数（如transform, map等）

**修复计划**: 修复 `parse_generic_function_definition` 方法

---

## 未来计划

1. **修复Template Func多类型参数** - 支持多类型参数的模板函数
2. **添加更多容器** - 如Deque、HashSet、HashMap
3. **实现更高效的算法** - 如快速排序、归并排序
4. **添加更多迭代器功能** - 如反向迭代器
5. **提供更多的函数对象** - 如逻辑运算、位运算
6. **优化性能和内存使用** - 减少内存分配，提高访问速度
7. **改进错误提示** - 提供更友好的错误信息

---

## 版本历史

### 0.12.0 (2026-03-01)

**新增功能**:
- ✅ 模板结构体支持
- ✅ 模板函数支持
- ✅ 类型推断
- ✅ 函数类型参数
- ✅ Option<T>类型
- ✅ 比较操作符解析修复
- ✅ Template Class多类型参数

**改进**:
- ✅ List<T>使用模板结构体实现
- ✅ 优化的内存布局
- ✅ 更好的性能

### 0.10.1 (2026-03-01)

**初始版本**:
- ✅ 基础容器（Vector, List, Stack, Queue, Set, Map）
- ✅ 基础算法（排序、查找、变换）
- ✅ 函数对象和比较器
- ✅ 迭代器系统

---

## 贡献

欢迎贡献代码、报告问题或提出建议！

### 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 报告问题

如果发现bug或有功能请求，请在GitHub上创建issue。

---

## 许可证

MIT License

---

**文档版本**: 2.0  
**最后更新**: 2026-03-01  
**作者**: AI助手（架构/STL负责人）
