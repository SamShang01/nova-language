# Nova 语言开发工具集

本文档总结了Nova语言的开发工具集，包括VS Code插件、Nova IDE和REPL。

## VS Code 插件

### 功能特性

- **语法高亮**：支持Nova语言的关键字、运算符、字符串、数字等
- **代码片段**：提供函数、结构体、条件语句等常用代码模板
- **代码运行**：直接在VS Code中运行Nova代码
- **代码格式化**：自动格式化Nova代码
- **快捷键**：F5运行代码，Shift+Alt+F格式化代码

### 安装方式

1. 打开VS Code
2. 点击扩展图标
3. 点击"从VSIX安装"
4. 选择`nova-language-0.1.0.vsix`文件

### 使用说明

1. 创建或打开`.nova`文件
2. 编写Nova代码
3. 使用代码片段（如`func`、`struct`、`if`等）
4. 按F5运行代码
5. 按Shift+Alt+F格式化代码

## Nova IDE

### 功能特性

- **基本窗口**：主窗口、文件浏览器、编辑器标签页
- **语法高亮**：内置Nova语言语法高亮
- **文件操作**：新建、打开、保存、另存为
- **代码运行**：直接运行Nova代码并显示结果
- **菜单栏**：完整的文件、编辑、运行菜单

### 安装方式

```bash
cd nova-ide
pip install -r requirements.txt
pip install -e .
```

### 使用说明

1. 运行 `nova-ide` 命令启动IDE
2. 使用菜单栏或快捷键进行文件操作
3. 编写Nova代码
4. 点击"运行"菜单或按F5运行代码

## REPL

### 功能特性

- **命令系统**：支持多种内置命令
- **代码执行**：直接执行Nova代码
- **变量管理**：查看和管理变量
- **类型信息**：显示变量和函数的类型

### 启动方式

```bash
nova repl
```

### 常用命令

- `:help` - 显示帮助信息
- `:clear` - 清除所有变量和函数
- `:vars` - 显示所有变量
- `:type <name>` - 显示变量或函数的类型信息
- `:import <module>` - 导入模块
- `:multiline` - 切换多行模式
- `quit`/`exit` - 退出REPL

## 示例代码

```nova
// 变量声明
let message: string = "Hello, Nova!";
let count: int = 42;

// 函数定义
func greet(name: string) -> string {
    return "Hello, " + name + "!";
}

// 调用函数
print(greet("World"));
print(message);
```

## 开发计划

### 已完成
- ✅ VS Code插件基础功能
- ✅ Nova IDE基础功能
- ✅ REPL功能分析

### 待完成
- ⬜ VS Code插件语言服务器（智能提示）
- ⬜ Nova IDE调试功能
- ⬜ Nova IDE项目管理
- ⬜ 更多代码片段和语法高亮

## 技术栈

- **VS Code插件**：TypeScript, VS Code Extension API
- **Nova IDE**：Python, PyQt5, QScintilla
- **REPL**：Python

## 贡献

欢迎贡献代码和提出建议！请在GitHub上提交Issue或Pull Request。

## 许可证

MIT License