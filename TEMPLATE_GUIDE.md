# Nova语言模板功能使用指南

## 概述

Nova语言支持类似C++的模板功能，允许您定义泛型类和泛型函数。模板功能可以帮助您编写更加通用、可重用的代码。

## 基本语法

### 1. 模板类定义

使用`template class`关键字定义模板类：

```nova
template class ClassName<T> {
    var field: T;
    
    init(value: T) {
        this.field = value;
    }
    
    func getValue(): T {
        return this.field;
    }
}
```

### 2. 多类型参数

模板类支持多个类型参数：

```nova
template class Pair<T, U> {
    var first: T;
    var second: U;
    
    init(first: T, second: U) {
        this.first = first;
        this.second = second;
    }
}
```

### 3. 模板类实例化

使用尖括号`<类型>`指定具体类型：

```nova
let intContainer = Container<int>(42);
let stringContainer = Container<string>("Hello");
let pair = Pair<int, string>(1, "one");
```

## 完整示例

### 示例1: 简单容器类

```nova
template class Container<T> {
    var value: T;
    
    init(value: T) {
        this.value = value;
    }
    
    func getValue(): T {
        return this.value;
    }
    
    func setValue(newValue: T) {
        this.value = newValue;
    }
}

func main() {
    let intContainer = Container<int>(42);
    print(intContainer.getValue());  # 输出: 42
    
    let stringContainer = Container<string>("Hello Nova!");
    print(stringContainer.getValue());  # 输出: Hello Nova!
}
```

### 示例2: 键值对类

```nova
template class Pair<T, U> {
    var first: T;
    var second: U;
    
    init(first: T, second: U) {
        this.first = first;
        this.second = second;
    }
    
    func getFirst(): T {
        return this.first;
    }
    
    func getSecond(): U {
        return this.second;
    }
}

func main() {
    let pair = Pair<int, string>(1, "one");
    print(pair.getFirst());   # 输出: 1
    print(pair.getSecond());  # 输出: one
}
```

## 支持的类型

模板支持以下类型参数：

- 基本类型: `int`, `float`, `string`, `bool`
- 自定义类类型
- 其他模板类型

## 特性说明

### 当前支持的功能

1. ✅ 模板类定义 (`template class`)
2. ✅ 单类型参数 (`<T>`)
3. ✅ 多类型参数 (`<T, U, V>`)
4. ✅ 模板类实例化 (`ClassName<Type>`)
5. ✅ 构造函数 (`init`)
6. ✅ 成员方法
7. ✅ 类型参数在字段和方法中使用

### 即将支持的功能

1. 🚧 模板结构体 (`template struct`)
2. 🚧 模板函数 (`template func`)
3. 🚧 类型约束 (`where` 子句)
4. 🚧 默认类型参数

## 最佳实践

### 1. 命名约定

- 使用描述性的类型参数名称
- 单个类型参数通常命名为 `T`
- 多个类型参数可以使用 `T`, `U`, `V` 或更有意义的名称如 `Key`, `Value`

```nova
# 好的命名
template class Dictionary<Key, Value> { ... }

# 简单命名
template class Container<T> { ... }
```

### 2. 类型安全

模板提供了编译时类型检查：

```nova
let intContainer = Container<int>(42);
intContainer.setValue("string");  # 类型错误！
```

### 3. 代码重用

使用模板可以避免为不同类型重复编写相似的代码：

```nova
# 不使用模板需要为每种类型写一个类
class IntContainer { var value: int; ... }
class StringContainer { var value: string; ... }
class FloatContainer { var value: float; ... }

# 使用模板只需要一个定义
template class Container<T> { var value: T; ... }
```

## 运行示例

要运行模板示例，请使用以下命令：

```bash
python -m nova run template_examples.nova
```

## 注意事项

1. 模板类必须在实例化前定义
2. 类型参数在类定义中必须一致使用
3. 构造函数参数类型必须与实例化时的类型参数匹配

## 技术实现

模板功能的实现包括：

1. **词法分析**: 识别 `template` 关键字
2. **语法分析**: 解析模板定义和实例化
3. **语义分析**: 类型检查和类型参数绑定
4. **代码生成**: 生成具体的类型实例代码
5. **运行时**: 动态类型处理和实例化

## 更多资源

- 示例文件: `template_examples.nova`
- 测试文件: `test_template_simple.nova`
- 源代码: `src/nova/compiler/` 目录下的相关文件
