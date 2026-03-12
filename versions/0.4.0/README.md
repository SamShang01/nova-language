# Nova 语言版本 0.4.0 存档

## 版本信息
- 版本号：0.4.0
- 发布日期：2026-02-13

## 主要更新

### 新增功能
1. **编译功能**
   - 添加编译器模块，支持将Nova代码编译为Python可执行文件
   - 添加编译器模块，支持将Nova代码编译为独立可执行文件
   - 在script.py中添加compile子命令，支持命令行编译
   - 支持两种编译格式：python和executable

2. **GUI功能**
   - 添加GUI标准库，提供类似Python tkinter的GUI功能
   - 实现Widget窗口组件，支持创建GUI窗口
   - 实现Button按钮组件，支持点击回调
   - 实现Label标签组件，用于显示文本
   - 实现Entry输入框组件，支持用户输入
   - 实现Text文本框组件，支持多行文本
   - 实现Canvas画布组件，支持绘制图形
   - 实现Menu菜单组件，支持创建菜单

3. **测试用例扩展**
   - 添加GUI测试用例，测试所有GUI组件
   - 扩展标准库测试用例，测试所有新增函数
   - 修复测试用例中的断言失败问题

### 修复的问题
1. **标准库函数递归调用问题**
   - 修复list函数递归调用自己，使用builtins.list
   - 修复dict函数递归调用自己，使用builtins.dict
   - 修复keys、values、items函数使用list递归，使用builtins.list
   - 修复sort函数使用sorted递归，使用builtins.sorted
   - 修复reverse函数使用list和reversed递归，使用builtins.list和builtins.reversed
   - 修复map_func、filter_func、zip_func函数递归，使用builtins版本

2. **类型初始化递归问题**
   - 修复Float类初始化递归问题，使用builtins.float
   - 修复String类初始化递归问题，使用builtins.str
   - 修复Int类初始化递归问题，使用builtins.int

3. **测试用例断言问题**
   - 修复测试用例中的断言失败，正确处理返回的Int对象

### 变更内容
1. 更新版本号到0.4.0
2. 在标准库中添加GUI模块，版本要求>=0.4.0
3. 更新标准库版本提示信息

## 版本存档文件
- version.py：版本信息和版本判断函数
- README.md：本文件，记录版本详细信息
