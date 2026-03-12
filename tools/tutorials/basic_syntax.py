"""
Nova语言基础语法交互式教程
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
        self.lessons: List[Lesson] = []
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


def create_basic_syntax_tutorial() -> Tutorial:
    """
    创建基础语法教程
    
    Returns:
        Tutorial: 基础语法教程对象
    """
    tutorial = Tutorial(
        "Nova语言基础语法教程",
        "本教程将带您了解Nova语言的基本语法和概念，包括变量、类型、函数、控制流等。"
    )
    
    lesson1 = Lesson(
        "Hello World",
        """
让我们从经典的Hello World程序开始。在Nova语言中，使用print函数来输出文本。

Nova程序的入口是main函数。
        """,
        [
            """
func main() {
    print("Hello, World!");
}
            """
        ],
        [
            ("如何输出文本到控制台？", "使用print函数，例如：print(\"Hello, World!\");")
        ]
    )
    
    lesson2 = Lesson(
        "变量和类型",
        """
Nova语言是静态类型语言，需要在声明变量时指定类型。

基本类型包括：
- int: 整数类型
- float: 浮点数类型
- string: 字符串类型
- bool: 布尔类型（true或false）
        """,
        [
            """
func main() {
    let x: int = 42;
    let y: float = 3.14;
    let name: string = "Nova";
    let is_valid: bool = true;
    
    print(x);
    print(y);
    print(name);
    print(is_valid);
}
            """
        ],
        [
            ("如何声明一个整数变量？", "let x: int = 42;"),
            ("Nova语言有哪些基本类型？", "int、float、string、bool")
        ]
    )
    
    lesson3 = Lesson(
        "算术运算",
        """
Nova支持基本的算术运算符：
- +: 加法
- -: 减法
- *: 乘法
- /: 除法
- %: 取模（求余）
        """,
        [
            """
func main() {
    let a: int = 10;
    let b: int = 3;
    
    print(a + b);  // 13
    print(a - b);  // 7
    print(a * b);  // 30
    print(a / b);  // 3
    print(a % b);  // 1
}
            """
        ],
        [
            ("如何计算10除以3的余数？", "let result = 10 % 3;"),
            ("10 * 3的结果是什么？", "30")
        ]
    )
    
    lesson4 = Lesson(
        "条件语句",
        """
Nova使用if-else语句进行条件判断。

语法：
if (条件) {
    // 条件为真时执行
} else {
    // 条件为假时执行
}
        """,
        [
            """
func main() {
    let x: int = 10;
    
    if (x > 5) {
        print("x大于5");
    } else {
        print("x小于等于5");
    }
    
    let y: int = 3;
    if (y % 2 == 0) {
        print("y是偶数");
    } else {
        print("y是奇数");
    }
}
            """
        ],
        [
            ("如何判断一个数是否为偶数？", "if (x % 2 == 0) { ... }"),
            ("if语句的条件需要放在什么符号内？", "括号()")
        ]
    )
    
    lesson5 = Lesson(
        "循环语句",
        """
Nova支持for循环和while循环。

for循环用于遍历范围或集合：
for (let i = 0; i < 10; i = i + 1) {
    // 循环体
}

while循环在条件为真时重复执行：
while (条件) {
    // 循环体
}
        """,
        [
            """
func main() {
    // for循环
    for (let i = 0; i < 5; i = i + 1) {
        print(i);
    }
    
    // while循环
    let count: int = 0;
    while (count < 3) {
        print(count);
        count = count + 1;
    }
}
            """
        ],
        [
            ("for循环的三个部分分别是什么？", "初始化、条件、迭代"),
            ("如何使用while循环输出0到4？", "let i = 0; while (i < 5) { print(i); i = i + 1; }")
        ]
    )
    
    lesson6 = Lesson(
        "函数",
        """
函数是可重用的代码块。Nova使用func关键字定义函数。

语法：
func 函数名(参数: 类型) -> 返回类型 {
    // 函数体
    return 返回值;
}
        """,
        [
            """
func add(a: int, b: int) -> int {
    return a + b;
}

func greet(name: string) -> string {
    return "Hello, " + name + "!";
}

func main() {
    let result = add(5, 3);
    print(result);  // 8
    
    let message = greet("Nova");
    print(message);  // Hello, Nova!
}
            """
        ],
        [
            ("如何定义一个返回两个数之和的函数？", "func add(a: int, b: int) -> int { return a + b; }"),
            ("func关键字后面是什么？", "函数名")
        ]
    )
    
    lesson7 = Lesson(
        "数组",
        """
数组是存储多个相同类型元素的集合。

创建数组：
let arr: [int] = [1, 2, 3, 4, 5];

访问元素：
let first = arr[0];

添加元素：
arr.push(6);
        """,
        [
            """
func main() {
    let numbers: [int] = [1, 2, 3, 4, 5];
    
    print(numbers[0]);  // 1
    print(numbers[2]);  // 3
    
    numbers.push(6);
    print(numbers[5]);  // 6
    
    // 遍历数组
    for (let i = 0; i < len(numbers); i = i + 1) {
        print(numbers[i]);
    }
}
            """
        ],
        [
            ("如何创建一个包含三个整数的数组？", "let arr: [int] = [1, 2, 3];"),
            ("如何向数组添加元素？", "使用push方法，例如：arr.push(4);")
        ]
    )
    
    lesson8 = Lesson(
        "结构体",
        """
结构体是自定义数据类型，可以包含多个不同类型的字段。

定义结构体：
struct 结构体名 {
    字段1: 类型;
    字段2: 类型;
}

创建结构体实例：
let 实例 = 结构体名(字段1: 值1, 字段2: 值2);
        """,
        [
            """
struct Point {
    x: int;
    y: int;
}

func main() {
    let p = Point(x: 10, y: 20);
    
    print(p.x);  // 10
    print(p.y);  // 20
}
            """
        ],
        [
            ("如何定义一个包含x和y字段的结构体？", "struct Point { x: int; y: int; }"),
            ("如何访问结构体的字段？", "使用点号，例如：p.x")
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
    tutorial = create_basic_syntax_tutorial()
    tutorial.start()


if __name__ == '__main__':
    main()
