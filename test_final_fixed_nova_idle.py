#!/usr/bin/env python3
# 最终修复版 Nova IDLE - 修复 print 输出和 None 显示（修复换行问题）

import tkinter as tk
from tkinter import scrolledtext, messagebox
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

class FinalFixedNovaIDLE:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('最终修复版 Nova IDLE')
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
        self.text.tag_config('print_output', foreground='#008000')
        
        # 创建语义分析器（只创建一次，保持符号表状态）
        self.analyzer = SemanticAnalyzer()
        
        # 创建虚拟机（只创建一次，保持环境状态）
        self.vm = VirtualMachine()
        
        # 重写 print 函数以捕获输出
        self.print_output = []
        self._setup_print_capture()
        
        # 绑定事件
        self.text.bind('<Return>', self.on_return)
        
        # 显示欢迎信息
        self.show_welcome()
        
        print('[INFO] 最终修复版 Nova IDLE 已启动')
        print('[INFO] 请在窗口中输入 Nova 代码并按回车键')
        
        self.root.mainloop()
    
    def _setup_print_capture(self):
        """
        设置 print 函数捕获
        """
        # 保存原始的 print 函数
        self.original_print_func = self.vm.environment['print'].func
        
        # 创建自定义的 print 函数
        def custom_print(*values):
            # 调用原始 print 函数
            self.original_print_func(*values)
            # 捕获输出
            output = ' '.join(str(v) for v in values)
            self.print_output.append(output)
            return None
        
        # 替换 print 函数
        from nova.vm.machine import BuiltinFunction
        self.vm.environment['print'] = BuiltinFunction('print', custom_print)
    
    def show_welcome(self):
        welcome = """最终修复版 Nova IDLE
输入 Nova 代码并按回车键执行
"""
        self.text.insert(tk.END, welcome)
        self.show_prompt()
    
    def show_prompt(self):
        self.text.insert(tk.END, '\n>>> ', 'prompt')
        self.text.see(tk.END)
    
    def on_return(self, event):
        print('[DEBUG] Return 事件被触发')
        
        # 清空 print 输出
        self.print_output = []
        
        # 获取所有文本
        all_text = self.text.get(1.0, tk.END)
        lines = all_text.strip().split('\n')
        
        # 找到最后一行包含 >>> 的行
        input_text = ""
        for line in reversed(lines):
            line_stripped = line.strip()
            if line_stripped.startswith(">>>"):
                # 移除提示符
                if line_stripped.startswith(">>> "):
                    input_text = line_stripped[4:].strip()
                else:
                    input_text = line_stripped[3:].strip()
                print(f'[DEBUG] 输入: {repr(input_text)}')
                break
        
        if not input_text:
            print('[DEBUG] 空输入，显示新提示符')
            self.show_prompt()
            return "break"
        
        # 检查是否是 print 语句
        is_print_statement = input_text.strip().startswith('print(')
        
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
            
            # 语义分析（使用同一个分析器实例）
            analyzed_ast = self.analyzer.analyze(ast)
            print('[DEBUG] 语义分析完成')
            
            # 代码生成
            codegen = CodeGenerator()
            instructions, constants = codegen.generate(analyzed_ast)
            print(f'[DEBUG] 生成 {len(instructions)} 条指令')
            
            # 执行（使用同一个虚拟机实例）
            self.vm.load(instructions, constants)
            result = self.vm.run()
            print(f'[DEBUG] 执行结果: {repr(result)}')
            
            # 显示 print 输出
            if self.print_output:
                for output in self.print_output:
                    self.text.insert(tk.END, f'\n{output}', 'print_output')
            
            # 显示结果（如果是 print 语句且结果为 None，不显示）
            if not (is_print_statement and result is None):
                self.text.insert(tk.END, f'\n{result}', 'output')
            
        except Exception as e:
            import traceback
            print(f'[DEBUG] 错误: {repr(e)}')
            print(f'[DEBUG] Traceback: {traceback.format_exc()}')
            self.text.insert(tk.END, f'\n错误: {e}\n', 'error')
        
        # 显示新的提示符
        self.show_prompt()
        
        return "break"

if __name__ == '__main__':
    FinalFixedNovaIDLE()
