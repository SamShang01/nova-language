# Nova 语言更新日志（0.4.0存档）

## [0.4.0] - 2026-02-13
### 新增
- 实现编译功能
  - 添加编译器模块，支持将Nova代码编译为Python可执行文件
  - 添加编译器模块，支持将Nova代码编译为独立可执行文件
  - 在script.py中添加compile子命令，支持命令行编译
  - 支持两种编译格式：python和executable
- 实现GUI功能
  - 添加GUI标准库，提供类似Python tkinter的GUI功能
  - 实现Widget窗口组件，支持创建GUI窗口
  - 实现Button按钮组件，支持点击回调
  - 实现Label标签组件，用于显示文本
  - 实现Entry输入框组件，支持用户输入
  - 实现Text文本框组件，支持多行文本
  - 实现Canvas画布组件，支持绘制图形
  - 实现Menu菜单组件，支持创建菜单
- 添加GUI测试用例
  - 测试窗口组件的创建和子组件添加
  - 测试按钮组件的创建和回调函数
  - 测试标签组件的创建
  - 测试输入框组件的获取和设置
  - 测试文本框组件的获取、设置和追加
  - 测试画布组件的图形绘制
  - 测试菜单组件的菜单项添加
- 扩展标准库测试用例
  - 添加扩展标准库测试文件test_extended_stdlib.py
  - 测试数学函数：abs, max, min, sum, round, pow_func, divmod_func
  - 测试类型函数：type, isinstance
  - 测试转换函数：to_str, to_int, to_float
  - 测试容器函数：contains
  - 测试列表函数：list, append, remove, pop, sort, reverse, slice
  - 测试字典函数：dict, keys, values, items
  - 测试函数式编程函数：map_func, filter_func, reduce_func, zip_func
  - 测试逻辑函数：any_func, all_func
  - 测试字符函数：chr_func, ord_func, hex_func, oct_func, bin_func
  - 测试对象函数：hash_func, id_func

### 修复
- 修复标准库函数递归调用问题
  - 修复list函数递归调用自己，使用builtins.list
  - 修复dict函数递归调用自己，使用builtins.dict
  - 修复keys函数使用list递归，使用builtins.list
  - 修复values函数使用list递归，使用builtins.list
  - 修复items函数使用list递归，使用builtins.list
  - 修复sort函数使用sorted递归，使用builtins.sorted
  - 修复reverse函数使用list和reversed递归，使用builtins.list和builtins.reversed
  - 修复map_func函数使用map和list递归，使用builtins.map和builtins.list
  - 修复filter_func函数使用filter和list递归，使用builtins.filter和builtins.list
  - 修复zip_func函数使用zip和list递归，使用builtins.zip和builtins.list
- 修复Float类初始化递归问题，使用builtins.float
- 修复String类初始化递归问题，使用builtins.str
- 修复Int类初始化递归问题，使用builtins.int
- 修复测试用例中的断言失败，正确处理返回的Int对象

### 变更
- 更新版本号到0.4.0
- 在标准库中添加GUI模块，版本要求>=0.4.0
- 更新标准库版本提示信息
