#!/usr/bin/env python3
# 简化的 Nova IDLE 测试版本（带详细调试）

import tkinter as tk
from tkinter import scrolledtext, messagebox
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

class DebugNovaIDLE:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('调试版 Nova IDLE')
        self.root.geometry("800x600")
        
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
        self.text.tag_config('error', foreground='#800000')
        
        # 绑定事件
        self.text.bind('<Return>', self.on_return)
        
        # 显示欢迎信息
        self.show_welcome()
        
        print('[INFO] 调试版 Nova IDLE 已启动')
        print('[INFO] 请在窗口中输入 Nova 代码并按回车键')
        
        self.root.mainloop()
    
    def show_welcome(self):
        welcome = """调试版 Nova IDLE
输入 Nova 代码并按回车键执行
"""
        self.text.insert(tk.END, welcome)
        self.show_prompt()
    
    def show_prompt(self):
        self.text.insert(tk.END, '>>> ', 'prompt')
        self.text.see(tk.END)
    
    def on_return(self, event):
        print('[DEBUG] ========== Return 事件被触发 ==========')
        
        # 获取所有文本
        all_text = self.text.get(1.0, tk.END)
        print(f'[DEBUG] 所有文本: {repr(all_text)}')
        
        lines = all_text.strip().split('\n')
        print(f'[DEBUG] 行数: {len(lines)}')
        for i, line in enumerate(lines):
            print(f'[DEBUG] 行 {i}: {repr(line)}')
        
        # 找到最后一行包含 >>> 的行
        input_text = ""
        for line in reversed(lines):
            line_stripped = line.strip()
            print(f'[DEBUG] 检查行: {repr(line_stripped)}')
            
            if line_stripped.startswith(">>>"):
                # 移除提示符
                if line_stripped.startswith(">>> "):
                    input_text = line_stripped[4:].strip()
                else:
                    input_text = line_stripped[3:].strip()
                print(f'[DEBUG] 找到输入: {repr(input_text)}')
                break
        
        if not input_text:
            print('[DEBUG] 空输入，显示新提示符')
            self.show_prompt()
            return "break"
        
        # 执行 Nova 代码
        print(f'[DEBUG] 执行代码: {repr(input_text)}')
        try:
            # 词法分析
            scanner = Scanner(input_text)
            tokens = scanner.scan_tokens()
            print(f'[DEBUG] 生成 {len(tokens)} 个token')
            
            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            print('[DEBUG] AST创建成功')
            
            # 语义分析
            analyzer = SemanticAnalyzer()
            analyzed_ast = analyzer.analyze(ast)
            print('[DEBUG] 语义分析完成')
            
            # 代码生成
            codegen = CodeGenerator()
            instructions, constants = codegen.generate(analyzed_ast)
            print(f'[DEBUG] 生成 {len(instructions)} 条指令')
            
            # 执行
            vm = VirtualMachine()
            vm.load(instructions, constants)
            result = vm.run()
            print(f'[DEBUG] 执行结果: {repr(result)}')
            
            # 显示结果
            self.text.insert(tk.END, f'\n{result}\n', 'output')
            
        except Exception as e:
            import traceback
            print(f'[DEBUG] 错误: {repr(e)}')
            print(f'[DEBUG] Traceback: {traceback.format_exc()}')
            self.text.insert(tk.END, f'\n错误: {e}\n', 'error')
        
        # 显示新的提示符
        self.show_prompt()
        
        return "break"

if __name__ == '__main__':
    DebugNovaIDLE()
