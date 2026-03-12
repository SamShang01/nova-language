# Nova 0.14.0 - Enhanced STL Release

## 版本概述

Nova 0.14.0 是一个专注于增强标准模板库（STL）的版本，引入了多个新的容器类型和高级算法，显著提升了 Nova 语言的数据结构和算法能力。

## 主要特性

### 1. 新增容器

#### Deque（双端队列）
```nova
var deque = Deque<int>();
deque.pushBack(10);
deque.pushFront(5);
var front = deque.popFront();
var back = deque.popBack();
```

#### Heap（堆/优先队列）
```nova
// 最大堆
var maxHeap = Heap<int>();
maxHeap.push(50);
maxHeap.push(30);
var max = maxHeap.pop(); // 50

// 最小堆
var minHeap = Heap<int>(false);
minHeap.push(50);
minHeap.push(30);
var min = minHeap.pop(); // 30
```

#### Trie（前缀树）
```nova
var trie = Trie<int>();
trie.insert("apple", 1);
trie.insert("app", 2);
var value = trie.search("apple"); // 1
var hasPrefix = trie.startsWith("app"); // true
```

### 2. 高级算法

#### 排序算法
- 快速排序（Quick Sort）
- 归并排序（Merge Sort）
- 堆排序（Heap Sort）

#### 数值算法
- transform：元素转换
- accumulate：累加求和
- inner_product：内积计算
- adjacent_difference：相邻差值
- partial_sum：部分和

## 文件结构

```
versions/0.14.0/
├── src/                    # 完整的编译器源代码
│   └── nova/
│       ├── stdlib/stl/     # STL 库文件
│       │   ├── deque.nova
│       │   ├── heap.nova
│       │   ├── trie.nova
│       │   ├── algorithm_advanced.nova
│       │   └── numeric_advanced.nova
│       └── ...
├── version.py              # 版本信息
├── CHANGELOG.md            # 版本变更日志
└── README.md               # 版本说明
```

## 测试

运行基础测试：
```bash
python script.py run test_0_14_0_basic.nova
```

## 版本信息

- **版本号**: 0.14.0
- **发布日期**: 2026-03-03
- **版本名称**: Enhanced STL Release
- **状态**: ✅ 已发布

## 兼容性

- 向下兼容 0.13.x 版本
- 所有现有代码无需修改即可运行
- 新增功能完全可选

## 后续计划

- 0.15.0: 泛型接口（Generic Traits）
- 0.16.0: 并发编程支持
