# Changelog - Nova 0.14.0

## [0.14.0] - 2026-03-03

### 新增功能

#### 1. 新增容器类型
- **Deque（双端队列）**
  - 支持 O(1) 时间复杂度的两端插入和删除
  - 提供 pushFront、pushBack、popFront、popBack 操作
  - 循环数组实现，高效内存利用

- **Heap（堆/优先队列）**
  - 支持最大堆和最小堆两种模式
  - 提供 push、pop、top 操作
  - 上浮和下沉操作保持堆性质

- **Trie（前缀树）**
  - 高效存储和检索字符串键值对
  - 支持前缀搜索和自动补全
  - 提供 insert、search、contains、startsWith 操作

#### 2. 性能优化
- **高级排序算法**
  - 快速排序：平均 O(n log n) 时间复杂度
  - 归并排序：稳定排序，O(n log n) 时间复杂度
  - 堆排序：原地排序，O(n log n) 时间复杂度

#### 3. 新增算法
- **transform**：对范围内的每个元素应用函数
- **accumulate**：计算范围内的累加和
- **inner_product**：计算两个范围的内积
- **adjacent_difference**：计算相邻元素的差值
- **partial_sum**：计算部分和

### 测试
- 新增基础测试套件 test_0_14_0_basic.nova
- 验证数值计算、条件语句、循环、字符串、函数调用
- 所有测试用例均通过

### 版本信息
- 版本号：0.14.0
- 发布日期：2026-03-03
- 版本名称：Enhanced STL Release
