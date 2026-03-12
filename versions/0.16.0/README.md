# Nova 语言 0.16.0 版本

## 版本信息

- **版本号**: 0.16.0
- **发布日期**: 2026-03-06
- **版本类型**: 功能更新版本

## 主要特性

### 1. 基于LLVM的JIT编译器
Nova 0.16.0引入了基于LLVM的JIT编译器，通过llvmlite库实现即时编译，显著提升代码执行性能。

**主要功能**:
- 编译到LLVM IR中间表示
- JIT即时编译执行
- 支持多种优化级别

### 2. 包管理系统
全新的包管理系统，支持包的安装、卸载、更新和管理。

**主要功能**:
- 包安装和版本管理
- 包索引和依赖跟踪
- 命令行接口支持

### 3. 并行编译能力
增强的并行编译能力，支持多线程和GPU加速。

**主要功能**:
- 多线程并行编译
- GPU加速支持
- 增量编译优化

### 4. 完善的标准库
标准库功能大幅增强，提供更多实用函数和数据结构。

**主要模块**:
- 核心模块：基础函数和类型
- 字符串模块：字符串处理函数
- 数学模块：数学运算函数
- 集合模块：列表、字典、集合等

## 安装说明

### 系统要求
- Python 3.8+
- Windows/Linux/macOS

### 依赖安装
```bash
pip install llvmlite
```

### 安装Nova
```bash
python setup.py install
```

## 使用说明

### 运行Nova程序
```bash
nova run program.nova
```

### 使用包管理
```bash
nova package install <package_name>
nova package uninstall <package_name>
nova package list
```

### 使用并行编译
```bash
nova compile program.nova --parallel --gpu
```

## 示例代码

### Hello World
```nova
func main() {
    print("Hello, Nova!");
}
```

### 使用标准库
```nova
import string;
import math;

func main() {
    let s = "hello world";
    print(string.to_upper(s));
    print(math.sqrt(16));
}
```

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。
