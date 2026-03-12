"""
Nova语言标准库使用教程
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


def create_stdlib_tutorial() -> Tutorial:
    """
    创建标准库使用教程
    
    Returns:
        Tutorial: 标准库使用教程对象
    """
    tutorial = Tutorial(
        "Nova语言标准库使用教程",
        "本教程将带您了解Nova语言标准库的使用方法，包括核心模块、数学模块、字符串模块和IO模块。"
    )
    
    lesson1 = Lesson(
        "标准库概览",
        """
Nova标准库提供了丰富的功能，包括：

1. 核心模块 (std::core)
   - 基本数据类型
   - 常用函数
   - 集合类型

2. 数学模块 (std::math)
   - 三角函数
   - 数学运算
   - 数学常量

3. 字符串模块 (std::string)
   - 字符串操作
   - 字符串转换
   - 字符串检查

4. IO模块 (std::io)
   - 输入输出
   - 文件操作

使用标准库：
use std::module_name;
        """,
        [
            """
// 导入数学模块
use std::math;

// 导入字符串模块
use std::string;

func main() {
    let pi = PI;
    let result = sqrt(16);
    let text = "Hello";
    let upper = to_upper(text);
}
            """
        ],
        [
            ("Nova标准库包含哪些模块？", "核心模块、数学模块、字符串模块、IO模块"),
            ("如何导入标准库模块？", "use std::module_name;")
        ]
    )
    
    lesson2 = Lesson(
        "核心模块 (std::core)",
        """
核心模块提供了基本的数据类型和常用函数。

主要功能：
- 基本类型：int、float、string、bool
- 集合类型：数组、字典
- 常用函数：len、print、str
        """,
        [
            """
use std::core;

func main() {
    // 基本类型
    let x: int = 42;
    let y: float = 3.14;
    let s: string = "Hello";
    let b: bool = true;
    
    // 集合类型
    let arr: [int] = [1, 2, 3, 4, 5];
    let dict: [string: int] = {"a": 1, "b": 2};
    
    // 常用函数
    let length = len(arr);  // 5
    print("Hello, World!");
    let num_str = str(42);  // "42"
}
            """
        ],
        [
            ("核心模块提供哪些基本类型？", "int、float、string、bool"),
            ("如何获取数组的长度？", "使用len函数：len(arr)")
        ]
    )
    
    lesson3 = Lesson(
        "数学模块 (std::math) - 三角函数",
        """
数学模块提供了各种数学函数和常量。

三角函数：
- sin(x): 正弦函数
- cos(x): 余弦函数
- tan(x): 正切函数

数学常量：
- PI: 圆周率，约3.14159
- E: 自然常数，约2.71828
        """,
        [
            """
use std::math;

func main() {
    // 三角函数
    let angle = PI / 4;  // 45度
    let sin_value = sin(angle);  // 约0.707
    let cos_value = cos(angle);  // 约0.707
    let tan_value = tan(angle);  // 约1.0
    
    // 数学常量
    let pi_value = PI;  // 3.14159...
    let e_value = E;    // 2.71828...
    
    print(sin_value);
    print(cos_value);
    print(tan_value);
}
            """
        ],
        [
            ("数学模块提供哪些三角函数？", "sin、cos、tan"),
            ("PI的值大约是多少？", "3.14159")
        ]
    )
    
    lesson4 = Lesson(
        "数学模块 (std::math) - 数学运算",
        """
数学模块提供了各种数学运算函数。

运算函数：
- sqrt(x): 平方根
- pow(x, y): 幂运算
- abs(x): 绝对值
- floor(x): 向下取整
- ceil(x): 向上取整
- round(x): 四舍五入
- min(x, y): 最小值
- max(x, y): 最大值
        """,
        [
            """
use std::math;

func main() {
    // 数学运算
    let sqrt_value = sqrt(16);     // 4
    let pow_value = pow(2, 10);    // 1024
    let abs_value = abs(-5);       // 5
    
    // 取整函数
    let floor_value = floor(3.7);  // 3
    let ceil_value = ceil(3.2);    // 4
    let round_value = round(3.5);  // 4
    
    // 比较函数
    let min_value = min(10, 20);   // 10
    let max_value = max(10, 20);   // 20
    
    print(sqrt_value);
    print(pow_value);
    print(abs_value);
}
            """
        ],
        [
            ("如何计算平方根？", "使用sqrt函数：sqrt(16)"),
            ("如何计算2的10次方？", "使用pow函数：pow(2, 10)")
        ]
    )
    
    lesson5 = Lesson(
        "字符串模块 (std::string) - 基本操作",
        """
字符串模块提供了丰富的字符串操作功能。

基本操作：
- to_upper(s): 转换为大写
- to_lower(s): 转换为小写
- trim(s): 去除首尾空白
- len(s): 字符串长度
        """,
        [
            """
use std::string;

func main() {
    let text = "  Hello World  ";
    
    // 大小写转换
    let upper = to_upper(text);  // "  HELLO WORLD  "
    let lower = to_lower(text);  // "  hello world  "
    
    // 去除空白
    let trimmed = trim(text);    // "Hello World"
    
    // 字符串长度
    let length = len(text);      // 15
    
    print(upper);
    print(lower);
    print(trimmed);
    print(length);
}
            """
        ],
        [
            ("如何将字符串转换为大写？", "使用to_upper函数：to_upper(s)"),
            ("如何去除字符串首尾的空白？", "使用trim函数：trim(s)")
        ]
    )
    
    lesson6 = Lesson(
        "字符串模块 (std::string) - 高级操作",
        """
字符串模块提供了高级的字符串操作功能。

高级操作：
- split(s, delimiter): 分割字符串
- join(arr, delimiter): 连接字符串数组
- replace(s, old, new): 替换子串
- substring(s, start, end): 提取子串
        """,
        [
            """
use std::string;

func main() {
    // 分割字符串
    let text = "Hello,World,Nova";
    let parts = split(text, ",");  // ["Hello", "World", "Nova"]
    
    // 连接字符串
    let joined = join(parts, " ");  // "Hello World Nova"
    
    // 替换子串
    let replaced = replace("Hello World", "World", "Nova");  // "Hello Nova"
    
    // 提取子串
    let sub = substring("Hello World", 0, 5);  // "Hello"
    
    print(parts[0]);
    print(joined);
    print(replaced);
    print(sub);
}
            """
        ],
        [
            ("如何分割字符串？", "使用split函数：split(s, delimiter)"),
            ("如何替换字符串中的子串？", "使用replace函数：replace(s, old, new)")
        ]
    )
    
    lesson7 = Lesson(
        "字符串模块 (std::string) - 字符串检查",
        """
字符串模块提供了字符串检查功能。

检查函数：
- contains(s, substr): 是否包含子串
- starts_with(s, prefix): 是否以指定前缀开始
- ends_with(s, suffix): 是否以指定后缀结束
        """,
        [
            """
use std::string;

func main() {
    let text = "Hello World";
    
    // 检查子串
    let has_hello = contains(text, "Hello");      // true
    let has_nova = contains(text, "Nova");       // false
    
    // 检查前缀和后缀
    let starts_hello = starts_with(text, "Hello");  // true
    let ends_world = ends_with(text, "World");      // true
    let ends_nova = ends_with(text, "Nova");       // false
    
    print(has_hello);
    print(has_nova);
    print(starts_hello);
    print(ends_world);
}
            """
        ],
        [
            ("如何检查字符串是否包含某个子串？", "使用contains函数：contains(s, substr)"),
            ("如何检查字符串是否以指定前缀开始？", "使用starts_with函数：starts_with(s, prefix)")
        ]
    )
    
    lesson8 = Lesson(
        "实际应用：综合示例",
        """
让我们使用标准库实现一个实际的应用程序：计算圆的面积和周长。
        """,
        [
            """
use std::math;
use std::string;

func circle_area(radius: float) -> float {
    return PI * radius * radius;
}

func circle_circumference(radius: float) -> float {
    return 2 * PI * radius;
}

func format_result(name: string, value: float) -> string {
    let rounded = round(value * 100) / 100;
    let value_str = str(rounded);
    return name + ": " + value_str;
}

func main() {
    let radius = 5.0;
    
    let area = circle_area(radius);
    let circumference = circle_circumference(radius);
    
    let area_str = format_result("面积", area);
    let circ_str = format_result("周长", circumference);
    
    print("半径: " + str(radius));
    print(area_str);
    print(circ_str);
}
            """
        ],
        [
            ("如何计算圆的面积？", "PI * radius * radius"),
            ("如何计算圆的周长？", "2 * PI * radius")
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
    tutorial = create_stdlib_tutorial()
    tutorial.start()


if __name__ == '__main__':
    main()
