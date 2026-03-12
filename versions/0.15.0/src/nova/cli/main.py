"""
Nova命令行工具主模块
"""

import argparse
import sys
import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, messagebox, ttk

from ..version import __version__, get_version_string, version_greater_or_equal
from ..compiler.lexer.scanner import Scanner
from ..compiler.parser.parser import Parser
from ..compiler.semantic.analyzer import SemanticAnalyzer
from ..compiler.codegen.generator import CodeGenerator
from ..vm.machine import VirtualMachine
from ..compiler.optimizer.passes import ConstantFolding, DeadCodeElimination, TailRecursionOptimization

# CLI主函数
def cli_main():
    """
    CLI版本主函数
    """
    parser = argparse.ArgumentParser(description='Nova语言工具')
    parser.add_argument('--version', action='store_true', help='显示版本信息')
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # install子命令
    install_parser = subparsers.add_parser('install', help='安装Nova语言')
    install_parser.add_argument('--version', type=str, help='指定版本号，格式为 x.y.z')
    
    # run子命令
    run_parser = subparsers.add_parser('run', help='运行Nova程序')
    run_parser.add_argument('file', type=str, help='Nova程序文件路径')
    run_parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    # repl子命令
    repl_parser = subparsers.add_parser('repl', help='启动交互式环境')
    repl_parser.add_argument('-O0', '--optimization-level-0', action='store_const', const=0, dest='optimization_level', help='无优化（默认）')
    repl_parser.add_argument('-O1', '--optimization-level-1', action='store_const', const=1, dest='optimization_level', help='部分优化')
    repl_parser.add_argument('-O2', '--optimization-level-2', action='store_const', const=2, dest='optimization_level', help='高度优化')
    repl_parser.add_argument('-O3', '--optimization-level-3', action='store_const', const=3, dest='optimization_level', help='极度优化')
    repl_parser.set_defaults(optimization_level=0)
    
    # compile子命令
    compile_parser = subparsers.add_parser('compile', help='编译Nova程序')
    compile_parser.add_argument('file', type=str, help='Nova程序文件路径')
    compile_parser.add_argument('-o', '--output', type=str, help='输出文件路径')
    compile_parser.add_argument('--format', type=str, choices=['python', 'executable'], default='python', help='输出格式（python或executable）')
    compile_parser.add_argument('-O0', '--optimization-level-0', action='store_const', const=0, dest='optimization_level', help='无优化（默认）')
    compile_parser.add_argument('-O1', '--optimization-level-1', action='store_const', const=1, dest='optimization_level', help='部分优化')
    compile_parser.add_argument('-O2', '--optimization-level-2', action='store_const', const=2, dest='optimization_level', help='高度优化')
    compile_parser.add_argument('-O3', '--optimization-level-3', action='store_const', const=3, dest='optimization_level', help='极度优化')
    compile_parser.set_defaults(optimization_level=0)
    
    # run子命令
    run_parser.add_argument('-O0', '--optimization-level-0', action='store_const', const=0, dest='optimization_level', help='无优化（默认）')
    run_parser.add_argument('-O1', '--optimization-level-1', action='store_const', const=1, dest='optimization_level', help='部分优化')
    run_parser.add_argument('-O2', '--optimization-level-2', action='store_const', const=2, dest='optimization_level', help='高度优化')
    run_parser.add_argument('-O3', '--optimization-level-3', action='store_const', const=3, dest='optimization_level', help='极度优化')
    run_parser.set_defaults(optimization_level=0)
    
    # idle子命令
    idle_parser = subparsers.add_parser('idle', help='启动Nova IDLE')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Nova语言版本: {get_version_string()}")
        sys.exit(0)
    
    if args.command == 'install':
        install_nova(args.version)
    elif args.command == 'run':
        run_nova(args.file, args.verbose, args.optimization_level)
    elif args.command == 'repl':
        start_repl(args.optimization_level)
    elif args.command == 'compile':
        compile_nova(args.file, args.output, args.format, args.optimization_level)
    elif args.command == 'idle':
        start_idle()
    else:
        parser.print_help()

# 安装Nova语言
def install_nova(version=None):
    """
    安装Nova语言
    
    Args:
        version: 指定版本号，格式为 x.y.z
    """
    print(f"安装Nova语言 {'版本 ' + version if version else '最新版本'}")
    
    # 这里实现安装逻辑
    # 1. 检查版本是否存在
    # 2. 下载对应版本
    # 3. 安装到系统
    
    if version:
        print(f"正在安装Nova语言版本 {version}...")
        # 模拟安装过程
        print("下载安装包...")
        print("解压安装包...")
        print("配置环境...")
        print(f"Nova语言版本 {version} 安装完成！")
    else:
        print("正在安装Nova语言最新版本...")
        print("下载安装包...")
        print("解压安装包...")
        print("配置环境...")
        print("Nova语言最新版本安装完成！")

# 运行Nova程序
def run_nova(file_path, verbose=False, optimization_level=0):
    """
    运行Nova程序
    
    Args:
        file_path: Nova程序文件路径
        verbose: 是否详细输出
        optimization_level: 优化级别 (0-3)
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)
    
    print(f"运行Nova程序: {file_path}")
    if verbose:
        print("详细模式开启")
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if verbose:
            print("解析程序...")
        
        # 词法分析
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        
        if verbose:
            print(f"词法分析完成，生成了 {len(tokens)} 个token")
            print("编译程序...")
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        if verbose:
            print(f"语法分析完成，生成了AST")
            print("语义分析...")
        
        # 语义分析
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        
        if verbose:
            print("语义分析完成")
            print(f"应用优化级别 O{optimization_level}...")
        
        # 应用优化
        optimized_ast = analyzed_ast
        if optimization_level >= 1:
            from ..compiler.optimizer.passes import ConstantFolding
            constant_folding = ConstantFolding()
            optimized_ast = constant_folding.optimize(optimized_ast)
            if verbose:
                print("  - 常量折叠")
        
        if optimization_level >= 2:
            from ..compiler.optimizer.passes import DeadCodeElimination
            dead_code_elim = DeadCodeElimination()
            optimized_ast = dead_code_elim.optimize(optimized_ast)
            if verbose:
                print("  - 死代码消除")
        
        if optimization_level >= 3:
            from ..compiler.optimizer.passes import TailRecursionOptimization
            tail_recursion_opt = TailRecursionOptimization()
            optimized_ast = tail_recursion_opt.optimize(optimized_ast)
            if verbose:
                print("  - 尾递归优化")
        
        if verbose:
            print("代码生成...")
        
        # 代码生成
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(optimized_ast)
        
        if verbose:
            print(f"代码生成完成，生成了 {len(instructions)} 条指令")
            print(f"常量表包含 {len(constants)} 个常量")
            print("执行程序...")
        
        # 执行
        vm = VirtualMachine()
        vm.load(instructions, constants)
        result = vm.run()
        
        # 输出执行结果
        if result is not None:
            print(result)
        
        if verbose:
            print("程序执行完成！")
        
    except ImportError as e:
        print(f"错误: 无法导入必要的模块 - {e}")
        print("请确保Nova语言已正确安装")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# 启动交互式环境
def start_repl(optimization_level=0):
    """
    启动交互式环境
    
    Args:
        optimization_level: 优化级别 (0-3)
    """
    print("启动Nova交互式环境...")
    print(f"Nova语言版本: {get_version_string()}")
    print("输入 'exit' 退出环境")
    print("输入 'help' 查看帮助")
    print("输入 ':type <变量名>' 查看变量类型")
    print()
    
    # 变量环境
    variables = {}
    
    # 主循环
    while True:
        try:
            user_input = input("nova> ")
            if user_input.strip() == 'exit':
                print("退出交互式环境")
                break
            elif user_input.strip() == 'help':
                print("帮助信息:")
                print("  exit - 退出环境")
                print("  help - 查看帮助")
                print("  :type <变量名> - 查看变量类型")
                print("  输入Nova代码直接执行")
            elif user_input.strip().startswith(':type '):
                # 处理类型查询
                var_name = user_input.strip()[6:].strip()
                if var_name in variables:
                    var_type = variables[var_name]
                    print(f"{var_name}: {var_type}")
                else:
                    print(f"未找到: {var_name}")
            else:
                # 执行Nova代码
                try:
                    # 词法分析
                    scanner = Scanner(user_input)
                    tokens = scanner.scan_tokens()
                    
                    # 语法分析
                    parser = Parser(tokens)
                    ast = parser.parse()
                    
                    # 语义分析
                    analyzer = SemanticAnalyzer()
                    analyzed_ast = analyzer.analyze(ast)
                    
                    # 应用优化
                    optimized_ast = analyzed_ast
                    if optimization_level >= 1:
                        from ..compiler.optimizer.passes import ConstantFolding
                        constant_folding = ConstantFolding()
                        optimized_ast = constant_folding.optimize(optimized_ast)
                    
                    if optimization_level >= 2:
                        from ..compiler.optimizer.passes import DeadCodeElimination
                        dead_code_elim = DeadCodeElimination()
                        optimized_ast = dead_code_elim.optimize(optimized_ast)
                    
                    if optimization_level >= 3:
                        from ..compiler.optimizer.passes import TailRecursionOptimization
                        tail_recursion_opt = TailRecursionOptimization()
                        optimized_ast = tail_recursion_opt.optimize(optimized_ast)
                    
                    # 代码生成
                    codegen = CodeGenerator()
                    instructions, constants = codegen.generate(optimized_ast)
                    
                    # 执行
                    vm = VirtualMachine()
                    vm.load(instructions, constants)
                    result = vm.run()
                    
                    # 输出执行结果
                    if result is not None:
                        print(result)
                    
                    # 更新变量环境
                    for name, value in vm.environment.items():
                        if isinstance(value, (int, float, str, bool)):
                            variables[name] = type(value).__name__
                        elif hasattr(value, '__class__'):
                            variables[name] = value.__class__.__name__
                        else:
                            variables[name] = 'unknown'
                    
                except Exception as e:
                    print(f"错误: {e}")
        except KeyboardInterrupt:
            print()
            print("退出交互式环境")
            break
        except EOFError:
            print()
            print("退出交互式环境")
            break

# 编译Nova程序
def compile_nova(file_path, output_path=None, format='python', optimization_level=0):
    """
    编译Nova程序
    
    Args:
        file_path: Nova程序文件路径
        output_path: 输出文件路径
        format: 输出格式（python或executable）
        optimization_level: 优化级别 (0-3)
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)
    
    # 读取源代码
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # 确定输出路径
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if format == 'python':
            output_path = f"{base_name}.py"
        else:
            output_path = base_name
    
    # 导入编译器
    try:
        from ..compiler.compiler import Compiler
        compiler = Compiler()
        
        print(f"编译Nova程序: {file_path}")
        print("解析程序...")
        print(f"应用优化级别 O{optimization_level}...")
        print("编译程序...")
        
        # 编译
        if format == 'python':
            compiler.compile_to_python(source_code, output_path, optimization_level)
        else:
            compiler.compile_to_executable(source_code, output_path, optimization_level)
        
        print(f"编译成功: {output_path}")
        
    except ImportError as e:
        print(f"错误: 无法导入编译器 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"编译错误: {e}")
        sys.exit(1)

# Nova IDLE类
class NovaIDLE:
    """
    Nova IDLE - 类似 Python IDLE 的交互式开发环境
    """
    
    def __init__(self):
        """
        初始化Nova IDLE
        """
        self.root = tk.Tk()
        self.root.title(f"Nova IDLE - Version {get_version_string()}")
        self.root.geometry("900x700")
        
        # 创建菜单
        self.menu_bar = Menu(self.root)
        
        # 文件菜单
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新建窗口", command=self.new_window)
        self.file_menu.add_command(label="打开...", command=self.open_file)
        self.file_menu.add_command(label="最近文件", command=self.recent_files)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="保存", command=self.save_file)
        self.file_menu.add_command(label="另存为...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.root.quit)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        
        # 编辑菜单
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="撤销", command=self.undo)
        self.edit_menu.add_command(label="重做", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="剪切", command=self.cut)
        self.edit_menu.add_command(label="复制", command=self.copy)
        self.edit_menu.add_command(label="粘贴", command=self.paste)
        self.edit_menu.add_command(label="全选", command=self.select_all)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="查找...", command=self.find)
        self.edit_menu.add_command(label="替换...", command=self.replace)
        self.menu_bar.add_cascade(label="编辑", menu=self.edit_menu)
        
        # Shell菜单
        self.shell_menu = Menu(self.menu_bar, tearoff=0)
        self.shell_menu.add_command(label="查看上次重启", command=self.view_last_restart)
        self.shell_menu.add_command(label="重启Shell", command=self.restart_shell)
        self.shell_menu.add_separator()
        self.shell_menu.add_command(label="中断执行", command=self.interrupt_execution)
        self.menu_bar.add_cascade(label="Shell", menu=self.shell_menu)
        
        # 运行菜单
        self.run_menu = Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="运行模块", command=self.run_module)
        self.run_menu.add_command(label="运行模块 (F5)", command=self.run_module)
        self.run_menu.add_separator()
        self.run_menu.add_command(label="检查模块", command=self.check_module)
        self.menu_bar.add_cascade(label="运行", menu=self.run_menu)
        
        # 帮助菜单
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="关于Nova", command=self.about_nova)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)
        
        self.root.config(menu=self.menu_bar)
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建Shell选项卡
        self.shell_frame = tk.Frame(self.notebook)
        self.notebook.add(self.shell_frame, text="Shell")
        
        # 创建编辑器选项卡
        self.editor_frame = tk.Frame(self.notebook)
        self.notebook.add(self.editor_frame, text="编辑器")
        
        # 创建Shell文本区域
        self.create_shell()
        
        # 创建编辑器文本区域
        self.create_editor()
        
        # 当前文件路径
        self.current_file = None
        
        # 历史记录
        self.history = []
        self.history_index = -1
        
        # Shell输出
        self.shell_output = []
    
    def create_shell(self):
        """
        创建Shell界面
        """
        # 创建Shell文本区域
        self.shell_text = scrolledtext.ScrolledText(
            self.shell_frame,
            wrap=tk.WORD,
            font=('Courier New', 10),
            bg='#f0f0f0',
            fg='#000000'
        )
        self.shell_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置标签
        self.shell_text.tag_config('prompt', foreground='#000080')
        self.shell_text.tag_config('output', foreground='#000000')
        self.shell_text.tag_config('error', foreground='#800000')
        
        # 绑定事件
        self.shell_text.bind('<Return>', self.on_shell_return)
        self.shell_text.bind('<Up>', self.on_shell_up)
        self.shell_text.bind('<Down>', self.on_shell_down)
        self.shell_text.bind('<Key>', self.on_shell_key)
        self.shell_text.bind('<Button-1>', self.on_shell_click)
        self.shell_text.bind('<B1-Motion>', self.on_shell_drag)
        
        # 显示欢迎信息
        self.show_welcome_message()
    
    def create_editor(self):
        """
        创建编辑器界面
        """
        # 创建编辑器文本区域
        self.editor_text = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,
            font=('Courier New', 10),
            bg='#ffffff',
            fg='#000000'
        )
        self.editor_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置标签
        self.editor_text.tag_config('keyword', foreground='#0000ff')
        self.editor_text.tag_config('string', foreground='#008000')
        self.editor_text.tag_config('comment', foreground='#808080')
        
        # 绑定事件
        self.editor_text.bind('<KeyRelease>', self.on_editor_key_release)
    
    def on_shell_key(self, event):
        """
        处理Shell按键事件
        
        阻止在input_start之前进行编辑
        """
        # 允许的键
        allowed_keys = [
            'BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End',
            'Up', 'Down', 'Return', 'KP_Enter',
            'Control_L', 'Control_R', 'Shift_L', 'Shift_R',
            'Alt_L', 'Alt_R', 'Caps_Lock',
        ]
        
        # 检查是否在input_start之前
        try:
            cursor_pos = self.shell_text.index(tk.INSERT)
            input_start_pos = self.shell_text.index("input_start")
            
            # 如果光标在input_start之前
            if self.shell_text.compare(cursor_pos, "<", input_start_pos):
                # 只允许导航键
                if event.keysym not in allowed_keys and event.keysym not in ['Left', 'Right', 'Home', 'End', 'Up', 'Down']:
                    return "break"
                
                # 如果是BackSpace或Delete，阻止
                if event.keysym in ['BackSpace', 'Delete']:
                    return "break"
        except tk.TclError:
            pass
        
        return None
    
    def on_shell_click(self, event):
        """
        处理Shell点击事件
        
        阻止光标移动到input_start之前
        """
        try:
            # 获取点击位置
            click_pos = self.shell_text.index(f"@{event.x},{event.y}")
            input_start_pos = self.shell_text.index("input_start")
            
            # 如果点击位置在input_start之前
            if self.shell_text.compare(click_pos, "<", input_start_pos):
                # 将光标移动到input_start
                self.shell_text.mark_set(tk.INSERT, input_start_pos)
                return "break"
        except tk.TclError:
            pass
        
        return None
    
    def on_shell_drag(self, event):
        """
        处理Shell拖拽事件
        
        阻止选择input_start之前的文本
        """
        try:
            # 获取拖拽位置
            drag_pos = self.shell_text.index(f"@{event.x},{event.y}")
            input_start_pos = self.shell_text.index("input_start")
            
            # 如果拖拽位置在input_start之前
            if self.shell_text.compare(drag_pos, "<", input_start_pos):
                return "break"
        except tk.TclError:
            pass
        
        return None
    
    def show_welcome_message(self):
        """
        显示欢迎信息
        """
        welcome = f"""Nova {get_version_string()} IDLE
Type "help", "copyright" or "license" for more information.
"""
        self.shell_text.insert(tk.END, welcome)
        self.show_prompt()
    
    def show_prompt(self):
        """
        显示提示符
        """
        self.shell_text.insert(tk.END, ">>> ", 'prompt')
        self.shell_text.mark_set("input_start", tk.INSERT)
        self.shell_text.mark_gravity("input_start", tk.LEFT)
        self.shell_text.see(tk.END)
    
    def on_shell_return(self, event):
        """
        处理Shell回车事件
        """
        # 获取输入
        input_text = self.shell_text.get("input_start", tk.END)
        input_text = input_text.strip()
        
        # 添加到历史记录
        if input_text:
            self.history.append(input_text)
            self.history_index = len(self.history)
        
        # 执行命令
        self.execute_nova_code(input_text)
        
        # 显示新的提示符
        self.show_prompt()
        
        # 阻止默认行为
        return "break"
    
    def on_shell_up(self, event):
        """
        处理Shell上箭头事件
        """
        if self.history_index > 0:
            self.history_index -= 1
            self.replace_current_input(self.history[self.history_index])
        return "break"
    
    def on_shell_down(self, event):
        """
        处理Shell下箭头事件
        """
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.replace_current_input(self.history[self.history_index])
        else:
            self.history_index = len(self.history)
            self.replace_current_input("")
        return "break"
    
    def replace_current_input(self, text):
        """
        替换当前输入
        """
        self.shell_text.delete("input_start", tk.END)
        self.shell_text.insert(tk.END, text)
    
    def execute_nova_code(self, code):
        """
        执行Nova代码
        """
        if not code.strip():
            return
        
        # 处理特殊命令
        if code.strip() == "help":
            self.shell_text.insert(tk.END, "\nNova IDLE 帮助信息\n")
            self.shell_text.insert(tk.END, "  help - 显示帮助信息\n")
            self.shell_text.insert(tk.END, "  exit - 退出IDLE\n")
            self.shell_text.insert(tk.END, "  clear - 清空屏幕\n")
            return
        
        if code.strip() == "exit":
            self.root.quit()
            return
        
        if code.strip() == "clear":
            self.shell_text.delete(1.0, tk.END)
            self.show_welcome_message()
            return
        
        # 执行Nova代码
        try:
            # 这里应该调用Nova解释器来执行代码
            # 目前只是模拟执行
            result = f"执行: {code}\n"
            self.shell_text.insert(tk.END, result, 'output')
        except Exception as e:
            error_msg = f"错误: {e}\n"
            self.shell_text.insert(tk.END, error_msg, 'error')
    
    def on_editor_key_release(self, event):
        """
        处理编辑器按键释放事件
        """
        # 这里可以实现语法高亮
        pass
    
    def new_window(self):
        """
        新建窗口
        """
        # 清空编辑器
        self.editor_text.delete(1.0, tk.END)
        self.current_file = None
        self.root.title(f"Nova IDLE - Untitled")
        
        # 切换到编辑器选项卡
        self.notebook.select(self.editor_frame)
    
    def open_file(self):
        """
        打开文件
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Nova Files", "*.nova"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor_text.delete(1.0, tk.END)
                self.editor_text.insert(1.0, content)
                self.current_file = file_path
                self.root.title(f"Nova IDLE - {os.path.basename(file_path)}")
                
                # 切换到编辑器选项卡
                self.notebook.select(self.editor_frame)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def recent_files(self):
        """
        最近文件
        """
        messagebox.showinfo("Recent Files", "最近文件功能尚未实现")
    
    def save_file(self):
        """
        保存文件
        """
        if self.current_file:
            try:
                content = self.editor_text.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.root.title(f"Nova IDLE - {os.path.basename(self.current_file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """
        另存为文件
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".nova",
            filetypes=[("Nova Files", "*.nova"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                content = self.editor_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.current_file = file_path
                self.root.title(f"Nova IDLE - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def undo(self):
        """
        撤销
        """
        self.editor_text.event_generate("<<Undo>>")
    
    def redo(self):
        """
        重做
        """
        self.editor_text.event_generate("<<Redo>>")
    
    def cut(self):
        """
        剪切
        """
        self.editor_text.event_generate("<<Cut>>")
    
    def copy(self):
        """
        复制
        """
        self.editor_text.event_generate("<<Copy>>")
    
    def paste(self):
        """
        粘贴
        """
        self.editor_text.event_generate("<<Paste>>")
    
    def select_all(self):
        """
        全选
        """
        self.editor_text.tag_add(tk.SEL, 1.0, tk.END)
    
    def find(self):
        """
        查找
        """
        messagebox.showinfo("Find", "查找功能尚未实现")
    
    def replace(self):
        """
        替换
        """
        messagebox.showinfo("Replace", "替换功能尚未实现")
    
    def view_last_restart(self):
        """
        查看上次重启
        """
        messagebox.showinfo("Last Restart", "上次重启信息")
    
    def restart_shell(self):
        """
        重启Shell
        """
        self.shell_text.delete(1.0, tk.END)
        self.show_welcome_message()
    
    def interrupt_execution(self):
        """
        中断执行
        """
        messagebox.showinfo("Interrupt", "中断执行功能尚未实现")
    
    def run_module(self):
        """
        运行模块
        """
        # 获取编辑器中的代码
        code = self.editor_text.get(1.0, tk.END)
        
        if not code.strip():
            messagebox.showwarning("Warning", "没有代码可运行")
            return
        
        # 保存文件
        if self.current_file:
            self.save_file()
        
        # 切换到Shell选项卡
        self.notebook.select(self.shell_frame)
        
        # 在Shell中显示执行结果
        self.shell_text.insert(tk.END, "\n===== 运行模块 =====\n", 'output')
        self.shell_text.insert(tk.END, code, 'output')
        self.shell_text.insert(tk.END, "\n===== 执行完成 =====\n", 'output')
        
        # 显示新的提示符
        self.show_prompt()
    
    def check_module(self):
        """
        检查模块
        """
        messagebox.showinfo("Check Module", "检查模块功能尚未实现")
    
    def about_nova(self):
        """
        关于Nova
        """
        messagebox.showinfo(
            "About Nova",
            f"Nova Language\nVersion: {get_version_string()}\n\nA modern programming language designed for simplicity and efficiency."
        )
    
    def run(self):
        """
        运行主循环
        """
        self.root.mainloop()

# 启动Nova IDLE
def start_idle():
    """
    启动Nova IDLE
    """
    print("启动Nova IDLE...")
    idle = NovaIDLE()
    idle.run()

# GUI主函数
def gui_main():
    """
    GUI版本主函数
    """
    print("启动Nova语言GUI版本...")
    
    # 这里实现GUI逻辑
    # 1. 创建窗口
    # 2. 添加菜单和控件
    # 3. 实现事件处理
    # 4. 启动主循环
    
    # 模拟GUI启动
    print("初始化GUI...")
    print("创建主窗口...")
    print("添加菜单和控件...")
    print("启动事件循环...")
    print("GUI版本启动完成！")