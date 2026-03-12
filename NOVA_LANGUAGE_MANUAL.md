# Nova 语言说明书

**版本**: 0.16.0  
**发布日期**: 2026-03-06  
**作者**: Nova开发团队

---

## 目录

1. [简介](#1-简介)
2. [快速开始](#2-快速开始)
3. [基础语法](#3-基础语法)
4. [数据类型](#4-数据类型)
5. [变量和常量](#5-变量和常量)
6. [运算符](#6-运算符)
7. [控制流](#7-控制流)
8. [函数](#8-函数)
9. [结构体](#9-结构体)
10. [泛型编程](#10-泛型编程)
11. [Trait系统](#11-trait系统)
12. [模块系统](#12-模块系统)
13. [标准库](#13-标准库)
14. [包管理](#14-包管理)
15. [编译选项](#15-编译选项)
16. [调试和优化](#16-调试和优化)
17. [附录](#17-附录)

---

## 1. 简介

### 1.1 什么是Nova

Nova是一门现代化的静态类型编程语言，设计目标是提供：
- **简洁优雅的语法**：易于学习和使用
- **强大的类型系统**：静态类型检查，编译时捕获错误
- **高性能执行**：支持JIT编译和多种优化
- **丰富的标准库**：提供常用的数据结构和算法
- **模块化设计**：支持包管理和代码复用

### 1.2 主要特性

- **静态类型系统**：编译时类型检查，避免运行时类型错误
- **泛型编程**：支持泛型函数和泛型结构体
- **Trait系统**：类似接口的抽象机制，支持多态
- **内存管理**：自动垃圾回收，无需手动管理内存
- **并行编译**：支持多线程和GPU加速编译
- **包管理**：内置包管理系统，方便代码复用

### 1.3 Hello World

```nova
// Hello World程序
func main() {
    print("Hello, Nova!");
}
```

---

## 2. 快速开始

### 2.1 安装Nova

#### 系统要求
- Python 3.8或更高版本
- Windows 10/11、Linux或macOS

#### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/your-repo/nova.git
cd nova
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **安装Nova**
```bash
python setup.py install
```

### 2.2 运行Nova程序

```bash
# 运行程序
nova run hello.nova

# 编译程序
nova compile hello.nova

# 进入交互式环境
nova repl
```

### 2.3 第一个程序

创建文件 `hello.nova`：

```nova
// 定义主函数
func main() {
    // 声明变量
    let name = "Nova";
    let version = 0.16;
    
    // 打印输出
    print("Welcome to " + name + "!");
    print("Version: " + to_string(version));
    
    // 条件语句
    if version >= 1.0 {
        print("Stable release");
    } else {
        print("Development version");
    }
    
    // 循环语句
    for let i = 0; i < 3; i = i + 1 {
        print("Iteration: " + to_string(i));
    }
}
```

运行程序：
```bash
nova run hello.nova
```

---

## 3. 基础语法

### 3.1 注释

```nova
// 单行注释

/*
 * 多行注释
 * 可以跨越多行
 */

/// 文档注释（用于生成文档）
func documented_function() {
    // 函数实现
}
```

### 3.2 语句和表达式

```nova
// 语句以分号结束
let x = 10;

// 表达式可以嵌套
let y = (x + 5) * 2;

// 代码块
{
    let z = 20;
    print(z);
}
```

### 3.3 标识符和关键字

**标识符规则**：
- 以字母或下划线开头
- 可以包含字母、数字和下划线
- 区分大小写

**关键字**：
```
func, let, var, if, else, for, while, return,
struct, template, trait, impl, import, as,
true, false, null, unit, break, continue
```

---

## 4. 数据类型

### 4.1 基本类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `int` | 整数 | `42`, `-10`, `0` |
| `float` | 浮点数 | `3.14`, `-0.5` |
| `bool` | 布尔值 | `true`, `false` |
| `string` | 字符串 | `"Hello"` |
| `unit` | 空类型 | `()` |

### 4.2 复合类型

#### 数组
```nova
// 数组声明
let numbers: int[] = [1, 2, 3, 4, 5];
let names: string[] = ["Alice", "Bob", "Charlie"];

// 数组访问
let first = numbers[0];  // 1
let length = len(numbers);  // 5
```

#### 元组
```nova
// 元组声明
let point: (int, int) = (10, 20);
let person: (string, int) = ("Alice", 25);

// 元组解构
let (x, y) = point;
let (name, age) = person;
```

#### 字典
```nova
// 字典声明
let scores: dict<string, int> = {
    "Alice": 90,
    "Bob": 85,
    "Charlie": 95
};

// 字典访问
let alice_score = scores["Alice"];  // 90
```

### 4.3 自定义类型

#### 结构体
```nova
// 定义结构体
struct Point {
    x: int,
    y: int
}

// 创建实例
let p = Point { x: 10, y: 20 };

// 访问字段
let x_coord = p.x;
let y_coord = p.y;
```

#### 枚举（即将支持）
```nova
// 枚举定义（即将支持）
enum Color {
    Red,
    Green,
    Blue
}
```

---

## 5. 变量和常量

### 5.1 变量声明

```nova
// 不可变变量（默认）
let x = 10;
// x = 20;  // 错误：不能修改不可变变量

// 可变变量
var y = 10;
y = 20;  // 正确

// 显式类型声明
let count: int = 100;
let pi: float = 3.14159;
let message: string = "Hello";
```

### 5.2 常量

```nova
// 常量声明
const MAX_SIZE = 100;
const PI = 3.14159;
const GREETING = "Hello, Nova!";
```

### 5.3 作用域

```nova
func scope_example() {
    let outer = 10;
    
    {
        let inner = 20;
        print(outer);  // 可以访问外部变量
        print(inner);  // 可以访问内部变量
    }
    
    // print(inner);  // 错误：inner不在作用域内
    print(outer);  // 正确
}
```

---

## 6. 运算符

### 6.1 算术运算符

| 运算符 | 描述 | 示例 |
|--------|------|------|
| `+` | 加法 | `a + b` |
| `-` | 减法 | `a - b` |
| `*` | 乘法 | `a * b` |
| `/` | 除法 | `a / b` |
| `%` | 取模 | `a % b` |

### 6.2 比较运算符

| 运算符 | 描述 | 示例 |
|--------|------|------|
| `==` | 等于 | `a == b` |
| `!=` | 不等于 | `a != b` |
| `<` | 小于 | `a < b` |
| `>` | 大于 | `a > b` |
| `<=` | 小于等于 | `a <= b` |
| `>=` | 大于等于 | `a >= b` |

### 6.3 逻辑运算符

| 运算符 | 描述 | 示例 |
|--------|------|------|
| `&&` | 逻辑与 | `a && b` |
| `\|\|` | 逻辑或 | `a \|\| b` |
| `!` | 逻辑非 | `!a` |

### 6.4 赋值运算符

| 运算符 | 描述 | 示例 |
|--------|------|------|
| `=` | 赋值 | `a = b` |
| `+=` | 加后赋值 | `a += b` |
| `-=` | 减后赋值 | `a -= b` |
| `*=` | 乘后赋值 | `a *= b` |
| `/=` | 除后赋值 | `a /= b` |

### 6.5 位运算符（即将支持）

| 运算符 | 描述 | 示例 |
|--------|------|------|
| `&` | 按位与 | `a & b` |
| `\|` | 按位或 | `a \| b` |
| `^` | 按位异或 | `a ^ b` |
| `~` | 按位取反 | `~a` |
| `<<` | 左移 | `a << b` |
| `>>` | 右移 | `a >> b` |

---

## 7. 控制流

### 7.1 条件语句

#### if-else
```nova
let age = 18;

if age < 13 {
    print("Child");
} else if age < 20 {
    print("Teenager");  // 输出
} else {
    print("Adult");
}

// 三元表达式（即将支持）
// let category = if age < 18 { "Minor" } else { "Adult" };
```

#### match（即将支持）
```nova
// match表达式（即将支持）
// match value {
//     1 => print("One"),
//     2 => print("Two"),
//     _ => print("Other")
// }
```

### 7.2 循环语句

#### for循环
```nova
// 基本for循环
for let i = 0; i < 5; i = i + 1 {
    print(i);  // 0, 1, 2, 3, 4
}

// 遍历数组
let numbers = [1, 2, 3, 4, 5];
for let num in numbers {
    print(num);
}

// 带索引的遍历
for let (index, value) in enumerate(numbers) {
    print("Index: " + to_string(index) + ", Value: " + to_string(value));
}
```

#### while循环
```nova
// while循环
let count = 0;
while count < 5 {
    print(count);
    count = count + 1;
}

// do-while循环（即将支持）
// do {
//     print(count);
//     count = count + 1;
// } while count < 5;
```

#### 循环控制
```nova
// break语句
for let i = 0; i < 10; i = i + 1 {
    if i == 5 {
        break;  // 退出循环
    }
    print(i);  // 0, 1, 2, 3, 4
}

// continue语句
for let i = 0; i < 5; i = i + 1 {
    if i == 2 {
        continue;  // 跳过当前迭代
    }
    print(i);  // 0, 1, 3, 4
}
```

### 7.3 错误处理（即将支持）

```nova
// try-catch（即将支持）
// try {
//     risky_operation();
// } catch e: Error {
//     print("Error: " + e.message);
// } finally {
//     cleanup();
// }
```

---

## 8. 函数

### 8.1 函数定义

```nova
// 基本函数
func greet(name: string): string {
    return "Hello, " + name + "!";
}

// 无返回值函数
func print_message(message: string): unit {
    print(message);
}

// 多参数函数
func add(a: int, b: int): int {
    return a + b;
}

// 默认参数（即将支持）
// func greet(name: string, greeting: string = "Hello"): string {
//     return greeting + ", " + name + "!";
// }
```

### 8.2 函数调用

```nova
// 调用函数
let result = add(5, 3);  // 8
let greeting = greet("Nova");  // "Hello, Nova!"

// 嵌套调用
let sum = add(add(1, 2), add(3, 4));  // 10
```

### 8.3 递归函数

```nova
// 递归计算阶乘
func factorial(n: int): int {
    if n <= 1 {
        return 1;
    }
    return n * factorial(n - 1);
}

// 尾递归优化（编译器自动优化）
func factorial_tail(n: int, acc: int): int {
    if n <= 1 {
        return acc;
    }
    return factorial_tail(n - 1, n * acc);
}
```

### 8.4 高阶函数

```nova
// 函数作为参数
func apply_operation(a: int, b: int, op: func(int, int): int): int {
    return op(a, b);
}

// 函数作为返回值
func make_multiplier(factor: int): func(int): int {
    return func(x: int): int {
        return x * factor;
    };
}

// 使用示例
let multiply = func(a: int, b: int): int { return a * b; };
let result = apply_operation(5, 3, multiply);  // 15

let double = make_multiplier(2);
let doubled = double(5);  // 10
```

### 8.5 闭包（即将支持）

```nova
// 闭包（即将支持）
// func make_counter(): func(): int {
//     var count = 0;
//     return func(): int {
//         count = count + 1;
//         return count;
//     };
// }
```

---

## 9. 结构体

### 9.1 结构体定义

```nova
// 定义结构体
struct Point {
    x: int,
    y: int
}

struct Rectangle {
    top_left: Point,
    width: int,
    height: int
}

struct Person {
    name: string,
    age: int,
    email: string
}
```

### 9.2 结构体实例化

```nova
// 创建实例
let p1 = Point { x: 10, y: 20 };
let p2 = Point { x: 30, y: 40 };

// 嵌套结构体
let rect = Rectangle {
    top_left: Point { x: 0, y: 0 },
    width: 100,
    height: 50
};

// 结构体数组
let points: Point[] = [
    Point { x: 1, y: 2 },
    Point { x: 3, y: 4 },
    Point { x: 5, y: 6 }
];
```

### 9.3 结构体方法

```nova
// 为结构体定义方法
struct Point {
    x: int,
    y: int
}

// 实现方法
func Point.distance_from_origin(this): float {
    return sqrt(this.x * this.x + this.y * this.y);
}

func Point.translate(this, dx: int, dy: int): Point {
    return Point { x: this.x + dx, y: this.y + dy };
}

// 使用
let p = Point { x: 3, y: 4 };
let dist = p.distance_from_origin();  // 5.0
let moved = p.translate(10, 10);  // Point { x: 13, y: 14 }
```

### 9.4 结构体继承（即将支持）

```nova
// 结构体继承（即将支持）
// struct Shape {
//     color: string
// }
//
// struct Circle : Shape {
//     radius: float
// }
```

---

## 10. 泛型编程

### 10.1 泛型函数

```nova
// 定义泛型函数
template func identity<T>(value: T): T {
    return value;
}

template func swap<T>(a: T, b: T): (T, T) {
    return (b, a);
}

template func max<T>(a: T, b: T): T {
    if a > b {
        return a;
    }
    return b;
}

// 使用泛型函数
let int_val = identity<int>(42);  // 42
let str_val = identity<string>("Hello");  // "Hello"

let (x, y) = swap<int>(10, 20);  // (20, 10)
let larger = max<float>(3.14, 2.71);  // 3.14

// 类型推断
let inferred = identity(42);  // 自动推断为identity<int>
```

### 10.2 泛型结构体

```nova
// 定义泛型结构体
template struct Box<T> {
    value: T
}

template struct Pair<T, U> {
    first: T,
    second: U
}

template struct Node<T> {
    value: T,
    next: Node<T>?
}

// 使用泛型结构体
let int_box = Box<int> { value: 42 };
let str_box = Box<string> { value: "Hello" };

let pair = Pair<int, string> { first: 1, second: "One" };

let node = Node<int> {
    value: 10,
    next: Node<int> { value: 20, next: null }
};
```

### 10.3 泛型约束（即将支持）

```nova
// 泛型约束（即将支持）
// template func sum<T: Addable>(values: T[]): T {
//     var total = T.zero();
//     for let v in values {
//         total = total + v;
//     }
//     return total;
// }
```

---

## 11. Trait系统

### 11.1 定义Trait

```nova
// 定义Trait
trait Printable {
    func toString(): string;
}

trait Comparable<T> {
    func compare(other: T): int;
    func less_than(other: T): bool;
}

trait Iterable<T> {
    func iterator(): Iterator<T>;
    func has_next(): bool;
    func next(): T;
}
```

### 11.2 实现Trait

```nova
// 为类型实现Trait
struct Point {
    x: int,
    y: int
}

// 实现Printable Trait
impl Printable for Point {
    func toString(): string {
        return "(" + to_string(this.x) + ", " + to_string(this.y) + ")";
    }
}

// 实现Comparable Trait
impl Comparable<Point> for Point {
    func compare(other: Point): int {
        if this.x != other.x {
            return this.x - other.x;
        }
        return this.y - other.y;
    }
    
    func less_than(other: Point): bool {
        return this.compare(other) < 0;
    }
}

// 使用
let p = Point { x: 10, y: 20 };
print(p.toString());  // "(10, 20)"
```

### 11.3 Trait作为参数类型

```nova
// 使用Trait约束参数
func print_value(value: Printable): unit {
    print(value.toString());
}

// 泛型函数使用Trait约束
template func find_max<T: Comparable<T>>(items: T[]): T {
    var max = items[0];
    for let i = 1; i < len(items); i = i + 1 {
        if items[i].less_than(max) == false {
            max = items[i];
        }
    }
    return max;
}
```

### 11.4 标准Traits

```nova
// Display Trait - 用于格式化输出
trait Display<T> {
    func display(): string;
}

// Clone Trait - 用于复制对象
trait Clone {
    func clone(): Self;
}

// Drop Trait - 用于资源清理（即将支持）
// trait Drop {
//     func drop(): unit;
// }
```

---

## 12. 模块系统

### 12.1 导入模块

```nova
// 导入整个模块
import math;
import string;
import io;

// 使用模块中的函数
let result = math.sqrt(16);
let upper = string.to_upper("hello");

// 导入特定项（即将支持）
// import math { sqrt, pow, PI };
// let result = sqrt(16);

// 使用别名（即将支持）
// import math as m;
// let result = m.sqrt(16);
```

### 12.2 创建模块

```nova
// 文件: utils.nova
// 模块自动根据文件名命名

// 导出函数
func helper_function(): unit {
    print("Helper");
}

// 导出结构体
struct HelperStruct {
    value: int
}

// 导出常量
const HELPER_CONSTANT = 42;
```

### 12.3 模块路径

```nova
// 标准库模块
import std.collections;
import std.algorithm;
import std.numeric;

// 第三方模块（通过包管理安装）
// import external.package;

// 本地模块
// import ./local_module;
```

---

## 13. 标准库

### 13.1 核心模块 (core)

```nova
import core;

// 类型转换
let s = to_string(42);  // "42"
let n = to_int("42");   // 42
let f = to_float("3.14");  // 3.14

// 工具函数
let length = len([1, 2, 3]);  // 3
let type_name = type_of(42);  // "int"

// 数学函数
let abs_val = abs(-10);  // 10
let max_val = max(10, 20);  // 20
let min_val = min(10, 20);  // 10

// 集合操作
let sorted_list = sort([3, 1, 4, 1, 5]);  // [1, 1, 3, 4, 5]
let reversed_list = reverse([1, 2, 3]);  // [3, 2, 1]
let has_any = any([false, true, false]);  // true
let has_all = all([true, true, true]);  // true
```

### 13.2 字符串模块 (string)

```nova
import string;

// 大小写转换
let upper = string.to_upper("hello");  // "HELLO"
let lower = string.to_lower("WORLD");  // "world"
let capitalized = string.capitalize("hello world");  // "Hello world"
let title_case = string.title("hello world");  // "Hello World"
let swapped = string.swapcase("Hello");  // "hELLO"

// 空白处理
let trimmed = string.trim("  hello  ");  // "hello"
let left_trimmed = string.ltrim("  hello  ");  // "hello  "
let right_trimmed = string.rtrim("  hello  ");  // "  hello"

// 分割和连接
let parts = string.split("a,b,c", ",");  // ["a", "b", "c"]
let joined = string.join(["a", "b", "c"], "-");  // "a-b-c"

// 查找和替换
let index = string.find("hello world", "world");  // 6
let replaced = string.replace("hello world", "world", "nova");  // "hello nova"
let contains = string.contains("hello", "ell");  // true

// 检查
let is_alpha = string.isalpha("Hello");  // true
let is_digit = string.isdigit("123");  // true
let starts = string.startswith("hello", "he");  // true
let ends = string.endswith("hello", "lo");  // true

// 子串
let sub = string.substring("hello", 1, 4);  // "ell"
let reversed = string.reverse("hello");  // "olleh"
```

### 13.3 数学模块 (math)

```nova
import math;

// 常量
let pi = math.PI;  // 3.14159...
let e = math.E;    // 2.71828...

// 三角函数
let s = math.sin(math.PI / 2);  // 1.0
let c = math.cos(0);  // 1.0
let t = math.tan(math.PI / 4);  // 1.0

// 数学运算
let sq = math.sqrt(16);  // 4.0
let pw = math.pow(2, 10);  // 1024.0
let fl = math.floor(3.7);  // 3.0
let ce = math.ceil(3.2);  // 4.0
let rd = math.round(3.5);  // 4.0

// 其他函数
let ab = math.abs(-5.5);  // 5.5
let mx = math.max(10, 20);  // 20.0
let mn = math.min(10, 20);  // 10.0
```

### 13.4 IO模块 (io)

```nova
import io;

// 文件读取
let content = io.read_file("data.txt");
let lines = io.read_lines("data.txt");

// 文件写入
io.write_file("output.txt", "Hello, World!");
io.append_file("log.txt", "New log entry\n");

// 文件操作
let exists = io.file_exists("data.txt");
let size = io.file_size("data.txt");
io.delete_file("temp.txt");

// 目录操作
let files = io.list_directory("./");
io.create_directory("new_folder");
io.delete_directory("old_folder");
```

### 13.5 容器模块 (collections)

```nova
import collections;

// Vector - 动态数组
let vec = collections.Vector<int>();
vec.push_back(10);
vec.push_back(20);
let first = vec[0];  // 10
let vec_size = vec.size();  // 2

// List - 链表
let lst = collections.List<int>();
lst.push_back(10);
lst.push_front(5);

// Stack - 栈
let stack = collections.Stack<int>();
stack.push(10);
stack.push(20);
let top = stack.pop();  // 20

// Queue - 队列
let queue = collections.Queue<int>();
queue.enqueue(10);
queue.enqueue(20);
let front = queue.dequeue();  // 10

// Set - 集合
let set = collections.Set<int>();
set.insert(10);
set.insert(20);
let has = set.contains(10);  // true

// Map - 映射
let map = collections.Map<string, int>();
map.insert("one", 1);
map.insert("two", 2);
let value = map.get("one");  // 1
```

---

## 14. 包管理

### 14.1 包管理命令

```bash
# 安装包
nova package install <package_name>
nova package install <package_name> --version 1.0.0

# 卸载包
nova package uninstall <package_name>

# 更新包
nova package update <package_name>
nova package update  # 更新所有包

# 列出已安装的包
nova package list

# 查看包信息
nova package info <package_name>
```

### 14.2 包配置文件

```json
// nova.json - 包配置文件
{
    "name": "my-project",
    "version": "1.0.0",
    "description": "My Nova project",
    "author": "Your Name",
    "dependencies": {
        "http": "^1.0.0",
        "json": "^2.1.0"
    },
    "devDependencies": {
        "test": "^1.0.0"
    }
}
```

### 14.3 创建和发布包

```bash
# 初始化包
nova package init

# 构建包
nova package build

# 测试包
nova package test

# 发布包（即将支持）
# nova package publish
```

---

## 15. 编译选项

### 15.1 编译命令

```bash
# 基本编译
nova compile program.nova

# 指定输出文件
nova compile program.nova -o output

# 优化级别
nova compile program.nova -O0  # 无优化
nova compile program.nova -O1  # 部分优化
nova compile program.nova -O2  # 高度优化
nova compile program.nova -O3  # 极度优化

# 增量编译
nova compile program.nova --incremental

# 并行编译
nova compile program.nova --parallel

# GPU加速
nova compile program.nova --gpu
```

### 15.2 运行命令

```bash
# 运行程序
nova run program.nova

# 带参数运行
nova run program.nova -- arg1 arg2

# 调试模式运行
nova run program.nova --debug
```

### 15.3 交互式环境

```bash
# 启动REPL
nova repl

# 带优化级别启动
nova repl -O2
```

---

## 16. 调试和优化

### 16.1 调试工具

```nova
// 使用断点
func debug_example() {
    let x = 10;
    breakpoint();  // 进入调试器
    let y = 20;
    print(x + y);
}

// 打印调试信息
func debug_print(value: any): unit {
    print("DEBUG: " + to_string(value));
}
```

### 16.2 性能优化

#### 编译器优化
- **常量折叠**：编译时计算常量表达式
- **死代码消除**：移除不会执行的代码
- **尾递归优化**：将尾递归转换为迭代

#### 代码优化建议
```nova
// 好的做法：使用局部变量
func sum_array(arr: int[]): int {
    var total = 0;
    let n = len(arr);  // 缓存长度
    for let i = 0; i < n; i = i + 1 {
        total = total + arr[i];
    }
    return total;
}

// 避免：重复计算
// for let i = 0; i < len(arr); i = i + 1 {  // 每次循环都计算len

// 好的做法：使用合适的数据结构
// 频繁插入删除 -> 使用List
// 随机访问 -> 使用Vector
// 查找 -> 使用Set或Map
```

### 16.3 内存管理

```nova
// Nova使用自动垃圾回收
// 无需手动管理内存

// 避免内存泄漏的建议
// 1. 及时释放不再使用的大对象
// 2. 避免循环引用（即将支持弱引用）
// 3. 使用适当的作用域
```

---

## 17. 附录

### 17.1 关键字列表

| 关键字 | 说明 |
|--------|------|
| `func` | 定义函数 |
| `let` | 声明不可变变量 |
| `var` | 声明可变变量 |
| `const` | 声明常量 |
| `if` | 条件语句 |
| `else` | 条件语句分支 |
| `for` | for循环 |
| `while` | while循环 |
| `return` | 返回语句 |
| `struct` | 定义结构体 |
| `template` | 定义泛型 |
| `trait` | 定义Trait |
| `impl` | 实现Trait |
| `import` | 导入模块 |
| `as` | 别名（即将支持） |
| `true` | 布尔真 |
| `false` | 布尔假 |
| `null` | 空值 |
| `unit` | 单元类型 |
| `break` | 跳出循环 |
| `continue` | 继续下一次循环 |

### 17.2 运算符优先级

| 优先级 | 运算符 | 结合性 |
|--------|--------|--------|
| 1 | `()` `[]` `.` | 左到右 |
| 2 | `!` `-` (一元) | 右到左 |
| 3 | `*` `/` `%` | 左到右 |
| 4 | `+` `-` | 左到右 |
| 5 | `<` `>` `<=` `>=` | 左到右 |
| 6 | `==` `!=` | 左到右 |
| 7 | `&&` | 左到右 |
| 8 | `\|\|` | 左到右 |
| 9 | `=` `+=` `-=` `*=` `/=` | 右到左 |

### 17.3 内置函数

| 函数 | 说明 | 示例 |
|------|------|------|
| `print` | 打印输出 | `print("Hello")` |
| `to_string` | 转换为字符串 | `to_string(42)` |
| `to_int` | 转换为整数 | `to_int("42")` |
| `to_float` | 转换为浮点数 | `to_float("3.14")` |
| `len` | 获取长度 | `len([1, 2, 3])` |
| `type_of` | 获取类型 | `type_of(42)` |
| `breakpoint` | 设置断点 | `breakpoint()` |

### 17.4 错误代码

| 代码 | 说明 |
|------|------|
| E001 | 语法错误 |
| E002 | 未定义的标识符 |
| E003 | 类型不匹配 |
| E004 | 函数参数错误 |
| E005 | 数组越界 |
| E006 | 除零错误 |
| E007 | 空指针引用 |
| E008 | 模块未找到 |
| E009 | 导入错误 |
| E010 | 编译错误 |

### 17.5 版本历史

| 版本 | 发布日期 | 主要特性 |
|------|----------|----------|
| 0.16.0 | 2026-03-06 | LLVM JIT编译器、包管理、并行编译 |
| 0.15.1 | 2026-03-05 | Bug修复、Vector优化 |
| 0.15.0 | 2026-03-04 | 泛型Trait系统、编译器优化 |
| 0.14.0 | 2026-03-03 | 新容器类型、高级算法库 |
| 0.13.0 | 2026-03-03 | Trait约束参数语法 |
| 0.12.0 | 2026-03-01 | 模板结构体和函数 |
| 0.11.0 | 2026-03-01 | 模板结构体、类型推断 |
| 0.10.0 | 2026-03-01 | STL标准模板库 |

---

## 结语

感谢您使用Nova语言！这是一门正在积极开发中的现代化编程语言。我们期待您的反馈和建议，帮助我们不断改进和完善。

如有问题，请查阅：
- [官方文档](https://nova-lang.readthedocs.io)
- [GitHub仓库](https://github.com/your-repo/nova)
- [问题追踪](https://github.com/your-repo/nova/issues)

**Happy Coding with Nova! 🚀**
