"""
Nova IDLE 语法高亮模块
"""

import tkinter as tk
import re


class NovaSyntaxHighlighter:
    """
    Nova语言语法高亮器
    """
    
    def __init__(self, text_widget):
        """
        初始化语法高亮器
        
        Args:
            text_widget: tkinter文本控件
        """
        self.text_widget = text_widget
        
        # 配置标签样式
        self._configure_tags()
    
    def _configure_tags(self):
        """
        配置语法高亮标签样式
        """
        # 关键字 - 蓝色加粗
        self.text_widget.tag_config('keyword', foreground='#0000FF', font=('Courier New', 10, 'bold'))
        
        # 字符串 - 绿色
        self.text_widget.tag_config('string', foreground='#008000')
        
        # 注释 - 灰色斜体
        self.text_widget.tag_config('comment', foreground='#808080', font=('Courier New', 10, 'italic'))
        
        # 数字 - 橙色
        self.text_widget.tag_config('number', foreground='#FF6600')
        
        # 内置函数 - 紫色
        self.text_widget.tag_config('builtin', foreground='#800080')
        
        # 运算符 - 红色
        self.text_widget.tag_config('operator', foreground='#FF0000')
    
    def highlight(self):
        """
        执行语法高亮
        """
        try:
            # 移除所有现有标签
            for tag in ['keyword', 'string', 'comment', 'number', 'builtin', 'operator']:
                self.text_widget.tag_remove(tag, '1.0', tk.END)
            
            # 获取文本内容
            content = self.text_widget.get('1.0', tk.END)
            
            # 逐行处理
            lines = content.split('\n')
            for line_num, line in enumerate(lines, start=1):
                self._highlight_line(line_num, line)
                
        except Exception as e:
            # 如果出错，静默处理（避免影响用户体验）
            print(f"[Syntax Highlight Error] {e}")
    
    def _highlight_line(self, line_num, line):
        """
        高亮单行文本
        
        Args:
            line_num: 行号
            line: 行内容
        """
        # Nova关键字
        keywords = [
            'mod', 'module', 'use', 'from', 'import', 'feature', 'as',
            'func', 'fn', 'function', 'let', 'var', 'const', 'del',
            'if', 'else', 'for', 'while', 'loop', 'match',
            'break', 'continue', 'return',
            'struct', 'enum', 'union', 'trait', 'impl',
            'self', 'async', 'await', 'actor',
            'generic', 'template', 'where', 'in', 'manda', 'default',
            'true', 'false',
            'int', 'float', 'double', 'string', 'bool', 'char', 'void',
            'private', 'protected', 'public',
            'class', 'extends', 'super', 'this',
            'init', 'static', 'abstract', 'mut', 'type'
        ]
        
        # 内置函数
        builtins = [
            'print', 'println', 'len', 'input', 'type', 'str', 'int', 'float',
            'abs', 'max', 'min', 'sum', 'round', 'range', 'open', 'read', 'write'
        ]
        
        # 高亮注释（# 开头）
        comment_match = re.search(r'#.*', line)
        if comment_match:
            start = comment_match.start()
            end = comment_match.end()
            self._add_tag('comment', line_num, start, end)
            # 注释后面的内容不需要再处理
            line = line[:start]
        
        # 高亮字符串（单引号和双引号）
        for match in re.finditer(r'["\']([^"\']*)["\']', line):
            self._add_tag('string', line_num, match.start(), match.end())
        
        # 高亮数字
        for match in re.finditer(r'\b\d+\.?\d*\b', line):
            self._add_tag('number', line_num, match.start(), match.end())
        
        # 高亮关键字
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, line):
                self._add_tag('keyword', line_num, match.start(), match.end())
        
        # 高亮内置函数
        for builtin in builtins:
            pattern = r'\b' + re.escape(builtin) + r'\b'
            for match in re.finditer(pattern, line):
                self._add_tag('builtin', line_num, match.start(), match.end())
        
        # 高亮运算符
        for match in re.finditer(r'[+\-*/%=<>!&|]+', line):
            self._add_tag('operator', line_num, match.start(), match.end())
    
    def _add_tag(self, tag, line_num, start_col, end_col):
        """
        为指定范围添加标签
        
        Args:
            tag: 标签名称
            line_num: 行号
            start_col: 开始列
            end_col: 结束列
        """
        start_index = f'{line_num}.{start_col}'
        end_index = f'{line_num}.{end_col}'
        self.text_widget.tag_add(tag, start_index, end_index)
