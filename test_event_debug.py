#!/usr/bin/env python3
# 检查 Nova IDLE 的事件处理

import sys
sys.path.insert(0, 'src')

import tkinter as tk
from tkinter import scrolledtext, messagebox

print("正在测试 Tkinter 事件处理...")

class EventTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("事件测试")
        self.root.geometry("600x400")
        
        # 创建文本区域
        self.text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=('Courier New', 10),
            bg='#f0f0f0',
            fg='#000000'
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # 配置标签
        self.text.tag_config('prompt', foreground='#000080')
        self.text.tag_config('output', foreground='#000000')
        
        # 绑定事件
        print("正在绑定事件...")
        self.text.bind('<Return>', self.on_return)
        self.text.bind('<Key>', self.on_key)
        print("事件绑定完成")
        
        # 显示欢迎信息
        self.show_welcome()
        
        print("测试窗口已启动")
        
        self.root.mainloop()
    
    def show_welcome(self):
        welcome = """事件测试
输入内容并按回车键
"""
        self.text.insert(tk.END, welcome)
        self.show_prompt()
    
    def show_prompt(self):
        self.text.insert(tk.END, "\n>>> ", 'prompt')
        self.text.see(tk.END)
    
    def on_return(self, event):
        print(f"[DEBUG] Return 事件被触发: {event}")
        
        try:
            # 获取所有文本
            all_text = self.text.get(1.0, tk.END)
            lines = all_text.strip().split('\n')
            
            # 找到最后一行包含 >>> 的行
            input_text = ""
            for line in reversed(lines):
                line = line.strip()
                if line.startswith(">>>"):
                    # 移除提示符
                    if line.startswith(">>> "):
                        input_text = line[4:].strip()
                    else:
                        input_text = line[3:].strip()
                    print(f"[DEBUG] 输入: {repr(input_text)}")
                    break
            
            if input_text:
                # 显示结果
                self.text.insert(tk.END, f"\n你输入了: {input_text}", 'output')
            
            # 显示新的提示符
            self.show_prompt()
            
            return "break"
        except Exception as e:
            print(f"[ERROR] 处理 Return 事件时出错: {e}")
            import traceback
            traceback.print_exc()
            return "break"
    
    def on_key(self, event):
        print(f"[DEBUG] 按键事件: {event.keysym}")
        return None

try:
    test = EventTest()
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
