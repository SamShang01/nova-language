# Nova Language

Nova编程语言 - 一个现代、高性能的编程语言，支持LLVM JIT编译

## 特性

- **完整的编译器系统**：词法分析、语法分析、语义分析、代码生成
- **LLVM JIT编译**：可选的LLVM后端，提供更高的执行性能
- **包管理系统**：支持包的安装、卸载和更新
- **并行编译**：多线程编译支持，可选GPU加速
- **标准库**：STL（标准模板库）和丰富的内置函数
- **开发工具**：VS Code插件、Nova IDE、增强的REPL

## 安装

### 使用pip安装

```bash
pip install nova-language
```

### 从源码安装

```bash
git clone https://github.com/SamShang01/nova-language.git
cd nova-language
python setup.py install
```

## 快速开始

创建一个 `hello.nova` 文件：

```nova
fn main() {
    println("Hello, Nova!");
}
```

运行程序：

```bash
nova run hello.nova
```

## 命令行工具

- `nova run <file>` - 运行Nova程序
- `nova compile <file>` - 编译Nova程序
- `nova repl` - 启动交互式REPL环境
- `nova install <package>` - 安装包
- `nova uninstall <package>` - 卸载包
- `nova update <package>` - 更新包

## 文档

- [语言说明书](https://github.com/SamShang01/nova-language/blob/main/语言说明书.md)
- [开发文档](https://github.com/SamShang01/nova-language/blob/main/DEVELOPMENT_TOOLS.md)
- [项目总结](https://github.com/SamShang01/nova-language/blob/main/PROJECT_SUMMARY.md)

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

MIT License
