# Nova 语言更新日志 - 版本 0.9.3

## [0.9.3] - 2026-03-01
### 新增
- **完整的面向对象编程支持**：
  - **构造函数**：支持 `init()` 方法初始化类实例
  - **静态成员**：支持 `static` 关键字定义静态字段和方法
  - **抽象类和抽象方法**：支持 `abstract` 关键字定义抽象类和抽象方法
  - **多态和方法重写**：支持子类重写父类方法，实现动态绑定
  - **访问修饰符**：支持 `private`、`protected`、`public` 访问修饰符
  - **super 关键字**：支持通过 `super` 调用父类方法
  - **属性访问器**：支持 getter 和 setter 方法
  - **运算符重载**：支持 `__add__`、`__eq__` 等特殊方法

### 示例代码

```nova
// 抽象类
abstract class Shape {
    public abstract function area(): float;
}

// 具体类实现抽象方法
class Circle extends Shape {
    public var radius: float;
    
    init(radius: float) {
        this.radius = radius;
    }
    
    public function area(): float {
        return 3.14159 * this.radius * this.radius;
    }
}

// 使用
var c = Circle(5.0);
print(c.area());  // 78.53975
```
