# Nova 语言版本 0.15.1

## 版本信息

- **版本号**: 0.15.1
- **发布日期**: 2026-03-05
- **状态**: ✅ 已完成

## 主要修复

### 1. Vector实现简化

**问题**: NovaVector类的实现过于复杂，remove()方法中存在递归调用导致栈溢出。

**修复**:
- 使用Python列表作为底层存储，简化NovaVector类实现
- 修复remove()方法中的递归调用问题，改为使用list.remove()

### 2. 关键Bug修复

#### 数组len方法修复
- **问题**: 数组类型的len方法调用失败
- **修复**: 在generator.py中添加了对数组类型len方法的特殊处理

#### COMPARE_EQ指令修复
- **问题**: COMPARE_EQ指令处理NotImplemented返回值时出错
- **修复**: 正确处理NotImplemented返回值的情况

#### 跳转指令标签映射修复
- **问题**: JUMP、JUMP_IF_TRUE、JUMP_IF_FALSE指令直接将标签名称赋值给pc计数器，而pc应该是整数索引
- **修复**: 
  - 在VirtualMachine.load方法中添加代码，建立标签到指令索引的映射
  - 修改跳转指令的实现，使其能够使用映射将标签名称转换为指令索引

### 3. 代码清理

- 删除了analyzer.py中未使用的_parse_stl_files()方法
- 删除了analyzer.py中未使用的_initialize_array_type()方法

## 测试结果

所有关键测试用例均通过：

- ✅ **test_object_compare.nova** - 对象比较测试通过
  - 输出: "Bob is older than John"
  
- ✅ **test_multiple_trait_constraints.nova** - 多Trait约束测试通过
  - 输出: "Multiple trait constraints test passed!"
  
- ✅ **test_vector_traits.nova** - Vector Trait测试通过
  - Sequence Trait: first/last 测试通过
  - Collection Trait: add/remove/toArray 测试通过
  - Sized Trait: size 测试通过

## 版本存档

本版本的完整存档位于 `versions/0.15.1/` 目录，包含：

- 完整的 `src` 目录（所有编译器源代码）
- `version.py` 文件（版本号信息）
- `CHANGELOG.md` 文件（本版本的变更记录）
- `README.md` 文件（版本说明）

## 向后兼容性

本版本与 0.15.0 版本完全向后兼容。所有 0.15.0 版本的代码都可以在 0.15.1 版本中正常运行。

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues
- 项目文档

---

**Nova 语言团队**
**2026-03-05**
