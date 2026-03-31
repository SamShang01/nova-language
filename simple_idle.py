#!/usr/bin/env python3
# 简化的Nova IDLE测试
import tkinter as tk
from tkinter import scrolledtext
from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

class SimpleNovaIDLE:
    def __init__(self, root):
        self.root = root
        self.root.title('Nova IDLE - Test')
        
        # 创建Shell
        self.shell_text = scrolledtext.ScrolledText(root, font=('Courier New', 10))
        self.shell_text.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件（注意顺序）
        self.shell_text.bind('<Key>', self.on_key)
        self.shell_text.bind('<Return>', self.on_return)
        
        # 显示提示符
        self.show_prompt()
    
    def show_prompt(self):
        self.shell_text.insert(tk.END, '>>> ', 'prompt')
        self.shell_text.mark_set('input_start', tk.INSERT)
        self.shell_text.see(tk.END)
    
    def on_key(self, event):
        # 只处理导航键，让其他事件继续处理
        if event.keysym not in ['Left', 'Right', 'Home', 'End', 'Up', 'Down']:
            return None
    
    def on_return(self, event):
        print('Return key pressed!')
        try:
            input_text = self.shell_text.get('input_start', tk.END).strip()
            print(f'Input: {input_text}')
            
            # 提取Nova代码
            import re
            nova_code = re.sub(r'执行：.*', '', input_text).strip()
            print(f'Extracted Nova code: {nova_code}')
            
            if nova_code:
                # 执行Nova代码
                self.execute_nova_code(nova_code)
        except Exception as e:
            print(f'Error: {e}')
        self.show_prompt()
        return 'break'
    
    def execute_nova_code(self, code):
        print(f'Executing Nova code: {code}')
        try:
            # 词法分析
            scanner = Scanner(code)
            tokens = scanner.scan_tokens()
            print(f'Tokens: {len(tokens)}')
            
            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            print('AST created')
            
            # 语义分析
            analyzer = SemanticAnalyzer()
            analyzed_ast = analyzer.analyze(ast)
            print('Semantic analysis completed')
            
            # 代码生成
            codegen = CodeGenerator()
            instructions, constants = codegen.generate(analyzed_ast)
            print(f'Instructions: {len(instructions)}')
            
            # 执行
            vm = VirtualMachine()
            vm.load(instructions, constants)
            result = vm.run()
            print(f'Execution completed. Result: {result}')
            
            # 输出结果
            self.shell_text.insert(tk.END, f'\n{result}\n' if result is not None else '\n')
        except Exception as e:
            import traceback
            error_msg = f'Error: {e}\n'
            print(f'Error: {error_msg}')
            print(f'Traceback: {traceback.format_exc()}')
            self.shell_text.insert(tk.END, f'\n{error_msg}')

if __name__ == '__main__':
    root = tk.Tk()
    app = SimpleNovaIDLE(root)
    root.mainloop()
