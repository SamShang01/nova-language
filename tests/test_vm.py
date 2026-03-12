"""
Nova语言虚拟机测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from nova.vm.machine import VirtualMachine
from nova.vm.instructions import LOAD_CONST, STORE_NAME, LOAD_NAME, BINARY_ADD, RETURN_VALUE

class TestVirtualMachine(unittest.TestCase):
    """
    虚拟机测试类
    """
    
    def test_load_and_run(self):
        """
        测试加载和运行指令
        """
        vm = VirtualMachine()
        instructions = [
            LOAD_CONST(1),
            STORE_NAME("x"),
            LOAD_CONST(2),
            STORE_NAME("y"),
            LOAD_NAME("x"),
            LOAD_NAME("y"),
            BINARY_ADD(),
            RETURN_VALUE(),
        ]
        
        vm.load(instructions)
        result = vm.run()
        
        self.assertEqual(result, 3)
    
    def test_execute(self):
        """
        测试执行指令序列
        """
        vm = VirtualMachine()
        instructions = [
            LOAD_CONST(42),
            RETURN_VALUE(),
        ]
        
        result = vm.execute(instructions)
        
        self.assertEqual(result, 42)
    
    def test_push_and_pop(self):
        """
        测试压栈和出栈
        """
        vm = VirtualMachine()
        vm.push(1)
        vm.push(2)
        
        self.assertEqual(vm.pop(), 2)
        self.assertEqual(vm.pop(), 1)
    
    def test_peek(self):
        """
        测试查看栈顶值
        """
        vm = VirtualMachine()
        vm.push(42)
        
        self.assertEqual(vm.peek(), 42)
        self.assertEqual(len(vm.stack), 1)  # 栈大小不变
    
    def test_set_and_get_global(self):
        """
        测试设置和获取全局变量
        """
        vm = VirtualMachine()
        vm.set_global("x", 10)
        
        self.assertEqual(vm.get_global("x"), 10)
    
    def test_clear(self):
        """
        测试清空虚拟机状态
        """
        vm = VirtualMachine()
        vm.push(1)
        vm.set_global("x", 10)
        
        vm.clear()
        
        self.assertEqual(len(vm.stack), 0)
        self.assertIsNone(vm.get_global("x"))
    
    def test_get_state(self):
        """
        测试获取虚拟机状态
        """
        vm = VirtualMachine()
        vm.push(42)
        vm.set_global("x", 10)
        
        state = vm.get_state()
        
        self.assertEqual(state["stack"], [42])
        self.assertEqual(state["environment"]["x"], 10)
        self.assertEqual(state["pc"], 0)
        self.assertFalse(state["running"])

if __name__ == '__main__':
    unittest.main()
