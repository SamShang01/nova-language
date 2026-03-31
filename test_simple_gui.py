#!/usr/bin/env python3
# 简单的测试脚本，验证事件处理

import tkinter as tk
from tkinter import scrolledtext

class SimpleTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('测试')
        
        # 创建文本区域
        self.text = scrolledtext.ScrolledText(self.root, font=('Courier New', 10))
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.text.bind('<Return>', self.on_return)
        
        # 显示提示符
        self.show_prompt()
        
        self.root.mainloop()
    
    def show_prompt(self):
        self.text.insert(tk.END, '>>> ')
        self.text.see(tk.END)
    
    def on_return(self, event):
        print('[DEBUG] on_return called')
        
        # 获取所有文本
        all_text = self.text.get(1.0, tk.END)
        lines = all_text.strip().split('\n')
        
        # 找到最后一行包含 >>> 的行
        input_text = ""
        for line in reversed(lines):
            line = line.strip()
            if line.startswith(">>> "):
                input_text = line[4:].strip()
                print(f'[DEBUG] Found input: {input_text}')
                break
        
        print(f'[DEBUG] Final input: {input_text}')
        
        # 显示结果
        self.text.insert(tk.END, f'\n执行: {input_text}\n')
        self.show_prompt()
        
        return "break"

if __name__ == '__main__':
    SimpleTest()
