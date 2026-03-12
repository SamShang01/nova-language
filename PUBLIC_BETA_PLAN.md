# Nova 语言公测计划表

## 当前状态概览

- **版本**: 0.16.0
- **测试结果**: 114个测试，1个失败，24个错误
- **主要问题**: 词法分析器、语义分析器、Trait系统

---

## 阶段一：核心功能修复（优先级：高）

### 任务 1.1：修复词法分析器测试失败
**问题描述**: `test_scan_operators` 测试失败，运算符类型不匹配
- 预期: `TokenType.AND` 和 `TokenType.OR`
- 实际: `TokenType.AMPERSAND` 和 `TokenType.PIPE`

**执行命令**:
```powershell
# 检查词法分析器运算符定义
python -c "from nova.compiler.lexer.tokens import TokenType; print([t for t in dir(TokenType) if 'AND' in t or 'OR' in t or 'AMPERSAND' in t or 'PIPE' in t])"

# 运行词法分析器测试
python -m unittest tests.test_lexer.TestLexer.test_scan_operators -v
```

**修复文件**: `e:\nova\src\nova\compiler\lexer\tokens.py` 或 `e:\nova\src\nova\compiler\lexer\scanner.py`

---

### 任务 1.2：修复语义分析器返回类型检查
**问题描述**: `test_analyze_simple_program` 测试失败，返回类型不匹配
- 错误: `Return type mismatch: expected unit, got int`

**执行命令**:
```powershell
# 运行语义分析器测试
python -m unittest tests.test_semantic.TestSemanticAnalyzer.test_analyze_simple_program -v
```

**修复文件**: `e:\nova\src\nova\compiler\semantic\analyzer.py`

---

### 任务 1.3：修复Trait系统未定义标识符错误
**问题描述**: `test_multiple_trait_constraints` 测试失败，未定义标识符 'value'

**执行命令**:
```powershell
# 运行Trait测试
python -m unittest tests.test_traits.TestTraits.test_multiple_trait_constraints -v
```

**修复文件**: `e:\nova\src\nova\compiler\semantic\analyzer.py`

---

## 阶段二：功能完善（优先级：中）

### 任务 2.1：完善标准库函数
**目标**: 确保所有标准库函数正常工作

**执行命令**:
```powershell
# 运行标准库测试
python -m unittest tests.test_stdlib -v

# 测试字符串模块
python -m unittest tests.test_string_module -v

# 测试数学模块
python -m unittest tests.test_math_module -v
```

**修复文件**:
- `e:\nova\src\nova\stdlib\core\functions.py`
- `e:\nova\src\nova\stdlib\string\functions.py`
- `e:\nova\src\nova\stdlib\math\functions.py`

---

### 任务 2.2：完善泛型系统
**目标**: 确保泛型结构体和函数正常工作

**执行命令**:
```powershell
# 运行泛型结构体测试
python -m unittest tests.test_generic_structs -v

# 运行泛型函数测试
python -m unittest tests.test_generic_functions -v
```

**修复文件**: `e:\nova\src\nova\compiler\semantic\analyzer.py`

---

### 任务 2.3：完善虚拟机
**目标**: 确保虚拟机指令执行正确

**执行命令**:
```powershell
# 运行虚拟机测试
python -m unittest tests.test_vm -v
```

**修复文件**: `e:\nova\src\nova\vm\machine.py`

---

## 阶段三：性能优化（优先级：中）

### 任务 3.1：启用LLVM JIT编译器
**目标**: 确保LLVM JIT编译器正常工作

**执行命令**:
```powershell
# 测试LLVM编译器
python -c "from nova.compiler.llvm_compiler import LLVMCompiler; print('LLVM OK')"

# 安装llvmlite（如果未安装）
pip install llvmlite
```

**修复文件**: `e:\nova\src\nova\compiler\llvm_compiler.py`

---

### 任务 3.2：启用并行编译
**目标**: 确保并行编译功能正常工作

**执行命令**:
```powershell
# 测试并行编译
python -c "from nova.compiler.parallel import ParallelCompiler; print('Parallel OK')"
```

**修复文件**: `e:\nova\src\nova\compiler\parallel.py`

---

## 阶段四：文档和测试（优先级：低）

### 任务 4.1：完善测试覆盖率
**目标**: 确保所有功能都有测试覆盖

**执行命令**:
```powershell
# 安装pytest和覆盖率工具
pip install pytest pytest-cov

# 运行测试并生成覆盖率报告
python -m pytest tests/ --cov=nova --cov-report=html
```

---

### 任务 4.2：更新文档
**目标**: 确保文档与代码同步

**执行命令**:
```powershell
# 检查语言说明书是否存在
python -c "import os; print('Manual exists:', os.path.exists('NOVA_LANGUAGE_MANUAL.md'))"

# 检查CHANGELOG是否更新
python -c "import os; print('Changelog exists:', os.path.exists('CHANGELOG.md'))"
```

---

## 阶段五：发布准备（优先级：高）

### 任务 5.1：版本存档
**目标**: 创建完整的版本存档

**执行命令**:
```powershell
# 创建版本目录
mkdir versions\0.16.0

# 复制源代码
xcopy /E /I src versions\0.16.0\src

# 复制版本文件
copy src\nova\version.py versions\0.16.0\

# 复制文档
copy CHANGELOG.md versions\0.16.0\
copy README.md versions\0.16.0\
```

---

### 任务 5.2：构建和安装
**目标**: 确保包可以正确构建和安装

**执行命令**:
```powershell
# 清理旧的构建文件
rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q src\nova_language.egg-info

# 构建包
python setup.py build

# 安装包
python setup.py install

# 测试安装
python -m nova --version
python -m nova.repl
```

---

### 任务 5.3：最终测试
**目标**: 运行所有测试，确保没有错误

**执行命令**:
```powershell
# 运行所有测试
python -m unittest discover -s tests -v

# 测试REPL
echo "print('Hello, Nova!');" | python -m nova.repl

# 测试编译器
echo "let x = 10; print(x);" | python -m nova.cli run
```

---

## 公测检查清单

### 功能检查
- [ ] REPL 正常启动和运行
- [ ] 编译器可以编译 Nova 代码
- [ ] 虚拟机可以执行编译后的代码
- [ ] 标准库函数正常工作
- [ ] 泛型系统正常工作
- [ ] Trait 系统正常工作

### 性能检查
- [ ] LLVM JIT 编译器可用
- [ ] 并行编译可用
- [ ] 增量编译可用

### 文档检查
- [ ] 语言说明书完整
- [ ] CHANGELOG 更新
- [ ] README 更新

### 测试检查
- [ ] 所有测试通过（0 错误，0 失败）
- [ ] 测试覆盖率 > 80%

### 发布检查
- [ ] 版本存档完整
- [ ] 包可以正确安装
- [ ] 命令行工具可用

---

## 预计时间

| 阶段 | 预计时间 | 负责人 |
|------|----------|--------|
| 阶段一：核心功能修复 | 2-3天 | 开发团队 |
| 阶段二：功能完善 | 2-3天 | 开发团队 |
| 阶段三：性能优化 | 1-2天 | 开发团队 |
| 阶段四：文档和测试 | 1-2天 | 测试团队 |
| 阶段五：发布准备 | 1天 | 运维团队 |

**总计**: 7-11天

---

## 联系方式

如有问题，请联系：
- 项目负责人：[请填写]
- 技术支持：[请填写]
- 测试负责人：[请填写]
