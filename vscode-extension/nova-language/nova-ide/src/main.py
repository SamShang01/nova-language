#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTabWidget, QTextEdit, QListWidget, 
                           QMenuBar, QMenu, QAction, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor

class NovaSyntaxHighlighter(QSyntaxHighlighter):
    """Nova语言语法高亮"""
    def __init__(self, parent=None):
        super(NovaSyntaxHighlighter, self).__init__(parent)
        
        # 关键字
        self.keywords = [
            'func', 'struct', 'class', 'if', 'else', 'while', 'for', 'switch',
            'case', 'default', 'return', 'let', 'var', 'const', 'import', 'from',
            'as', 'export', 'module', 'public', 'private', 'protected', 'static',
            'async', 'await', 'and', 'or', 'not', 'true', 'false', 'null'
        ]
        
        # 类型
        self.types = [
            'int', 'float', 'bool', 'string', 'void', 'any', 'List', 'Dict',
            'Set', 'Tuple'
        ]
        
        # 颜色定义
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor('#0000ff'))
        self.keyword_format.setFontWeight(QFont.Bold)
        
        self.type_format = QTextCharFormat()
        self.type_format.setForeground(QColor('#008080'))
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor('#008000'))
        
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor('#808080'))
        self.comment_format.setFontItalic(True)
        
    def highlightBlock(self, text):
        """高亮文本块"""
        # 高亮关键字
        for keyword in self.keywords:
            start = 0
            while True:
                start = text.find(keyword, start)
                if start == -1:
                    break
                length = len(keyword)
                self.setFormat(start, length, self.keyword_format)
                start += length
        
        # 高亮类型
        for type_name in self.types:
            start = 0
            while True:
                start = text.find(type_name, start)
                if start == -1:
                    break
                length = len(type_name)
                self.setFormat(start, length, self.type_format)
                start += length
        
        # 高亮字符串
        in_string = False
        string_start = 0
        for i, char in enumerate(text):
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_start = i
                else:
                    in_string = False
                    self.setFormat(string_start, i - string_start + 1, self.string_format)
        
        # 高亮注释
        comment_start = text.find('//')
        if comment_start != -1:
            self.setFormat(comment_start, len(text) - comment_start, self.comment_format)

class NovaIDE(QMainWindow):
    """Nova IDE主窗口"""
    def __init__(self):
        super(NovaIDE, self).__init__()
        self.setWindowTitle('Nova IDE')
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化变量
        self.current_file = None
        
        # 创建主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # 创建左侧文件浏览器
        self.file_browser = QListWidget()
        self.file_browser.setMaximumWidth(250)
        main_layout.addWidget(self.file_browser)
        
        # 创建右侧编辑区域
        right_layout = QVBoxLayout()
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        right_layout.addWidget(self.tab_widget)
        
        main_layout.addLayout(right_layout)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建初始标签
        self.add_new_tab()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        # 文件菜单
        file_menu = QMenu('文件', self)
        menu_bar.addMenu(file_menu)
        
        new_action = QAction('新建', self)
        new_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_action)
        
        open_action = QAction('打开', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('保存', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('另存为', self)
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = QMenu('编辑', self)
        menu_bar.addMenu(edit_menu)
        
        cut_action = QAction('剪切', self)
        cut_action.setShortcut('Ctrl+X')
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('复制', self)
        copy_action.setShortcut('Ctrl+C')
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('粘贴', self)
        paste_action.setShortcut('Ctrl+V')
        edit_menu.addAction(paste_action)
        
        # 运行菜单
        run_menu = QMenu('运行', self)
        menu_bar.addMenu(run_menu)
        
        run_action = QAction('运行', self)
        run_action.setShortcut('F5')
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)
    
    def add_new_tab(self):
        """添加新标签页"""
        editor = QTextEdit()
        editor.setFont(QFont('Consolas', 12))
        
        # 添加语法高亮
        highlighter = NovaSyntaxHighlighter(editor.document())
        
        tab_index = self.tab_widget.addTab(editor, '未命名.nova')
        self.tab_widget.setCurrentIndex(tab_index)
    
    def open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, '打开文件', '', 'Nova Files (*.nova);;All Files (*.*)')
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                editor = QTextEdit()
                editor.setFont(QFont('Consolas', 12))
                editor.setPlainText(content)
                
                # 添加语法高亮
                highlighter = NovaSyntaxHighlighter(editor.document())
                
                tab_index = self.tab_widget.addTab(editor, os.path.basename(file_path))
                self.tab_widget.setCurrentIndex(tab_index)
                
                # 更新当前文件路径
                self.current_file = file_path
                
                # 更新文件浏览器
                self.update_file_browser(os.path.dirname(file_path))
                
            except Exception as e:
                QMessageBox.critical(self, '错误', f'打开文件失败: {str(e)}')
    
    def save_file(self):
        """保存文件"""
        if self.current_file:
            try:
                editor = self.tab_widget.currentWidget()
                content = editor.toPlainText()
                
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                QMessageBox.information(self, '成功', '文件保存成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'保存文件失败: {str(e)}')
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """另存为文件"""
        file_path, _ = QFileDialog.getSaveFileName(self, '另存为', '', 'Nova Files (*.nova);;All Files (*.*)')
        if file_path:
            try:
                editor = self.tab_widget.currentWidget()
                content = editor.toPlainText()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 更新标签名
                tab_index = self.tab_widget.currentIndex()
                self.tab_widget.setTabText(tab_index, os.path.basename(file_path))
                
                # 更新当前文件路径
                self.current_file = file_path
                
                # 更新文件浏览器
                self.update_file_browser(os.path.dirname(file_path))
                
                QMessageBox.information(self, '成功', '文件保存成功')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'保存文件失败: {str(e)}')
    
    def run_code(self):
        """运行代码"""
        editor = self.tab_widget.currentWidget()
        content = editor.toPlainText()
        
        if not content:
            QMessageBox.warning(self, '警告', '没有代码可以运行')
            return
        
        try:
            # 保存临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.nova', delete=False) as temp_file:
                temp_file.write(content.encode('utf-8'))
                temp_file_path = temp_file.name
            
            # 运行Nova代码
            import subprocess
            result = subprocess.run(['nova', temp_file_path], 
                                  capture_output=True, text=True, shell=True)
            
            # 显示运行结果
            output = result.stdout
            error = result.stderr
            
            if error:
                QMessageBox.critical(self, '错误', f'运行错误:\n{error}')
            else:
                QMessageBox.information(self, '运行结果', f'运行成功:\n{output}')
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'运行失败: {str(e)}')
    
    def update_file_browser(self, directory):
        """更新文件浏览器"""
        self.file_browser.clear()
        
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path) and item.endswith('.nova'):
                    self.file_browser.addItem(item)
        except Exception as e:
            pass

def main():
    """主函数"""
    app = QApplication(sys.argv)
    ide = NovaIDE()
    ide.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()