# Nova 语言更新日志（0.3.0存档）

## [0.3.0] - 2026-02-13
### 新增
- 扩展标准库核心函数，添加大量实用函数
  - 列表操作：list, append, remove, pop, sort, reverse, slice
  - 字典操作：dict, keys, values, items
  - 容器操作：contains
  - 函数式编程：map_func, filter_func, reduce_func, zip_func
  - 逻辑检查：any_func, all_func
  - 字符转换：chr_func, ord_func, hex_func, oct_func, bin_func
  - 数学运算：pow_func, divmod_func
  - 对象操作：hash_func, id_func
- 实现 `__future__.nova` 文件支持
- 添加 `from __future__ import ...` 语法支持，类似 Python 的 `__future__` 模块
- 支持双下划线（__）作为特殊标识符
- 性能优化
  - 优化虚拟机指令执行循环，减少条件检查开销
  - 优化内存管理器，减少排序和遍历开销
  - 改进内存分配策略，批量处理空闲列表

### 修复
- 修复标准库函数命名冲突问题
- 优化内存管理器的地址有效性检查

### 变更
- 更新版本号到 0.3.0
- 扩展标准库功能，提供更丰富的内置函数
