"""
Nova调试器

类似于Python的pdb，提供调试功能
"""

import sys
import os
from typing import Optional, Dict, List, Any

class NovaDebugger:
    """
    Nova调试器
    """
    
    def __init__(self):
        """
        初始化调试器
        """
        self.breakpoints = set()
        self.current_frame = None
        self.stepping = False
        self.step_into = False
        self.step_over = False
        self.step_out = False
        self.stack = []
        self.locals = {}
        self.globals = {}
        self.commands = {
            'h': self.help,
            'help': self.help,
            'n': self.next,
            'next': self.next,
            's': self.step,
            'step': self.step,
            'c': self.continue_execution,
            'continue': self.continue_execution,
            'l': self.list_code,
            'list': self.list_code,
            'p': self.print_var,
            'print': self.print_var,
            'pp': self.pretty_print,
            'b': self.set_breakpoint,
            'break': self.set_breakpoint,
            'cl': self.clear_breakpoint,
            'clear': self.clear_breakpoint,
            'w': self.where,
            'where': self.where,
            'q': self.quit,
            'quit': self.quit,
            'r': self.return_cmd,
            'return': self.return_cmd,
            'a': self.args,
            'args': self.args,
        }
    
    def help(self, args: List[str] = None):
        """
        显示帮助信息
        
        Args:
            args: 命令参数
        """
        help_text = """
Nova调试器命令：

h(elp)         显示帮助信息
n(ext)         执行下一行（不进入函数）
s(tep)         执行下一行（进入函数）
c(ontinue)     继续执行，直到遇到断点
l(ist)         列出当前代码
p(rint) expr   打印表达式的值
pp expr        美化打印表达式的值
b(reak) [file:]line 设置断点
cl(ear) [file:]line 清除断点
w(here)        显示调用栈
q(uit)         退出调试器
r(eturn)       继续执行，直到当前函数返回
a(rgs)         显示当前函数的参数
"""
        print(help_text)
    
    def next(self, args: List[str] = None):
        """
        执行下一行（不进入函数）
        
        Args:
            args: 命令参数
        """
        self.step_over = True
        return True
    
    def step(self, args: List[str] = None):
        """
        执行下一行（进入函数）
        
        Args:
            args: 命令参数
        """
        self.step_into = True
        return True
    
    def continue_execution(self, args: List[str] = None):
        """
        继续执行，直到遇到断点
        
        Args:
            args: 命令参数
        """
        self.stepping = False
        return True
    
    def list_code(self, args: List[str] = None):
        """
        列出当前代码
        
        Args:
            args: 命令参数
        """
        if not self.current_frame:
            print("没有当前帧")
            return
        
        # 这里应该显示当前帧的代码
        # 目前只是模拟
        print(f"当前行: {self.current_frame.get('line', 0)}")
        print("代码列表功能尚未完全实现")
    
    def print_var(self, args: List[str] = None):
        """
        打印表达式的值
        
        Args:
            args: 命令参数
        """
        if not args:
            print("请提供要打印的表达式")
            return
        
        expr = ' '.join(args)
        
        # 尝试在局部变量中查找
        if expr in self.locals:
            print(f"{expr} = {self.locals[expr]}")
        # 尝试在全局变量中查找
        elif expr in self.globals:
            print(f"{expr} = {self.globals[expr]}")
        else:
            print(f"未找到变量: {expr}")
    
    def pretty_print(self, args: List[str] = None):
        """
        美化打印表达式的值
        
        Args:
            args: 命令参数
        """
        if not args:
            print("请提供要打印的表达式")
            return
        
        expr = ' '.join(args)
        
        # 尝试在局部变量中查找
        if expr in self.locals:
            import pprint
            pprint.pprint(self.locals[expr])
        # 尝试在全局变量中查找
        elif expr in self.globals:
            import pprint
            pprint.pprint(self.globals[expr])
        else:
            print(f"未找到变量: {expr}")
    
    def set_breakpoint(self, args: List[str] = None):
        """
        设置断点
        
        Args:
            args: 命令参数，格式为 [file:]line
        """
        if not args:
            print("请提供断点位置，格式为 [file:]line")
            return
        
        bp = ' '.join(args)
        
        # 解析断点位置
        if ':' in bp:
            file, line = bp.split(':', 1)
            try:
                line = int(line)
                self.breakpoints.add((file, line))
                print(f"断点已设置: {file}:{line}")
            except ValueError:
                print(f"无效的行号: {line}")
        else:
            try:
                line = int(bp)
                if self.current_frame:
                    file = self.current_frame.get('file', '')
                    self.breakpoints.add((file, line))
                    print(f"断点已设置: {file}:{line}")
                else:
                    print("没有当前文件")
            except ValueError:
                print(f"无效的行号: {bp}")
    
    def clear_breakpoint(self, args: List[str] = None):
        """
        清除断点
        
        Args:
            args: 命令参数，格式为 [file:]line
        """
        if not args:
            print("请提供断点位置，格式为 [file:]line")
            return
        
        bp = ' '.join(args)
        
        # 解析断点位置
        if ':' in bp:
            file, line = bp.split(':', 1)
            try:
                line = int(line)
                if (file, line) in self.breakpoints:
                    self.breakpoints.remove((file, line))
                    print(f"断点已清除: {file}:{line}")
                else:
                    print(f"断点不存在: {file}:{line}")
            except ValueError:
                print(f"无效的行号: {line}")
        else:
            try:
                line = int(bp)
                if self.current_frame:
                    file = self.current_frame.get('file', '')
                    if (file, line) in self.breakpoints:
                        self.breakpoints.remove((file, line))
                        print(f"断点已清除: {file}:{line}")
                    else:
                        print(f"断点不存在: {file}:{line}")
                else:
                    print("没有当前文件")
            except ValueError:
                print(f"无效的行号: {bp}")
    
    def where(self, args: List[str] = None):
        """
        显示调用栈
        
        Args:
            args: 命令参数
        """
        if not self.stack:
            print("调用栈为空")
            return
        
        print("调用栈:")
        for i, frame in enumerate(self.stack):
            file = frame.get('file', '<unknown>')
            line = frame.get('line', 0)
            func = frame.get('function', '<unknown>')
            print(f"  {i}: {func} at {file}:{line}")
    
    def quit(self, args: List[str] = None):
        """
        退出调试器
        
        Args:
            args: 命令参数
        """
        print("退出调试器")
        sys.exit(0)
    
    def return_cmd(self, args: List[str] = None):
        """
        继续执行，直到当前函数返回
        
        Args:
            args: 命令参数
        """
        self.step_out = True
        return True
    
    def args(self, args: List[str] = None):
        """
        显示当前函数的参数
        
        Args:
            args: 命令参数
        """
        if not self.current_frame:
            print("没有当前帧")
            return
        
        args_info = self.current_frame.get('args', {})
        if args_info:
            print("函数参数:")
            for name, value in args_info.items():
                print(f"  {name} = {value}")
        else:
            print("没有参数")
    
    def set_trace(self, frame: Dict[str, Any] = None):
        """
        设置跟踪点
        
        Args:
            frame: 当前帧信息
        """
        if frame:
            self.current_frame = frame
            self.stack.append(frame)
            self.locals = frame.get('locals', {})
            self.globals = frame.get('globals', {})
        
        self.stepping = True
        self.step_into = False
        self.step_over = False
        self.step_out = False
        
        # 进入调试循环
        self.debug_loop()
    
    def debug_loop(self):
        """
        调试循环
        """
        while self.stepping:
            try:
                # 显示当前行
                if self.current_frame:
                    file = self.current_frame.get('file', '<unknown>')
                    line = self.current_frame.get('line', 0)
                    func = self.current_frame.get('function', '<unknown>')
                    print(f"\n> {file}({line}) {func}()")
                
                # 读取命令
                cmd = input("(Pdb) ").strip()
                
                if not cmd:
                    continue
                
                # 解析命令
                parts = cmd.split()
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else None
                
                # 执行命令
                if command in self.commands:
                    result = self.commands[command](args)
                    if result:
                        break
                else:
                    print(f"未知命令: {command}")
                    print("输入 'h' 或 'help' 查看帮助")
            
            except KeyboardInterrupt:
                print("\n输入 'q' 或 'quit' 退出调试器")
            except EOFError:
                print("\n输入 'q' 或 'quit' 退出调试器")
    
    def check_breakpoint(self, file: str, line: int) -> bool:
        """
        检查是否在断点处
        
        Args:
            file: 文件名
            line: 行号
        
        Returns:
            是否在断点处
        """
        return (file, line) in self.breakpoints
    
    def should_stop(self, file: str, line: int) -> bool:
        """
        检查是否应该停止执行
        
        Args:
            file: 文件名
            line: 行号
        
        Returns:
            是否应该停止执行
        """
        # 检查断点
        if self.check_breakpoint(file, line):
            return True
        
        # 检查单步执行
        if self.stepping:
            if self.step_into:
                return True
            elif self.step_over:
                return True
            elif self.step_out:
                return True
        
        return False


# 全局调试器实例
_debugger = None

def get_debugger() -> NovaDebugger:
    """
    获取全局调试器实例
    
    Returns:
        调试器实例
    """
    global _debugger
    if _debugger is None:
        _debugger = NovaDebugger()
    return _debugger

def set_debugger(debugger: NovaDebugger):
    """
    设置全局调试器实例
    
    Args:
        debugger: 调试器实例
    """
    global _debugger
    _debugger = debugger

def reset_debugger():
    """
    重置全局调试器实例
    """
    global _debugger
    _debugger = None


# 导出
__all__ = [
    'NovaDebugger',
    'get_debugger',
    'set_debugger',
    'reset_debugger'
]