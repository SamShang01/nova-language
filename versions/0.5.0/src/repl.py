"""
Nova语言REPL（Read-Eval-Print Loop）
支持多行输入、自动补全、类型信息显示和模块导入
"""

import sys
import os
from typing import Optional, List, Dict

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine
from nova.version import get_version_string


class NovaREPL:
    """
    Nova语言REPL
    
    功能：
    - 多行输入支持
    - 自动补全
    - 类型信息显示
    - 模块导入
    - 历史记录
    """
    
    def __init__(self):
        """
        初始化REPL
        """
        self.vm = VirtualMachine()
        self.analyzer = SemanticAnalyzer()
        self.codegen = CodeGenerator()
        
        self.variables: Dict[str, object] = {}
        self.functions: Dict[str, object] = {}
        self.imported_modules: List[str] = []
        
        self.multiline_buffer: List[str] = []
        self.in_multiline = False
        
        self.keywords = [
            'func', 'struct', 'trait', 'impl', 'generic',
            'let', 'if', 'else', 'for', 'while', 'return',
            'use', 'where', 'true', 'false', 'null'
        ]
        
        self.types = ['int', 'float', 'string', 'bool', 'unit']
        
        self.stdlib_modules = [
            'std::core', 'std::math', 'std::string', 'std::io'
        ]
        
        self._setup_prompt_session()
    
    def _setup_prompt_session(self):
        """
        设置提示会话
        """
        if PROMPT_TOOLKIT_AVAILABLE:
            history_file = os.path.expanduser('~/.nova_history')
            all_words = self.keywords + self.types + self.stdlib_modules
            completer = WordCompleter(all_words, ignore_case=True)
            
            self.session = PromptSession(
                history=FileHistory(history_file),
                auto_suggest=AutoSuggestFromHistory(),
                completer=completer
            )
        else:
            self.session = None
    
    def _get_prompt(self) -> str:
        """
        获取提示符
        
        Returns:
            str: 提示符
        """
        if self.in_multiline:
            return '... '
        else:
            return 'nova> '
    
    def _is_complete_expression(self, line: str) -> bool:
        """
        检查表达式是否完整
        
        Args:
            line: 输入行
        
        Returns:
            bool: 是否完整
        """
        line = line.strip()
        
        if not line:
            return True
        
        # 检查括号平衡
        open_braces = line.count('{')
        close_braces = line.count('}')
        open_parens = line.count('(')
        close_parens = line.count(')')
        open_brackets = line.count('[')
        close_brackets = line.count(']')
        
        if open_braces > close_braces:
            return False
        
        if open_parens > close_parens:
            return False
        
        if open_brackets > close_brackets:
            return False
        
        # 检查是否以冒号结尾（表示需要更多代码）
        if line.endswith(':'):
            return False
        
        # 检查是否以逗号结尾（表示参数列表未完成）
        if line.endswith(','):
            return False
        
        return True
    
    def _read_input(self) -> str:
        """
        读取用户输入
        
        Returns:
            str: 输入内容
        """
        if PROMPT_TOOLKIT_AVAILABLE and self.session:
            try:
                line = self.session.prompt(self._get_prompt())
            except KeyboardInterrupt:
                print()
                return ''
            except EOFError:
                print()
                sys.exit(0)
        else:
            try:
                line = input(self._get_prompt())
            except KeyboardInterrupt:
                print()
                return ''
            except EOFError:
                print()
                sys.exit(0)
        
        # 过滤掉控制字符（ASCII码小于32的字符，除了换行符、制表符等）
        filtered_line = []
        for char in line:
            # 允许的字符：ASCII >= 32，或者换行符(10)、制表符(9)、回车符(13)
            if ord(char) >= 32 or ord(char) in [9, 10, 13]:
                filtered_line.append(char)
        
        return ''.join(filtered_line)
    
    def _execute_code(self, code: str):
        """
        执行代码
        
        Args:
            code: 要执行的代码
        """
        try:
            scanner = Scanner(code)
            tokens = scanner.scan_tokens()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            analyzed_ast = self.analyzer.analyze(ast)
            
            instructions, constants = self.codegen.generate(analyzed_ast)
            
            self.vm.load(instructions)
            result = self.vm.run()
            
            # 同步虚拟机环境中的变量和函数到REPL
            self._sync_environment()
            
            if result is not None:
                print(f"=> {result}")
            
        except EOFError:
            print()
            sys.exit(0)
        except Exception as e:
            print(f"错误: {e}")
    
    def _sync_environment(self):
        """
        同步虚拟机环境到REPL
        """
        for name, value in self.vm.environment.items():
            # 跳过内置函数
            if name in ['print', 'len', 'input']:
                continue
            
            # 检查是否是函数
            if callable(value):
                self.functions[name] = value
            else:
                self.variables[name] = value
    
    def _show_type_info(self, name: str):
        """
        显示变量或函数的类型信息
        
        Args:
            name: 变量或函数名称
        """
        if name in self.variables:
            value = self.variables[name]
            type_name = type(value).__name__
            print(f"{name}: {type_name} = {value}")
        elif name in self.functions:
            func = self.functions[name]
            print(f"{name}: function")
        else:
            print(f"未找到: {name}")
    
    def _handle_special_command(self, line: str) -> bool:
        """
        处理特殊命令
        
        Args:
            line: 输入行
        
        Returns:
            bool: 是否处理了特殊命令
        """
        line = line.strip()
        
        if line.startswith(':'):
            parts = line.split()
            command = parts[0]
            
            # 移除命令后面的分号
            if command.endswith(';'):
                command = command[:-1]
            
            if command == ':quit' or command == ':exit':
                print("再见！")
                sys.exit(0)
            
            elif command == ':help':
                self._show_help()
                return True
            
            elif command == ':clear':
                self.variables.clear()
                self.functions.clear()
                self.imported_modules.clear()
                print("已清除所有变量和函数")
                return True
            
            elif command == ':vars':
                self._show_variables()
                return True
            
            elif command == ':type' and len(parts) > 1:
                # 移除变量名后面的分号
                var_name = parts[1]
                if var_name.endswith(';'):
                    var_name = var_name[:-1]
                self._show_type_info(var_name)
                return True
            
            elif command == ':import' and len(parts) > 1:
                self._import_module(parts[1])
                return True
            
            elif command == ':multiline':
                self.in_multiline = not self.in_multiline
                if self.in_multiline:
                    print("进入多行模式（输入空行结束）")
                else:
                    print("退出多行模式")
                return True
        
        return False
    
    def _show_help(self):
        """
        显示帮助信息
        """
        print("""
Nova REPL 帮助
============

特殊命令:
  :quit, :exit    退出REPL
  :help           显示此帮助信息
  :clear          清除所有变量和函数
  :vars           显示所有变量
  :type <name>    显示变量或函数的类型信息
  :import <module> 导入模块
  :multiline       切换多行模式

快捷键:
  Ctrl+C          中断当前输入
  Ctrl+D          退出REPL

示例:
  let x = 42
  let y = 3.14
  let s = "Hello"
  func add(a: int, b: int) -> int { return a + b; }
  add(x, 10)
        """)
    
    def _show_variables(self):
        """
        显示所有变量
        """
        if not self.variables:
            print("没有定义的变量")
            return
        
        print("变量:")
        for name, value in self.variables.items():
            type_name = type(value).__name__
            print(f"  {name}: {type_name} = {value}")
    
    def _import_module(self, module_name: str):
        """
        导入模块
        
        Args:
            module_name: 模块名称
        """
        if module_name in self.imported_modules:
            print(f"模块 '{module_name}' 已导入")
            return
        
        self.imported_modules.append(module_name)
        print(f"已导入模块: {module_name}")
    
    def run(self):
        """
        运行REPL
        """
        version = get_version_string()
        print(f"""
Nova REPL v{version}
输入 ':help' 查看帮助信息
        """)
        
        while True:
            line = self._read_input()
            
            if self._handle_special_command(line):
                continue
            
            if not line:
                # 空行：如果在多行模式，执行缓冲的代码
                if self.in_multiline and self.multiline_buffer:
                    code = '\n'.join(self.multiline_buffer)
                    self.multiline_buffer = []
                    self.in_multiline = False
                    self._execute_code(code)
                continue
            
            # 添加到多行缓冲
            self.multiline_buffer.append(line)
            
            # 检查代码是否完整
            full_code = '\n'.join(self.multiline_buffer)
            if self._is_complete_expression(full_code):
                # 代码完整，执行并清空缓冲
                self._execute_code(full_code)
                self.multiline_buffer = []
                self.in_multiline = False
            else:
                # 代码不完整，继续多行模式
                self.in_multiline = True


def main():
    """
    主函数
    """
    repl = NovaREPL()
    repl.run()


if __name__ == '__main__':
    main()
