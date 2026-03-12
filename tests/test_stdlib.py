"""
Nova语言标准库测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import builtins
from nova.stdlib.core.types import Int, Float, String, Bool, Char
from nova.stdlib.core.functions import print as nova_print, len as nova_len, input
from nova.stdlib.collections.list import List
from nova.stdlib.collections.dict import Dict
from nova.stdlib.collections.set import Set
from nova.stdlib.io.file import open, File
from nova.stdlib.io.streams import stdin, stdout, stderr
from nova.stdlib.asynchronous.future import Future
from nova.stdlib.asynchronous.task import Task, create_task, async_func, await_

class TestStdlib(unittest.TestCase):
    """
    标准库测试类
    """
    
    def test_core_types(self):
        """
        测试核心类型
        """
        # 测试整数
        i = Int(42)
        self.assertEqual(i.value, 42)
        self.assertEqual(i.__add__(Int(10)).value, 52)
        
        # 测试浮点数
        f = Float(3.14)
        self.assertEqual(f.value, 3.14)
        
        # 测试字符串
        s = String("hello")
        self.assertEqual(s.value, "hello")
        
        # 测试布尔值
        b = Bool(True)
        self.assertEqual(b.value, True)
        
        # 测试字符
        c = Char('a')
        self.assertEqual(c.value, 'a')
    
    def test_core_functions(self):
        """
        测试核心函数
        """
        # 测试len函数
        s = "hello"
        result = nova_len(s)
        self.assertEqual(result.value, 5)
        
        # 测试print函数
        # 这里只是测试函数存在，不实际输出
        self.assertIsNotNone(nova_print)
        
        # 测试input函数
        # 这里只是测试函数存在，不实际输入
        self.assertIsNotNone(input)
    
    def test_collections(self):
        """
        测试集合类型
        """
        # 测试列表
        lst = List([1, 2, 3])
        self.assertEqual(builtins.len(lst), 3)
        lst.append(4)
        self.assertEqual(builtins.len(lst), 4)
        self.assertEqual(lst[0], 1)
        
        # 测试字典
        d = Dict({"a": 1, "b": 2})
        self.assertEqual(builtins.len(d), 2)
        d["c"] = 3
        self.assertEqual(builtins.len(d), 3)
        self.assertEqual(d["a"], 1)
        
        # 测试集合
        s = Set([1, 2, 3])
        self.assertEqual(builtins.len(s), 3)
        s.add(4)
        self.assertEqual(builtins.len(s), 4)
        self.assertTrue(1 in s)
    
    def test_io(self):
        """
        测试IO模块
        """
        # 测试标准流
        self.assertIsNotNone(stdin)
        self.assertIsNotNone(stdout)
        self.assertIsNotNone(stderr)
        
        # 测试File类
        self.assertIsNotNone(File)
        
        # 测试open函数
        self.assertIsNotNone(open)
    
    def test_async(self):
        """
        测试异步模块
        """
        # 测试Future
        future = Future()
        future.set_result(42)
        self.assertEqual(future.result(), 42)
        
        # 测试Task
        def simple_coroutine():
            yield 42
        
        task = Task(simple_coroutine())
        task.start()
        
        # 直接检查任务状态
        self.assertTrue(task.done())
        
        # 测试创建任务
        self.assertIsNotNone(create_task)
        
        # 测试异步装饰器
        self.assertIsNotNone(async_func)
        
        # 测试await函数
        self.assertIsNotNone(await_)

if __name__ == '__main__':
    unittest.main()
