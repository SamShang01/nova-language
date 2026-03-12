# Nova 语言版本 0.15.0

## 版本信息

- **版本号**: 0.15.0
- **发布日期**: 2026-03-04
- **状态**: ✅ 已完成

## 主要功能

### 1. 泛型Trait系统

本版本实现了完整的泛型Trait系统，包括：

- **Trait定义**：支持泛型Trait定义，如 `trait Display<T>`
- **Impl块**：支持为特定类型实现Trait，如 `impl Display<T> for Array<T>`
- **Trait约束检查**：确保类型实现所需方法
- **Trait方法调用**：支持Trait方法的动态调用

### 2. 编译器优化系统

本版本引入了完整的编译器优化系统，包括：

#### 优化级别支持

- `-O0`：无优化（默认）
- `-O1`：部分优化（常量折叠）
- `-O2`：高度优化（常量折叠 + 死代码消除）
- `-O3`：极度优化（常量折叠 + 死代码消除 + 尾递归优化）

#### 优化Pass实现

1. **ConstantFolding（常量折叠）**
   - 在编译时计算常量表达式
   - 支持算术运算：+、-、*、/、%
   - 自动类型推断（int/float）

2. **DeadCodeElimination（死代码消除）**
   - 移除永远不会执行的代码
   - 清理无用的分支和语句

3. **TailRecursionOptimization（尾递归优化）**
   - 检测尾递归函数
   - 将尾递归转换为迭代
   - 避免栈溢出

### 3. 命令行接口增强

所有主要命令都支持优化级别参数：

- **repl命令**：`python script.py repl -O1`
- **run命令**：`python script.py run program.nova -O2`
- **compile命令**：`python script.py compile program.nova -O3`

## 使用示例

### 基本使用

```bash
# 运行Nova程序（无优化）
python script.py run program.nova

# 运行Nova程序（使用O1优化）
python script.py run program.nova -O1

# 运行Nova程序（使用O2优化）
python script.py run program.nova -O2

# 运行Nova程序（使用O3优化）
python script.py run program.nova -O3
```

### 泛型Trait示例

```nova
trait Display<T> {
    fn toString() -> string;
}

impl Display<int> for int {
    fn toString() -> string {
        return "int";
    }
}

fn main() {
    let x = 42;
    print(x.toString());
}
```

### 优化效果示例

```nova
fn main() {
    let result = 2 + 3 * 4;
    print(result);
}
```

使用 `-O1` 优化后，表达式 `2 + 3 * 4` 会在编译时被计算为 `14`，减少运行时计算开销。

## 测试

本版本包含以下测试用例：

- `test_0_15_0_simple.nova`：泛型Trait功能测试
- `test_constant_folding.nova`：优化功能测试

所有测试用例均通过验证。

## 版本存档

本版本的完整存档位于 `versions/0.15.0/` 目录，包含：

- 完整的 `src` 目录（所有编译器源代码）
- `version.py` 文件（版本号信息）
- `CHANGELOG.md` 文件（本版本的变更记录）
- `README.md` 文件（版本说明）

## 向后兼容性

本版本与 0.14.0 版本完全向后兼容。所有 0.14.0 版本的代码都可以在 0.15.0 版本中正常运行。

## 已知问题

目前存在以下已知问题：

1. 泛型Trait的运行时方法调用存在一些限制，需要进一步优化
2. 尾递归优化的实现目前较为基础，需要进一步完善

## 下一步计划

未来的版本计划包括：

1. 完善泛型Trait的运行时支持
2. 增强尾递归优化的实现
3. 添加更多的优化Pass
4. 改进错误处理和诊断信息

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues
- 项目文档

---

**Nova 语言团队**
**2026-03-04**
