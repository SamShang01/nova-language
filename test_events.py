#!/usr/bin/env python3
# 测试Nova IDLE事件处理

import tkinter as tk
from tkinter import scrolledtext

class TestEvents:
    def __init__(self, root):
        self.root = root
        self.root.title('Test Events')
        
        # 创建文本区域
        self.text = scrolledtext.ScrolledText(root, font=('Courier New', 10))
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.text.bind('<Return>', self.on_return)
        self.text.bind('<Key>', self.on_key)
        
        # 显示提示符
        self.show_prompt()
    
    def show_prompt(self):
        self.text.insert(tk.END, '>>> ', 'prompt')
        self.text.mark_set('input_start', tk.INSERT)
        self.text.see(tk.END)
    
    def on_key(self, event):
        print(f'Key pressed: {event.keysym}')
        # 不要阻止Return事件
        if event.keysym == 'Return':
            return None
        return None
    
    def on_return(self, event):
        print('Return key pressed!')
        try:
            input_text = self.text.get('input_start', tk.END).strip()
            print(f'Input: {input_text}')
            self.text.insert(tk.END, f'\nYou entered: {input_text}\n')
        except Exception as e:
            print(f'Error: {e}')
        self.show_prompt()
        return 'break'

if __name__ == '__main__':
    root = tk.Tk()
    app = TestEvents(root)
    root.mainloop()
