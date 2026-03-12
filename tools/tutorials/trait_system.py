"""
Nova语言特质系统交互式教程
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


def create_trait_system_tutorial() -> Tutorial:
    """
    创建特质系统教程
    
    Returns:
        Tutorial: 特质系统教程对象
    """
    tutorial = Tutorial(
        "Nova语言特质系统教程",
        "本教程将带您了解Nova语言的特质系统，包括特质定义、特质实现、特质约束等。"
    )
    
    lesson1 = Lesson(
        "什么是特质？",
        """
特质（Trait）是一种定义共享行为的方式。它类似于其他语言中的接口或协议。

特质的优势：
- 定义共享行为：多个类型可以实现相同的特质
- 多态性：通过特质实现多态
- 类型约束：限制泛型类型参数的行为
- 组合性：一个类型可以实现多个特质

在Nova中，使用trait关键字定义特质。
        """,
        [
            """
// 定义一个Display特质
trait Display {
    func display(self: Self) -> string;
}

// 定义一个Debug特质
trait Debug {
    func debug(self: Self) -> string;
}
            """
        ],
        [
            ("特质的主要优势是什么？", "定义共享行为、多态性、类型约束、组合性"),
            ("在Nova中用什么关键字定义特质？", "trait")
        ]
    )
    
    lesson2 = Lesson(
        "定义特质",
        """
特质定义了一组方法签名，实现该特质的类型必须提供这些方法的具体实现。

语法：
trait 特质名 {
    func 方法名(self: Self) -> 返回类型;
}

特质中的方法使用self: Self来表示自身类型。
        """,
        [
            """
// 定义一个Display特质
trait Display {
    func display(self: Self) -> string;
}

// 定义一个Debug特质
trait Debug {
    func debug(self: Self) -> string;
    func type_name(self: Self) -> string;
}

// 定义一个Comparable特质
trait Comparable {
    func compare(self: Self, other: Self) -> int;
}
            """
        ],
        [
            ("特质中的方法使用什么表示自身类型？", "self: Self"),
            ("特质定义的是什么？", "一组方法签名")
        ]
    )
    
    lesson3 = Lesson(
        "实现特质",
        """
使用impl关键字为特定类型实现特质。

语法：
impl 特质名 for 类型名 {
    func 方法名(self: 类型名) -> 返回类型 {
        // 方法实现
    }
}
        """,
        [
            """
// 定义特质
trait Display {
    func display(self: Self) -> string;
}

// 为int类型实现Display
impl Display for int {
    func display(self: int) -> string {
        return str(self);
    }
}

// 为string类型实现Display
impl Display for string {
    func display(self: string) -> string {
        return self;
    }
}

// 为结构体实现特质
struct Point {
    x: int;
    y: int;
}

impl Display for Point {
    func display(self: Point) -> string {
        return f"Point({self.x}, {self.y})";
    }
}

func main() {
    let x = 42;
    let s = "Hello";
    let p = Point(x: 10, y: 20);
    
    print(x.display());  // 42
    print(s.display());  // Hello
    print(p.display());  // Point(10, 20)
}
            """
        ],
        [
            ("用什么关键字为类型实现特质？", "impl"),
            ("如何为int类型实现Display特质？", "impl Display for int { ... }")
        ]
    )
    
    lesson4 = Lesson(
        "特质约束",
        """
特质约束限制泛型类型参数必须实现特定的特质。

语法：
generic func 函数名<T>(参数: T) -> 返回类型
    where T: 特质名
{
    // 函数体
}

可以指定多个特质约束：
where T: Trait1 + Trait2
        """,
        [
            """
// 定义特质
trait Display {
    func display(self: Self) -> string;
}

trait Clone {
    func clone(self: Self) -> Self;
}

// 为int实现特质
impl Display for int {
    func display(self: int) -> string {
        return str(self);
    }
}

impl Clone for int {
    func clone(self: int) -> int {
        return self;
    }
}

// 单特质约束的泛型函数
generic func print_display<T>(value: T)
    where T: Display
{
    print(value.display());
}

// 多特质约束的泛型函数
generic func clone_and_display<T>(value: T) -> T
    where T: Display + Clone
{
    let cloned = value.clone();
    print(cloned.display());
    return cloned;
}

func main() {
    let x = 42;
    print_display(x);        // 42
    clone_and_display(x);     // 42
}
            """
        ],
        [
            ("如何限制泛型类型参数必须实现某个特质？", "使用where子句：where T: TraitName"),
            ("如何指定多个特质约束？", "使用+号连接：where T: Trait1 + Trait2")
        ]
    )
    
    lesson5 = Lesson(
        "多特质实现",
        """
一个类型可以实现多个特质，这提供了比继承更灵活的代码组织方式。

示例：一个类型同时实现Display、Debug和Clone特质。
        """,
        [
            """
// 定义多个特质
trait Display {
    func display(self: Self) -> string;
}

trait Debug {
    func debug(self: Self) -> string;
}

trait Clone {
    func clone(self: Self) -> Self;
}

// 定义结构体
struct Point {
    x: int;
    y: int;
}

// 为Point实现多个特质
impl Display for Point {
    func display(self: Point) -> string {
        return f"Point({self.x}, {self.y})";
    }
}

impl Debug for Point {
    func debug(self: Point) -> string {
        return f"Point {{ x: {self.x}, y: {self.y} }}";
    }
}

impl Clone for Point {
    func clone(self: Point) -> Point {
        return Point(x: self.x, y: self.y);
    }
}

func main() {
    let p = Point(x: 10, y: 20);
    
    print(p.display());  // Point(10, 20)
    print(p.debug());   // Point { x: 10, y: 20 }
    let p2 = p.clone();
}
            """
        ],
        [
            ("一个类型可以实现多个特质吗？", "是的，可以"),
            ("多特质实现提供了什么优势？", "比继承更灵活的代码组织方式")
        ]
    )
    
    lesson6 = Lesson(
        "特质与泛型结合",
        """
特质和泛型可以结合使用，创建强大而灵活的代码。

示例：实现一个通用的容器，可以存储任何实现了Display特质的类型。
        """,
        [
            """
// 定义特质
trait Display {
    func display(self: Self) -> string;
}

// 定义泛型容器
generic struct Container<T> {
    items: [T];
    
    generic func add(self: Container<T>, item: T) -> Container<T> {
        self.items.push(item);
        return self;
    }
    
    // 只对实现了Display特质的类型提供此方法
    generic func display_all(self: Container<T>)
        where T: Display
    {
        for item in self.items {
            print(item.display());
        }
    }
}

// 为基本类型实现特质
impl Display for int {
    func display(self: int) -> string {
        return str(self);
    }
}

impl Display for string {
    func display(self: string) -> string {
        return self;
    }
}

func main() {
    let nums = Container<int>(items: []);
    nums.add(1);
    nums.add(2);
    nums.add(3);
    nums.display_all();  // 1, 2, 3
    
    let strs = Container<string>(items: []);
    strs.add("Hello");
    strs.add("World");
    strs.display_all();  // Hello, World
}
            """
        ],
        [
            ("特质和泛型可以结合使用吗？", "是的，可以"),
            ("特质约束可以应用于泛型方法吗？", "是的，可以")
        ]
    )
    
    lesson7 = Lesson(
        "实际应用：排序算法",
        """
使用特质约束实现通用的排序算法，可以排序任何实现了Comparable特质的类型。
        """,
        [
            """
// 定义Comparable特质
trait Comparable {
    func compare(self: Self, other: Self) -> int;
}

// 为int实现Comparable
impl Comparable for int {
    func compare(self: int, other: int) -> int {
        if self < other {
            return -1;
        } else if self > other {
            return 1;
        } else {
            return 0;
        }
    }
}

// 为string实现Comparable
impl Comparable for string {
    func compare(self: string, other: string) -> int {
        if self < other {
            return -1;
        } else if self > other {
            return 1;
        } else {
            return 0;
        }
    }
}

// 通用冒泡排序
generic func bubble_sort<T>(arr: [T]) -> [T]
    where T: Comparable
{
    let n = len(arr);
    let result = arr;
    
    for (let i = 0; i < n - 1; i = i + 1) {
        for (let j = 0; j < n - i - 1; j = j + 1) {
            if result[j].compare(result[j + 1]) > 0 {
                let temp = result[j];
                result[j] = result[j + 1];
                result[j + 1] = temp;
            }
        }
    }
    
    return result;
}

func main() {
    let nums = [5, 2, 8, 1, 9];
    let sorted_nums = bubble_sort(nums);  // [1, 2, 5, 8, 9]
    
    let strs = ["banana", "apple", "cherry"];
    let sorted_strs = bubble_sort(strs);  // ["apple", "banana", "cherry"]
}
            """
        ],
        [
            ("特质约束如何帮助实现通用算法？", "允许算法操作任何实现了特定特质的类型"),
            ("冒泡排序的时间复杂度是多少？", "O(n²)")
        ]
    )
    
    lesson8 = Lesson(
        "最佳实践",
        """
使用特质时的一些最佳实践：

1. 特质设计：
   - 保持特质小而专注
   - 特质应该描述"能做什么"而不是"是什么"
   - 为特质提供清晰的文档

2. 特质实现：
   - 确保实现符合特质的语义
   - 保持实现的一致性

3. 特质约束：
   - 只在需要时添加特质约束
   - 优先使用最通用的特质

4. 命名约定：
   - 特质名使用描述性名称，如Display、Debug
   - 特质方法名应该清晰表达其意图
        """,
        [
            """
// 好的特质设计
trait Display {
    func display(self: Self) -> string;
}

// 好的特质实现
impl Display for int {
    func display(self: int) -> string {
        return str(self);
    }
}

// 好的特质约束使用
generic func print_all<T>(items: [T])
    where T: Display
{
    for item in items {
        print(item.display());
    }
}
            """
        ],
        [
            ("特质应该描述什么？", "能做什么，而不是是什么"),
            ("特质应该如何设计？", "保持小而专注")
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
    tutorial = create_trait_system_tutorial()
    tutorial.start()


if __name__ == '__main__':
    main()
