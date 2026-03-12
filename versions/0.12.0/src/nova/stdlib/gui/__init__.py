"""
Nova语言GUI库
提供类似Python tkinter的GUI功能
"""

import builtins

class Widget:
    """
    GUI组件基类
    """
    
    def __init__(self, title="Nova GUI", width=800, height=600):
        """
        初始化GUI窗口
        
        Args:
            title: 窗口标题
            width: 窗口宽度
            height: 窗口高度
        """
        self.title = title
        self.width = width
        self.height = height
        self.children = []
    
    def add(self, widget):
        """
        添加子组件
        
        Args:
            widget: 子组件
        """
        self.children.append(widget)
    
    def show(self):
        """
        显示窗口
        """
        print(f"显示窗口: {self.title} ({self.width}x{self.height})")
        for child in self.children:
            child.show()
    
    def mainloop(self):
        """
        启动主循环
        """
        print("启动GUI主循环...")
        print("按 Ctrl+C 退出")
        try:
            builtins.input()
        except KeyboardInterrupt:
            print("退出GUI主循环")

class Button:
    """
    按钮组件
    """
    
    def __init__(self, text, callback=None):
        """
        初始化按钮
        
        Args:
            text: 按钮文本
            callback: 点击回调函数
        """
        self.text = text
        self.callback = callback
    
    def show(self):
        """
        显示按钮
        """
        print(f"  [按钮] {self.text}")
        if self.callback:
            print(f"    回调: {self.callback.__name__}")
    
    def click(self):
        """
        模拟点击
        """
        print(f"点击按钮: {self.text}")
        if self.callback:
            self.callback()

class Label:
    """
    标签组件
    """
    
    def __init__(self, text):
        """
        初始化标签
        
        Args:
            text: 标签文本
        """
        self.text = text
    
    def show(self):
        """
        显示标签
        """
        print(f"  [标签] {self.text}")

class Entry:
    """
    输入框组件
    """
    
    def __init__(self, text=""):
        """
        初始化输入框
        
        Args:
            text: 初始文本
        """
        self.text = text
    
    def show(self):
        """
        显示输入框
        """
        print(f"  [输入框] {self.text}")
    
    def get(self):
        """
        获取输入框内容
        
        Returns:
            str: 输入框内容
        """
        return self.text
    
    def set(self, text):
        """
        设置输入框内容
        
        Args:
            text: 新文本
        """
        self.text = text

class Text:
    """
    文本框组件
    """
    
    def __init__(self, text=""):
        """
        初始化文本框
        
        Args:
            text: 初始文本
        """
        self.text = text
    
    def show(self):
        """
        显示文本框
        """
        print(f"  [文本框] {self.text}")
    
    def get(self):
        """
        获取文本框内容
        
        Returns:
            str: 文本框内容
        """
        return self.text
    
    def set(self, text):
        """
        设置文本框内容
        
        Args:
            text: 新文本
        """
        self.text = text
    
    def append(self, text):
        """
        追加文本
        
        Args:
            text: 要追加的文本
        """
        self.text += text

class Canvas:
    """
    画布组件
    """
    
    def __init__(self, width=400, height=300):
        """
        初始化画布
        
        Args:
            width: 画布宽度
            height: 画布高度
        """
        self.width = width
        self.height = height
        self.shapes = []
    
    def show(self):
        """
        显示画布
        """
        print(f"  [画布] {self.width}x{self.height}")
        for shape in self.shapes:
            print(f"    {shape}")
    
    def create_rectangle(self, x1, y1, x2, y2, fill=""):
        """
        创建矩形
        
        Args:
            x1, y1: 左上角坐标
            x2, y2: 右下角坐标
            fill: 填充颜色
        """
        shape = f"矩形: ({x1},{y1})-({x2},{y2})"
        if fill:
            shape += f" 填充:{fill}"
        self.shapes.append(shape)
    
    def create_oval(self, x1, y1, x2, y2, fill=""):
        """
        创建椭圆
        
        Args:
            x1, y1: 左上角坐标
            x2, y2: 右下角坐标
            fill: 填充颜色
        """
        shape = f"椭圆: ({x1},{y1})-({x2},{y2})"
        if fill:
            shape += f" 填充:{fill}"
        self.shapes.append(shape)
    
    def create_line(self, x1, y1, x2, y2, fill="black", width=1):
        """
        创建线条
        
        Args:
            x1, y1: 起点坐标
            x2, y2: 终点坐标
            fill: 线条颜色
            width: 线条宽度
        """
        shape = f"线条: ({x1},{y1})-({x2},{y2}) 颜色:{fill} 宽度:{width}"
        self.shapes.append(shape)
    
    def create_text(self, x, y, text, fill="black"):
        """
        创建文本
        
        Args:
            x, y: 文本坐标
            text: 文本内容
            fill: 文本颜色
        """
        shape = f"文本: ({x},{y}) '{text}' 颜色:{fill}"
        self.shapes.append(shape)

class Menu:
    """
    菜单组件
    """
    
    def __init__(self):
        """
        初始化菜单
        """
        self.items = []
    
    def add_command(self, label, callback):
        """
        添加菜单项
        
        Args:
            label: 菜单项标签
            callback: 回调函数
        """
        self.items.append({"label": label, "callback": callback})
    
    def show(self):
        """
        显示菜单
        """
        print(f"  [菜单]")
        for item in self.items:
            print(f"    {item['label']}")
