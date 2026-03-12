# Nova 语言 0.9.2 版本更新日志

## [0.9.2] - 2026-02-27

### 修复
- **const 常量赋值修复**：
  - 修复 `const` 声明的常量可以被重新赋值的问题
  - 现在尝试给 `const` 常量赋值会报错："Cannot assign to constant 'x'"
  - 同时 `let` 声明的不可变变量也不能被重新赋值

- **延迟运算特性控制**：
  - 修复 `DeferredOperations` 特性控制逻辑
  - 未启用特性时：`0.1+0.2-0.2` 返回 `0.10000000000000003`（保留浮点数精度问题）
  - 启用特性时：`from __future__ import DeferredOperations;` + `0.1+0.2-0.2` 返回 `0.1`（优化后）

### 技术细节
- 在语义分析器的 `visit_BinaryExpression` 方法中添加了对常量赋值的检查
- 修改了 `_evaluate_constant_expression` 方法，根据 `DeferredOperations` 特性状态决定计算方式
- 修复了 `Double.__str__()` 方法的无限递归问题
