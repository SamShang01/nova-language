"""
Nova语言GUI库测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from nova.stdlib.gui import Widget, Button, Label, Entry, Text, Canvas, Menu

class TestGUI(unittest.TestCase):
    """
    GUI库测试类
    """
    
    def test_widget(self):
        """
        测试窗口组件
        """
        # 测试创建窗口
        window = Widget(title="测试窗口", width=400, height=300)
        self.assertEqual(window.title, "测试窗口")
        self.assertEqual(window.width, 400)
        self.assertEqual(window.height, 300)
        
        # 测试添加子组件
        button = Button("点击我")
        window.add(button)
        self.assertEqual(len(window.children), 1)
    
    def test_button(self):
        """
        测试按钮组件
        """
        # 测试创建按钮
        button = Button("测试按钮")
        self.assertEqual(button.text, "测试按钮")
        
        # 测试回调函数
        clicked = False
        def callback():
            nonlocal clicked
            clicked = True
        
        button_with_callback = Button("点击我", callback=callback)
        self.assertIsNotNone(button_with_callback.callback)
    
    def test_label(self):
        """
        测试标签组件
        """
        # 测试创建标签
        label = Label("测试标签")
        self.assertEqual(label.text, "测试标签")
    
    def test_entry(self):
        """
        测试输入框组件
        """
        # 测试创建输入框
        entry = Entry("默认值")
        self.assertEqual(entry.text, "默认值")
        
        # 测试获取和设置
        entry.set("新值")
        self.assertEqual(entry.get(), "新值")
    
    def test_text(self):
        """
        测试文本框组件
        """
        # 测试创建文本框
        text = Text("初始文本")
        self.assertEqual(text.text, "初始文本")
        
        # 测试获取和设置
        text.set("新文本")
        self.assertEqual(text.get(), "新文本")
        
        # 测试追加
        text.append(" 追加文本")
        self.assertEqual(text.get(), "新文本 追加文本")
    
    def test_canvas(self):
        """
        测试画布组件
        """
        # 测试创建画布
        canvas = Canvas(width=200, height=150)
        self.assertEqual(canvas.width, 200)
        self.assertEqual(canvas.height, 150)
        
        # 测试绘制图形
        canvas.create_rectangle(10, 10, 50, 50, fill="red")
        canvas.create_oval(60, 10, 100, 50, fill="blue")
        canvas.create_line(10, 60, 100, 60, fill="green", width=2)
        canvas.create_text(50, 80, "测试文本", fill="black")
        
        self.assertEqual(len(canvas.shapes), 4)
    
    def test_menu(self):
        """
        测试菜单组件
        """
        # 测试创建菜单
        menu = Menu()
        self.assertEqual(len(menu.items), 0)
        
        # 测试添加菜单项
        menu.add_command("打开", lambda: None)
        menu.add_command("保存", lambda: None)
        menu.add_command("退出", lambda: None)
        
        self.assertEqual(len(menu.items), 3)

if __name__ == '__main__':
    unittest.main()
