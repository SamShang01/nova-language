"""
Nova语言泛型编程交互式教程
"""

from typing import List, Dict, Tuple


class Tutorial:
    """
    教程基类
    """
    
    def __init__(self, title: str, description: str):
        """
        初始化教程
        
        Args:
            title: 教程标题
            description: 教程描述
        """
        self.title = title
        self.description = description
        self.lessons: List['Lesson'] = []
        self.current_lesson = 0
    
    def add_lesson(self, lesson: 'Lesson'):
        """
        添加课程
        
        Args:
            lesson: 课程对象
        """
        self.lessons.append(lesson)
    
    def start(self):
        """
        开始教程
        """
        print(f"\n{'=' * 60}")
        print(f"{self.title}")
        print(f"{'=' * 60}")
        print(f"\n{self.description}\n")
        print(f"按 Enter 开始...")
        input()
        
        for i, lesson in enumerate(self.lessons):
            self.current_lesson = i
            lesson.run()
            
            if i < len(self.lessons) - 1:
                print(f"\n按 Enter 继续下一课...")
                input()
        
        print(f"\n{'=' * 60}")
        print(f"恭喜！您已完成 {self.title}")
        print(f"{'=' * 60}\n")


class Lesson:
    """
    课程类
    """
    
    def __init__(self, title: str, content: str, examples: List[str], exercises: List[Tuple[str, str]]):
        """
        初始化课程
        
        Args:
            title: 课程标题
            content: 课程内容
            examples: 示例代码列表
            exercises: 练习题列表，格式为 (题目, 答案)
        """
        self.title = title
        self.content = content
        self.examples = examples
        self.exercises = exercises
    
    def run(self):
        """
        运行课程
        """
        print(f"\n{'=' * 60}")
        print(f"课程: {self.title}")
        print(f"{'=' * 60}\n")
        
        print(self.content)
        
        if self.examples:
            print(f"\n示例代码:")
            for i, example in enumerate(self.examples, 1):
                print(f"\n示例 {i}:")
                print(example)
        
        if self.exercises:
            self._run_exercises()
    
    def _run_exercises(self):
        """
        运行练习
        """
        print(f"\n{'=' * 60}")
        print(f"练习题")
        print(f"{'=' * 60}\n")
        
        for i, (question, answer) in enumerate(self.exercises, 1):
            print(f"练习 {i}: {question}")
            print(f"答案: {answer}\n")


def create_generic_programming_tutorial() -> Tutorial:
    """
    创建泛型编程教程
    
    Returns:
        Tutorial: 泛型编程教程对象
    """
    tutorial = Tutorial(
        "Nova语言泛型编程教程",
        "本教程将带您了解Nova语言的泛型编程特性，包括泛型函数、泛型结构体、类型约束等。"
    )
    
    lesson1 = Lesson(
        "什么是泛型？",
        """
泛型是一种编程技术，允许您编写可以处理多种类型的代码，而不需要为每种类型编写重复的代码。

泛型的优势：
- 代码重用：一次编写，多种类型使用
- 类型安全：编译时类型检查
- 灵活性：适应不同的数据类型

在Nova中，使用generic关键字定义泛型。
        """,
        [
            """
// 非泛型版本 - 只能处理整数
func add_int(a: int, b: int) -> int {
    return a + b;
}

// 泛型版本 - 可以处理任何支持+运算的类型
generic func add<T>(a: T, b: T) -> T {
    return a + b;
}
            """
        ],
        [
            ("泛型的主要优势是什么？", "代码重用、类型安全、灵活性"),
            ("在Nova中用什么关键字定义泛型？", "generic")
        ]
    )
    
    lesson2 = Lesson(
        "泛型函数",
        """
泛型函数使用类型参数来表示可以接受多种类型的参数。

语法：
generic func 函数名<T>(参数: T) -> T {
    // 函数体
}

类型参数放在尖括号<>中，通常使用大写字母如T、U、V等。
        """,
        [
            """
// 简单的泛型函数
generic func identity<T>(value: T) -> T {
    return value;
}

// 交换两个值
generic func swap<T>(a: T, b: T) -> (T, T) {
    return (b, a);
}

// 获取第一个元素
generic func first<T>(items: [T]) -> T {
    return items[0];
}

func main() {
    let x = identity(42);        // int类型
    let y = identity("hello");  // string类型
    
    let (a, b) = swap(1, 2);    // 交换整数
    let (c, d) = swap("a", "b"); // 交换字符串
    
    let nums = [1, 2, 3];
    let f = first(nums);        // 1
}
            """
        ],
        [
            ("如何定义一个返回其参数的泛型函数？", "generic func identity<T>(value: T) -> T { return value; }"),
            ("类型参数放在什么符号中？", "尖括号<>")
        ]
    )
    
    lesson3 = Lesson(
        "多类型参数",
        """
泛型函数可以接受多个类型参数。

语法：
generic func 函数名<T, U>(参数1: T, 参数2: U) -> U {
    // 函数体
}
        """,
        [
            """
// 创建一个包含两种类型值的元组
generic func pair<T, U>(first: T, second: U) -> (T, U) {
    return (first, second);
}

// 将一种类型转换为另一种类型
generic func transform<T, U>(value: T, f: func(T) -> U) -> U {
    return f(value);
}

func main() {
    let p1 = pair(1, "hello");           // (int, string)
    let p2 = pair("world", 3.14);        // (string, float)
    
    // 使用transform函数
    let result = transform(5, func(x: int) -> string {
        return str(x);
    });  // "5"
}
            """
        ],
        [
            ("如何定义一个接受两种类型参数的泛型函数？", "generic func func_name<T, U>(a: T, b: U) -> ..."),
            ("多个类型参数之间用什么分隔？", "逗号")
        ]
    )
    
    lesson4 = Lesson(
        "泛型结构体",
        """
泛型结构体允许您创建可以存储多种类型数据的结构体。

语法：
generic struct 结构体名<T> {
    字段1: T;
    字段2: T;
}

创建实例：
let 实例 = 结构体名<类型>(字段1: 值1, 字段2: 值2);
        """,
        [
            """
// 简单的泛型结构体
generic struct Box<T> {
    value: T;
    
    generic func get(self: Box<T>) -> T {
        return self.value;
    }
}

// 多类型参数的结构体
generic struct Pair<T, U> {
    first: T;
    second: U;
}

// 泛型栈
generic struct Stack<T> {
    items: [T];
    
    generic func push(self: Stack<T>, item: T) -> Stack<T> {
        self.items.push(item);
        return self;
    }
    
    generic func pop(self: Stack<T>) -> T {
        return self.items.pop();
    }
}

func main() {
    let box_int = Box<int>(value: 42);
    let box_str = Box<string>(value: "hello");
    
    let pair = Pair<int, string>(first: 1, second: "hello");
    
    let stack = Stack<int>(items: []);
    stack.push(1);
    stack.push(2);
    let value = stack.pop();  // 2
}
            """
        ],
        [
            ("如何定义一个泛型结构体？", "generic struct StructName<T> { ... }"),
            ("如何创建泛型结构体的实例？", "let instance = StructName<Type>(field: value);")
        ]
    )
    
    lesson5 = Lesson(
        "类型约束（Where子句）",
        """
类型约束限制泛型类型参数必须满足某些条件，例如实现特定的特质。

语法：
generic func 函数名<T>(参数: T) -> T
    where T: 特质名
{
    // 函数体
}

可以指定多个特质约束：
where T: Trait1 + Trait2
        """,
        [
            """
// 定义一个特质
trait Display {
    func display(self: Self) -> string;
}

// 为基本类型实现特质
impl Display for int {
    func display(self: int) -> string {
        return str(self);
    }
}

// 使用类型约束的泛型函数
generic func print_value<T>(value: T)
    where T: Display
{
    print(value.display());
}

// 多特质约束
trait Clone {
    func clone(self: Self) -> Self;
}

generic func clone_and_display<T>(value: T) -> T
    where T: Display + Clone
{
    let cloned = value.clone();
    print(cloned.display());
    return cloned;
}

func main() {
    let x = 42;
    print_value(x);  // 可以，因为int实现了Display
}
            """
        ],
        [
            ("如何限制泛型类型参数必须实现某个特质？", "使用where子句：where T: TraitName"),
            ("如何指定多个特质约束？", "使用+号连接：where T: Trait1 + Trait2")
        ]
    )
    
    lesson6 = Lesson(
        "泛型方法",
        """
泛型结构体的方法也可以是泛型的。

语法：
generic struct Struct<T> {
    generic func method<U>(self: Struct<T>, param: U) -> U {
        // 方法体
    }
}
        """,
        [
            """
generic struct Container<T> {
    items: [T];
    
    // 添加元素
    generic func add(self: Container<T>, item: T) -> Container<T> {
        self.items.push(item);
        return self;
    }
    
    // 转换容器中的元素
    generic func map<U>(self: Container<T>, f: func(T) -> U) -> Container<U> {
        let result = [];
        for item in self.items {
            result.push(f(item));
        }
        return Container<U>(items: result);
    }
    
    // 过滤元素
    generic func filter(self: Container<T>, f: func(T) -> bool) -> Container<T> {
        let result = [];
        for item in self.items {
            if f(item) {
                result.push(item);
            }
        }
        return Container<T>(items: result);
    }
}

func main() {
    let nums = Container<int>(items: [1, 2, 3, 4, 5]);
    
    // 过滤偶数
    let evens = nums.filter(func(x: int) -> bool {
        return x % 2 == 0;
    });
    
    // 映射为字符串
    let strs = nums.map(func(x: int) -> string {
        return str(x);
    });
}
            """
        ],
        [
            ("泛型结构体的方法可以是泛型的吗？", "是的，可以"),
            ("如何定义泛型方法？", "generic func method_name<U>(...) -> ...")
        ]
    )
    
    lesson7 = Lesson(
        "实际应用：通用数据结构",
        """
泛型非常适合实现通用的数据结构，如链表、树、图等。

让我们实现一个简单的链表：
        """,
        [
            """
generic struct Node<T> {
    value: T;
    next: Node<T>;
}

generic struct LinkedList<T> {
    head: Node<T>;
    
    generic func append(self: LinkedList<T>, value: T) -> LinkedList<T> {
        let new_node = Node<T>(value: value, next: null);
        if self.head == null {
            self.head = new_node;
        } else {
            let current = self.head;
            while current.next != null {
                current = current.next;
            }
            current.next = new_node;
        }
        return self;
    }
    
    generic func to_array(self: LinkedList<T>) -> [T] {
        let result = [];
        let current = self.head;
        while current != null {
            result.push(current.value);
            current = current.next;
        }
        return result;
    }
}

func main() {
    let list = LinkedList<int>(head: null);
    list.append(1);
    list.append(2);
    list.append(3);
    
    let arr = list.to_array();  // [1, 2, 3]
}
            """
        ],
        [
            ("泛型适合实现什么类型的数据结构？", "通用数据结构，如链表、树、图等"),
            ("链表的基本组成是什么？", "节点（Node），每个节点包含值和指向下一个节点的指针")
        ]
    )
    
    lesson8 = Lesson(
        "最佳实践",
        """
使用泛型时的一些最佳实践：

1. 类型参数命名：
   - 使用单个大写字母：T、U、V
   - 使用描述性名称：TKey、TValue、TElement

2. 类型约束：
   - 只在需要时添加类型约束
   - 优先使用特质而不是具体类型

3. 文档：
   - 为泛型函数和结构体添加文档
   - 说明类型参数的用途和约束

4. 性能考虑：
   - 泛型在编译时会为每种类型生成代码
   - 避免过度使用泛型导致代码膨胀
        """,
        [
            """
// 好的命名
generic func map<T, U>(items: [T], f: func(T) -> U) -> [U] {
    let result = [];
    for item in items {
        result.push(f(item));
    }
    return result;
}

// 好的类型约束使用
generic func find<T>(items: [T], predicate: func(T) -> bool) -> T
    where T: Comparable
{
    for item in items {
        if predicate(item) {
            return item;
        }
    }
    return null;
}
            """
        ],
        [
            ("类型参数命名通常使用什么？", "单个大写字母，如T、U、V"),
            ("泛型在什么时候生成代码？", "编译时")
        ]
    )
    
    tutorial.add_lesson(lesson1)
    tutorial.add_lesson(lesson2)
    tutorial.add_lesson(lesson3)
    tutorial.add_lesson(lesson4)
    tutorial.add_lesson(lesson5)
    tutorial.add_lesson(lesson6)
    tutorial.add_lesson(lesson7)
    tutorial.add_lesson(lesson8)
    
    return tutorial


def main():
    """
    主函数
    """
    tutorial = create_generic_programming_tutorial()
    tutorial.start()


if __name__ == '__main__':
    main()
