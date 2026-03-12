# Nova 语言版本 0.3.0 存档

## 版本信息
- 版本号：0.3.0
- 发布日期：2026-02-13

## 主要更新

### 新增功能
1. **扩展标准库核心函数**
   - 列表操作：list, append, remove, pop, sort, reverse, slice
   - 字典操作：dict, keys, values, items
   - 容器操作：contains
   - 函数式编程：map_func, filter_func, reduce_func, zip_func
   - 逻辑检查：any_func, all_func
   - 字符转换：chr_func, ord_func, hex_func, oct_func, bin_func
   - 数学运算：pow_func, divmod_func
   - 对象操作：hash_func, id_func

2. **`__future__.nova` 文件支持**
   - 实现 `__future__.nova` 文件
   - 添加 `from __future__ import ...` 语法支持
   - 类似 Python 的 `__future__` 模块

3. **词法分析器增强**
   - 支持双下划线（__）作为特殊标识符
   - 添加 DOUBLE_UNDERSCORE token 类型

4. **语法分析器增强**
   - 支持解析 `from __future__ import ...` 语句
   - 将 `from __future__ import ...` 转换为 FeatureStatement 节点

### 性能优化
1. **虚拟机优化**
   - 优化指令执行循环，减少条件检查开销
   - 预加载跳转指令类型，避免每次循环都导入

2. **内存管理器优化**
   - 减少排序和遍历开销
   - 改进内存分配策略，批量处理空闲列表
   - 优化地址有效性检查方法

### 修复的问题
1. 修复标准库函数命名冲突问题
2. 优化内存管理器的地址有效性检查

### 变更内容
1. 更新版本号到 0.3.0
2. 扩展标准库功能，提供更丰富的内置函数

## 版本存档文件
- version.py：版本信息和版本判断函数
- README.md：本文件，记录版本详细信息
