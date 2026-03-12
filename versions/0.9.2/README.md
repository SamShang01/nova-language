# Nova 语言 0.9.2 版本

## 版本信息
- **版本号**: 0.9.2
- **发布日期**: 2026-02-27
- **版本类型**: Bugfix 版本

## 主要修复

### 1. const 常量赋值修复
修复了 `const` 声明的常量可以被重新赋值的问题。

**之前的行为**:
```nova
const x = 12;
x = 13;  // 居然成功了！
```

**现在的行为**:
```nova
const x = 12;
x = 13;  // 错误: Cannot assign to constant 'x'
```

### 2. 延迟运算特性控制
修复了 `DeferredOperations` 特性控制逻辑，使其真正可控。

**未启用特性时**:
```nova
var result = 0.1 + 0.2 - 0.2;
print(str(result));  // 输出: 0.10000000000000003
```

**启用特性时**:
```nova
from __future__ import DeferredOperations;
var result = 0.1 + 0.2 - 0.2;
print(str(result));  // 输出: 0.1
```

## 文件结构
```
versions/0.9.2/
├── src/nova/           # 完整的编译器源代码
├── version.py          # 版本信息
├── CHANGELOG.md        # 版本更新日志
└── README.md           # 版本说明
```

## 安装说明
使用 script.py 安装此版本:
```bash
python script.py install --version=0.9.2
```

## 兼容性
- 与 0.9.x 系列版本兼容
- 建议从 0.9.1 升级到此版本以获得 bugfix
