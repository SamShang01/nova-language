# Nova 语言 0.9.3

## 版本说明

Nova 语言 0.9.3 版本引入了完整的面向对象编程支持，包括类、继承、多态、抽象类等特性。

## 主要特性

### 1. 类和对象
- 使用 `class` 关键字定义类
- 支持 `public`、`private`、`protected` 访问修饰符
- 支持 `this` 关键字访问当前实例

### 2. 构造函数
- 使用 `init()` 方法定义构造函数
- 支持在构造函数中初始化字段

### 3. 继承
- 使用 `extends` 关键字实现继承
- 支持单继承
- 子类可以访问父类的字段和方法

### 4. 多态
- 支持方法重写（override）
- 运行时动态绑定

### 5. 抽象类
- 使用 `abstract` 关键字定义抽象类
- 抽象类不能被实例化
- 抽象方法必须在子类中实现

### 6. 静态成员
- 使用 `static` 关键字定义静态字段和方法
- 静态成员属于类，不属于实例

### 7. super 关键字
- 使用 `super` 调用父类的方法
- 可以在重写的方法中调用父类版本

### 8. 运算符重载
- 支持 `__add__`、`__eq__` 等特殊方法
- 可以自定义类的运算符行为

## 示例代码

```nova
// 定义抽象类
abstract class Shape {
    public abstract function area(): float;
    public abstract function perimeter(): float;
}

// 实现具体类
class Rectangle extends Shape {
    private var width: float;
    private var height: float;
    
    init(width: float, height: float) {
        this.width = width;
        this.height = height;
    }
    
    public function area(): float {
        return this.width * this.height;
    }
    
    public function perimeter(): float {
        return 2 * (this.width + this.height);
    }
}

// 使用
var rect = Rectangle(5.0, 3.0);
print(rect.area());       // 15.0
print(rect.perimeter());  // 16.0
```

## 安装

```bash
python script.py install --version==0.9.3
```
