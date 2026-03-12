# Nova STL库使用指南

## 📚 目录

1. [简介](#简介)
2. [快速开始](#快速开始)
3. [容器](#容器)
   - [Vector](#vector)
   - [List](#list)
   - [Stack](#stack)
   - [Queue](#queue)
   - [Set](#set)
   - [Map](#map)
4. [算法](#算法)
5. [函数对象](#函数对象)
6. [迭代器](#迭代器)
7. [Option类型](#option类型)
8. [模板功能](#模板功能)
9. [最佳实践](#最佳实践)

---

## 简介

Nova STL（Standard Template Library）是Nova语言的标准模板库，提供了丰富的容器、算法和函数对象，帮助开发者高效地编写代码。

### 特性

- ✅ **类型安全** - 基于模板的类型系统，编译时类型检查
- ✅ **高性能** - 优化的数据结构和算法
- ✅ **易用性** - 简洁的API设计
- ✅ **泛型支持** - 支持模板结构体和模板函数
- ✅ **类型推断** - 自动推断类型参数，简化代码

### 版本

- **当前版本**: 0.12.0
- **发布日期**: 2026-03-01

---

## 快速开始

### 导入STL库

```nova
import nova.stdlib.stl.*;
```

### 使用Vector容器

```nova
var vec = Vector<int>();
vec.push(10);
vec.push(20);
vec.push(30);

print(vec.count());  // 输出: 3
print(vec.get(0));  // 输出: 10
```

### 使用算法

```nova
var vec = Vector<int>();
vec.push(3);
vec.push(1);
vec.push(4);
vec.push(1);

sort(vec);
print(isSorted(vec));  // 输出: true
```

---

## 容器

### Vector

Vector是动态数组，支持快速随机访问。

#### 创建Vector

```nova
var vec = Vector<int>();
var vec2 = Vector<string>();
```

#### 添加元素

```nova
vec.push(10);
vec.push(20);
vec.push(30);
```

#### 访问元素

```nova
let element = vec.get(0);  // 获取第一个元素
print(element);  // 输出: 10
```

#### 查找元素

```nova
let index = vec.indexOf(20);  // 查找20的索引
print(index);  // 输出: 1

let contains = vec.contains(20);  // 检查是否包含20
print(contains);  // 输出: true
```

#### 删除元素

```nova
vec.removeAt(1);  // 删除索引1的元素
print(vec.count());  // 输出: 2
```

#### 获取大小

```nova
let size = vec.count();
print(size);  // 输出: 3
```

---

### List

List是双向链表，支持快速插入和删除。

#### 创建List

```nova
var list = List<int>();
var list2 = List<string>();
```

#### 添加元素

```nova
list.push(10);
list.push(20);
list.push(30);
```

#### 访问元素

```nova
let element = list.get(0);  // 获取第一个元素
print(element);  // 输出: 10
```

#### 查找和删除

```nova
let contains = list.contains(20);  // 检查是否包含20
print(contains);  // 输出: true

list.remove(20);  // 删除20
print(list.count());  // 输出: 2
```

---

### Stack

Stack是后进先出（LIFO）的数据结构。

#### 创建Stack

```nova
var stack = Stack<int>();
```

#### 压入元素

```nova
stack.push(10);
stack.push(20);
stack.push(30);
```

#### 弹出元素

```nova
let top = stack.pop();  // 弹出栈顶元素
print(top);  // 输出: 30
```

#### 检查是否为空

```nova
let empty = stack.isEmpty();
print(empty);  // 输出: false
```

---

### Queue

Queue是先进先出（FIFO）的数据结构。

#### 创建Queue

```nova
var queue = Queue<int>();
```

#### 入队

```nova
queue.enqueue(10);
queue.enqueue(20);
queue.enqueue(30);
```

#### 出队

```nova
let front = queue.dequeue();  // 出队
print(front);  // 输出: 10
```

#### 检查是否为空

```nova
let empty = queue.isEmpty();
print(empty);  // 输出: false
```

---

### Set

Set是集合，不允许重复元素。

#### 创建Set

```nova
var set = Set<int>();
```

#### 添加元素

```nova
set.add(10);
set.add(20);
set.add(30);
set.add(20);  // 重复元素不会被添加
```

#### 检查包含

```nova
let contains = set.contains(20);
print(contains);  // 输出: true
```

#### 删除元素

```nova
set.remove(20);
print(set.count());  // 输出: 2
```

---

### Map

Map是键值对映射。

#### 创建Map

```nova
var map = Map<string, int>();
```

#### 添加键值对

```nova
map.set("one", 1);
map.set("two", 2);
map.set("three", 3);
```

#### 获取值

```nova
let value = map.get("two");
print(value);  // 输出: 2
```

#### 检查键

```nova
let contains = map.containsKey("two");
print(contains);  // 输出: true
```

#### 删除键

```nova
map.remove("two");
print(map.count());  // 输出: 2
```

---

## 算法

### 查找算法

#### find

查找元素，返回索引。

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(3);

let index = find(vec, 2);
print(index);  // 输出: 1
```

#### count

计算元素出现的次数。

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(1);

let count = count(vec, 1);
print(count);  // 输出: 2
```

### 排序算法

#### sort

对容器进行排序。

```nova
var vec = Vector<int>();
vec.push(3);
vec.push(1);
vec.push(4);
vec.push(1);

sort(vec);
print(isSorted(vec));  // 输出: true
```

#### isSorted

检查容器是否已排序。

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(3);

let sorted = isSorted(vec);
print(sorted);  // 输出: true
```

### 变换算法

#### transform

对每个元素应用函数，返回新的Vector。

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(3);

var result = transform<int, int>(vec, func(x: int): int {
    return x * 2;
});
// result: [2, 4, 6]
```

#### map

映射元素（transform的别名）。

```nova
var result = map<int, int>(vec, func(x: int): int {
    return x * x;
});
// result: [1, 4, 9]
```

#### filter

过滤元素。

```nova
var result = filter<int>(vec, func(x: int): bool {
    return x > 1;
});
// result: [2, 3]
```

#### forEach

遍历元素。

```nova
forEach<int>(vec, func(x: int) {
    print(x);
});
// 输出: 1, 2, 3
```

### 归约算法

#### reduce

归约元素。

```nova
var vec = Vector<int>();
vec.push(1);
vec.push(2);
vec.push(3);

var sum = reduce<int>(vec, 0, func(a: int, b: int): int {
    return a + b;
});
print(sum);  // 输出: 6
```

#### accumulate

累加元素。

```nova
var sum = accumulate(vec, 0);
print(sum);  // 输出: 6
```

---

## 函数对象

### 比较函数对象

#### less

小于比较。

```nova
let result = less(10, 20);
print(result);  // 输出: true
```

#### greater

大于比较。

```nova
let result = greater(20, 10);
print(result);  // 输出: true
```

### 算术函数对象

#### plus

加法。

```nova
let result = plus(10, 20);
print(result);  // 输出: 30
```

#### minus

减法。

```nova
let result = minus(20, 10);
print(result);  // 输出: 10
```

#### multiplies

乘法。

```nova
let result = multiplies(10, 20);
print(result);  // 输出: 200
```

---

## 迭代器

### 使用迭代器遍历Vector

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

### 迭代器方法

- `begin()` - 获取起始迭代器
- `end()` - 获取结束迭代器
- `value()` - 获取当前值
- `next()` - 移动到下一个
- `!=` - 迭代器比较

---

## Option类型

Option类型用于处理可能不存在的值。

### 创建Some值

```nova
var someValue = Option<int>.some(42);
print(someValue.isSome());  // 输出: true
print(someValue.unwrap());  // 输出: 42
```

### 创建None值

```nova
var noneValue = Option<int>.none();
print(noneValue.isSome());  // 输出: false
```

### 映射值

```nova
var mapped = someValue.map(func(x: int): int {
    return x * 2;
});
print(mapped.unwrap());  // 输出: 84
```

---

## 模板功能

### 模板结构体

定义模板结构体。

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

使用模板结构体（类型推断）。

```nova
let p = Point(10, 20);
print(p.getX());  // 输出: 10
```

使用模板结构体（显式指定）。

```nova
let p = Point<int>(10, 20);
print(p.getX());  // 输出: 10
```

### 模板函数

定义模板函数。

```nova
template func add<T>(a: T, b: T): T {
    return a + b;
}
```

使用模板函数（类型推断）。

```nova
let result = add(10, 20);
print(result);  // 输出: 30
```

使用模板函数（显式指定）。

```nova
let result = add<int>(10, 20);
print(result);  // 输出: 30
```

### 函数类型参数

定义接受函数作为参数的函数。

```nova
template func apply<T, U>(value: T, transformer: func(T): U): U {
    return transformer(value);
}
```

使用函数类型参数。

```nova
func double(x: int): int {
    return x * 2;
}

let result = apply<int, int>(5, double);
print(result);  // 输出: 10
```

---

## 最佳实践

### 1. 选择合适的容器

- **Vector** - 需要随机访问时使用
- **List** - 需要频繁插入和删除时使用
- **Stack** - 需要后进先出时使用
- **Queue** - 需要先进先出时使用
- **Set** - 需要唯一元素时使用
- **Map** - 需要键值映射时使用

### 2. 使用类型推断简化代码

```nova
// 推荐：使用类型推断
let vec = Vector<int>();
let p = Point(10, 20);
let result = add(10, 20);

// 不推荐：显式指定类型
let vec = Vector<int>();
let p = Point<int>(10, 20);
let result = add<int>(10, 20);
```

### 3. 使用算法而不是手动循环

```nova
// 推荐：使用算法
sort(vec);
let result = filter<int>(vec, func(x: int): bool {
    return x > 0;
});

// 不推荐：手动循环
var i = 0;
while i < vec.count() {
    if vec.get(i) > 0 {
        // ...
    }
    i = i + 1;
}
```

### 4. 使用Option类型处理可能不存在的值

```nova
// 推荐：使用Option类型
var value = map.get("key");
if value.isSome() {
    print(value.unwrap());
}

// 不推荐：使用null检查
var value = map.get("key");
if value != null {
    print(value);
}
```

### 5. 使用函数对象提高可读性

```nova
// 推荐：使用函数对象
sort(vec, less);

// 不推荐：使用lambda
sort(vec, func(a: int, b: int): bool {
    return a < b;
});
```

---

## 常见问题

### Q: 如何在Vector中存储自定义类型？

A: 使用模板Vector。

```nova
template struct Person {
    var name: string;
    var age: int;
}

var people = Vector<Person>();
people.push(Person("Alice", 30));
people.push(Person("Bob", 25));
```

### Q: 如何对自定义类型进行排序？

A: 实现比较函数。

```nova
func comparePeople(a: Person, b: Person): bool {
    return a.age < b.age;
}

sort(people, comparePeople);
```

### Q: 如何处理可能不存在的值？

A: 使用Option类型。

```nova
var value = map.get("key");
if value.isSome() {
    print(value.unwrap());
}
```

---

## 参考资料

- **VERSION_ROADMAP.md** - Nova版本规划
- **TEMPLATE_GUIDE.md** - 模板功能指南
- **TEMPLATE_IMPLEMENTATION_GUIDE.md** - 模板实现指南
- **STL_TEST_REPORT.md** - STL库测试报告

---

**文档版本**: 1.0  
**最后更新**: 2026-03-01  
**作者**: AI助手（架构/STL负责人）
