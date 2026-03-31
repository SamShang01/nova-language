#!/usr/bin/env python3
# 简单的测试脚本，验证 Return 事件是否正常工作

import tkinter as tk
from tkinter import scrolledtext

class SimpleEventTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Return 事件测试')
        
        # 创建文本区域
        self.text = scrolledtext.ScrolledText(self.root, font=('Courier New', 10))
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # 绑定 Return 事件
        self.text.bind('<Return>', self.on_return)
        
        # 显示提示符
        self.show_prompt()
        
        print('[INFO] GUI 已启动，请在窗口中输入内容并按回车键')
        print('[INFO] 查看控制台输出以确认事件是否被触发')
        
        self.root.mainloop()
    
    def show_prompt(self):
        self.text.insert(tk.END, '>>> ')
        self.text.see(tk.END)
    
    def on_return(self, event):
        print('[DEBUG] Return 事件被触发！')
        
        # 获取所有文本
        all_text = self.text.get(1.0, tk.END)
        lines = all_text.strip().split('\n')
        
        # 找到最后一行包含 >>> 的行
        input_text = ""
        for line in reversed(lines):
            line = line.strip()
            if line.startswith(">>> "):
                input_text = line[4:].strip()
                print(f'[DEBUG] 输入内容: {input_text}')
                break
        
        # 显示结果
        self.text.insert(tk.END, f'\n执行结果: {input_text}\n')
        self.show_prompt()
        
        return "break"

if __name__ == '__main__':
    SimpleEventTest()
