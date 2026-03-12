"""
Nova调试器 - 支持断点设置、变量查看、单步执行、调用栈查看
"""

import sys
import os
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum


class DebugCommand(Enum):
    """
    调试命令枚举
    """
    CONTINUE = 'continue'
    STEP = 'step'
    NEXT = 'next'
    BREAKPOINT = 'breakpoint'
    PRINT = 'print'
    BACKTRACE = 'backtrace'
    LIST = 'list'
    HELP = 'help'
    QUIT = 'quit'


class Breakpoint:
    """
    断点类
    """
    
    def __init__(self, file_path: str, line_number: int, condition: str = None):
        """
        初始化断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
            condition: 条件（可选）
        """
        self.file_path = file_path
        self.line_number = line_number
        self.condition = condition
        self.hit_count = 0
        self.enabled = True
    
    def should_break(self, variables: Dict[str, object]) -> bool:
        """
        判断是否应该中断
        
        Args:
            variables: 变量字典
        
        Returns:
            bool: 是否应该中断
        """
        if not self.enabled:
            return False
        
        if self.condition is None:
            return True
        
        try:
            return eval(self.condition, {}, variables)
        except:
            return False
    
    def __str__(self) -> str:
        """
        字符串表示
        
        Returns:
            str: 字符串表示
        """
        status = "enabled" if self.enabled else "disabled"
        condition_str = f" if {self.condition}" if self.condition else ""
        return f"{self.file_path}:{self.line_number} ({status}){condition_str}"


class Debugger:
    """
    Nova调试器
    
    功能：
    - 断点设置和管理
    - 变量查看
    - 单步执行
    - 调用栈查看
    """
    
    def __init__(self):
        """
        初始化调试器
        """
        self.breakpoints: Dict[str, List[Breakpoint]] = {}
        self.call_stack: List[Dict] = []
        self.variables: Dict[str, object] = {}
        self.current_frame: Optional[Dict] = None
        self.step_mode = False
        self.step_over = False
        self.step_depth = 0
        self.running = False
    
    def add_breakpoint(self, file_path: str, line_number: int, condition: str = None):
        """
        添加断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
            condition: 条件（可选）
        """
        if file_path not in self.breakpoints:
            self.breakpoints[file_path] = []
        
        bp = Breakpoint(file_path, line_number, condition)
        self.breakpoints[file_path].append(bp)
        
        print(f"断点 {len(self.breakpoints[file_path])}: {bp}")
    
    def remove_breakpoint(self, file_path: str, line_number: int):
        """
        移除断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
        """
        if file_path not in self.breakpoints:
            print(f"文件 {file_path} 没有断点")
            return
        
        for i, bp in enumerate(self.breakpoints[file_path]):
            if bp.line_number == line_number:
                del self.breakpoints[file_path][i]
                print(f"已移除断点: {file_path}:{line_number}")
                return
        
        print(f"未找到断点: {file_path}:{line_number}")
    
    def list_breakpoints(self):
        """
        列出所有断点
        """
        if not self.breakpoints:
            print("没有设置断点")
            return
        
        print("断点列表:")
        for file_path, bps in self.breakpoints.items():
            for i, bp in enumerate(bps):
                print(f"  {i + 1}. {bp}")
    
    def enable_breakpoint(self, file_path: str, line_number: int):
        """
        启用断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
        """
        if file_path not in self.breakpoints:
            print(f"文件 {file_path} 没有断点")
            return
        
        for bp in self.breakpoints[file_path]:
            if bp.line_number == line_number:
                bp.enabled = True
                print(f"已启用断点: {file_path}:{line_number}")
                return
        
        print(f"未找到断点: {file_path}:{line_number}")
    
    def disable_breakpoint(self, file_path: str, line_number: int):
        """
        禁用断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
        """
        if file_path not in self.breakpoints:
            print(f"文件 {file_path} 没有断点")
            return
        
        for bp in self.breakpoints[file_path]:
            if bp.line_number == line_number:
                bp.enabled = False
                print(f"已禁用断点: {file_path}:{line_number}")
                return
        
        print(f"未找到断点: {file_path}:{line_number}")
    
    def check_breakpoint(self, file_path: str, line_number: int) -> bool:
        """
        检查是否应该中断
        
        Args:
            file_path: 文件路径
            line_number: 行号
        
        Returns:
            bool: 是否应该中断
        """
        if file_path not in self.breakpoints:
            return False
        
        for bp in self.breakpoints[file_path]:
            if bp.line_number == line_number and bp.should_break(self.variables):
                bp.hit_count += 1
                print(f"\n断点 {bp.hit_count}: {file_path}:{line_number}")
                return True
        
        return False
    
    def print_variable(self, var_name: str):
        """
        打印变量值
        
        Args:
            var_name: 变量名
        """
        if var_name in self.variables:
            value = self.variables[var_name]
            type_name = type(value).__name__
            print(f"{var_name} = {value} ({type_name})")
        else:
            print(f"未找到变量: {var_name}")
    
    def print_all_variables(self):
        """
        打印所有变量
        """
        if not self.variables:
            print("没有变量")
            return
        
        print("变量:")
        for name, value in self.variables.items():
            type_name = type(value).__name__
            print(f"  {name} = {value} ({type_name})")
    
    def print_backtrace(self):
        """
        打印调用栈
        """
        if not self.call_stack:
            print("调用栈为空")
            return
        
        print("调用栈:")
        for i, frame in enumerate(self.call_stack):
            file_path = frame.get('file', '?')
            line_number = frame.get('line', '?')
            function_name = frame.get('function', '?')
            print(f"  #{i} {function_name} at {file_path}:{line_number}")
    
    def push_frame(self, file_path: str, line_number: int, function_name: str):
        """
        推入调用栈帧
        
        Args:
            file_path: 文件路径
            line_number: 行号
            function_name: 函数名
        """
        frame = {
            'file': file_path,
            'line': line_number,
            'function': function_name
        }
        self.call_stack.append(frame)
        self.current_frame = frame
    
    def pop_frame(self):
        """
        弹出调用栈帧
        """
        if self.call_stack:
            self.call_stack.pop()
            if self.call_stack:
                self.current_frame = self.call_stack[-1]
            else:
                self.current_frame = None
    
    def set_variable(self, var_name: str, value: object):
        """
        设置变量值
        
        Args:
            var_name: 变量名
            value: 值
        """
        self.variables[var_name] = value
        print(f"{var_name} = {value}")
    
    def step_into(self):
        """
        单步进入
        """
        self.step_mode = True
        self.step_over = False
    
    def step_over(self):
        """
        单步跳过
        """
        self.step_mode = True
        self.step_over = True
        self.step_depth = len(self.call_stack)
    
    def step_out(self):
        """
        单步跳出
        """
        self.step_mode = True
        self.step_over = True
        self.step_depth = len(self.call_stack) - 1
    
    def continue_execution(self):
        """
        继续执行
        """
        self.step_mode = False
        self.step_over = False
    
    def should_stop(self, file_path: str, line_number: int) -> bool:
        """
        判断是否应该停止
        
        Args:
            file_path: 文件路径
            line_number: 行号
        
        Returns:
            bool: 是否应该停止
        """
        if self.check_breakpoint(file_path, line_number):
            return True
        
        if self.step_mode:
            if self.step_over:
                current_depth = len(self.call_stack)
                if current_depth <= self.step_depth:
                    return True
            else:
                return True
        
        return False
    
    def show_help(self):
        """
        显示帮助信息
        """
        print("""
Nova调试器命令
============

执行控制:
  continue (c)    继续执行
  step (s)        单步进入
  next (n)        单步跳过
  finish (f)      单步跳出

断点管理:
  break (b) <file:line> [condition]  设置断点
  delete (d) <file:line>             删除断点
  enable <file:line>                 启用断点
  disable <file:line>                禁用断点
  info breakpoints (info b)           列出断点

变量查看:
  print (p) <var>                    打印变量
  print *<expr>                      打印表达式
  info locals (info l)                打印所有局部变量
  set <var> = <value>               设置变量值

调用栈:
  backtrace (bt)                     显示调用栈
  frame <n>                          切换栈帧

其他:
  list (l) [n]                      显示源代码
  help (h)                           显示帮助
  quit (q)                           退出调试器
        """)
    
    def show_source(self, file_path: str, line_number: int, context: int = 5):
        """
        显示源代码
        
        Args:
            file_path: 文件路径
            line_number: 当前行号
            context: 上下文行数
        """
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start = max(0, line_number - context - 1)
        end = min(len(lines), line_number + context)
        
        print(f"\n{file_path}:{line_number}")
        for i in range(start, end):
            marker = "=>" if i == line_number - 1 else "  "
            print(f"{marker} {i + 1:4d} {lines[i]}", end='')
    
    def run_repl(self):
        """
        运行调试器REPL
        """
        print("\nNova调试器 v0.2.0")
        print("输入 'help' 查看帮助信息\n")
        
        while self.running:
            try:
                if self.current_frame:
                    prompt = f"(nova:{self.current_frame.get('function', '?')}) "
                else:
                    prompt = "(nova) "
                
                line = input(prompt).strip()
                
                if not line:
                    continue
                
                self._execute_command(line)
                
            except KeyboardInterrupt:
                print("\n使用 'quit' 退出调试器")
            except EOFError:
                print("\n退出调试器")
                break
    
    def _execute_command(self, line: str):
        """
        执行命令
        
        Args:
            line: 命令行
        """
        parts = line.split()
        command = parts[0].lower()
        
        if command in ['continue', 'c']:
            self.continue_execution()
        
        elif command in ['step', 's']:
            self.step_into()
        
        elif command in ['next', 'n']:
            self.step_over()
        
        elif command in ['finish', 'f']:
            self.step_out()
        
        elif command in ['break', 'b']:
            if len(parts) < 2:
                print("用法: break <file:line> [condition]")
                return
            
            location = parts[1]
            if ':' in location:
                file_path, line_str = location.split(':', 1)
                try:
                    line_number = int(line_str)
                    condition = ' '.join(parts[2:]) if len(parts) > 2 else None
                    self.add_breakpoint(file_path, line_number, condition)
                except ValueError:
                    print("无效的行号")
            else:
                print("用法: break <file:line> [condition]")
        
        elif command in ['delete', 'd']:
            if len(parts) < 2:
                print("用法: delete <file:line>")
                return
            
            location = parts[1]
            if ':' in location:
                file_path, line_str = location.split(':', 1)
                try:
                    line_number = int(line_str)
                    self.remove_breakpoint(file_path, line_number)
                except ValueError:
                    print("无效的行号")
            else:
                print("用法: delete <file:line>")
        
        elif command == 'enable':
            if len(parts) < 2:
                print("用法: enable <file:line>")
                return
            
            location = parts[1]
            if ':' in location:
                file_path, line_str = location.split(':', 1)
                try:
                    line_number = int(line_str)
                    self.enable_breakpoint(file_path, line_number)
                except ValueError:
                    print("无效的行号")
            else:
                print("用法: enable <file:line>")
        
        elif command == 'disable':
            if len(parts) < 2:
                print("用法: disable <file:line>")
                return
            
            location = parts[1]
            if ':' in location:
                file_path, line_str = location.split(':', 1)
                try:
                    line_number = int(line_str)
                    self.disable_breakpoint(file_path, line_number)
                except ValueError:
                    print("无效的行号")
            else:
                print("用法: disable <file:line>")
        
        elif command == 'info':
            if len(parts) < 2:
                print("用法: info <breakpoints|locals>")
                return
            
            subcommand = parts[1].lower()
            if subcommand in ['breakpoints', 'b']:
                self.list_breakpoints()
            elif subcommand in ['locals', 'l']:
                self.print_all_variables()
            else:
                print("未知命令: info " + subcommand)
        
        elif command in ['print', 'p']:
            if len(parts) < 2:
                print("用法: print <var>")
                return
            
            var_name = parts[1]
            self.print_variable(var_name)
        
        elif command in ['backtrace', 'bt']:
            self.print_backtrace()
        
        elif command in ['list', 'l']:
            if self.current_frame:
                file_path = self.current_frame.get('file', '')
                line_number = self.current_frame.get('line', 1)
                context = int(parts[1]) if len(parts) > 1 else 5
                self.show_source(file_path, line_number, context)
            else:
                print("没有当前栈帧")
        
        elif command == 'set':
            if len(parts) < 3:
                print("用法: set <var> = <value>")
                return
            
            var_name = parts[1]
            value_str = ' '.join(parts[3:])
            try:
                value = eval(value_str)
                self.set_variable(var_name, value)
            except:
                print(f"无效的值: {value_str}")
        
        elif command in ['help', 'h']:
            self.show_help()
        
        elif command in ['quit', 'q']:
            self.running = False
            print("退出调试器")
        
        else:
            print(f"未知命令: {command}")
            print("输入 'help' 查看帮助信息")


def main():
    """
    主函数
    """
    debugger = Debugger()
    debugger.running = True
    debugger.run_repl()


if __name__ == '__main__':
    main()
