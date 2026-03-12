# Nova 0.12.0 版本说明

## 版本信息
- 版本号：0.12.0
- 发布日期：2026-03-01
- 版本类型：主要版本更新

## 新增功能

### 模板结构体（Generic Structs）
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

let intPoint = Point<int>(10, 20);
let floatPoint = Point<float>(1.5, 2.5);
```

**特性**：
- ✅ 值类型语义（栈上分配）
- ✅ 类型参数支持
- ✅ 类型推断
- ✅ 方法定义

### 模板函数（Generic Functions）
支持使用模板函数定义泛型函数。

```nova
template func identity<T>(value: T): T {
    return value;
}

let intValue = identity<int>(42);
let stringValue = identity<string>("hello");
```

**特性**：
- ✅ 类型参数支持
- ✅ 类型推断
- ✅ 多种类型实例化

### 类型推断（Type Inference）
支持自动类型推断，无需显式指定类型参数。

```nova
let point = Point(10, 20);  // 自动推断为 Point<int>
let value = identity(42);    // 自动推断为 identity<int>
```

## 使用示例

### 基本模板结构体
```nova
template struct Pair<T, U> {
    var first: T;
    var second: U;
    
    init(first: T, second: U) {
        this.first = first;
        this.second = second;
    }
}

let pair = Pair<int, string>(1, "one");
```

### 基本模板函数
```nova
template func max<T>(a: T, b: T): T {
    if a > b {
        return a;
    } else {
        return b;
    }
}

let maxValue = max<int>(10, 20);
```

## 技术实现

模板功能的实现涉及编译器的多个组件：

1. **词法分析器**：添加 `TEMPLATE` 关键字识别
2. **语法分析器**：解析模板结构体和模板函数定义
3. **抽象语法树**：添加 `GenericStructDefinition` 和 `GenericFunctionDefinition` 节点
4. **语义分析器**：处理泛型类型参数的声明和绑定
5. **代码生成器**：生成泛型结构体和函数的实例化代码
6. **虚拟机**：支持泛型结构体和函数的运行时实例化

## 兼容性

- 完全向后兼容之前的版本
- 模板功能是可选的，不影响现有代码
- 可以在同一个项目中混合使用模板和普通代码

## 已知限制

- 暂不支持trait约束（计划在0.13.0实现）
- 暂不支持默认类型参数（计划在0.14.0实现）
- 暂不支持模板方法（计划在0.15.0实现）

## 测试文件

- `test_generic_struct.nova` - 模板结构体测试
- `test_generic_function.nova` - 模板函数测试
- `test_type_inference.nova` - 类型推断测试

## 升级指南

从0.11.x版本升级到0.12.0：

1. 无需修改现有代码
2. 可以开始使用新的模板功能
3. 参考示例文件学习模板语法

## 反馈

如有问题或建议，请通过以下方式反馈：
- 提交Issue到项目仓库
- 参与项目讨论

---

**Nova 0.12.0 - 让泛型编程更强大！**
