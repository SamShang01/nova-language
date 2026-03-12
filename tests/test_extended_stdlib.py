"""
Nova语言扩展标准库测试
"""

import unittest
import sys
import os

# 添加src目录到路径，确保使用本地源代码
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from nova.stdlib.core.types import Int, Float, String
from nova.stdlib.core.functions import (
    abs, max, min, sum, round, type, isinstance,
    to_str, to_int, to_float, list, dict, contains,
    keys, values, items, append, remove, pop, sort,
    reverse, slice, map_func, filter_func, reduce_func,
    zip_func, any_func, all_func, chr_func, ord_func,
    hex_func, oct_func, bin_func, pow_func, divmod_func,
    hash_func, id_func
)

class TestExtendedStdlib(unittest.TestCase):
    """
    扩展标准库测试类
    """
    
    def test_math_functions(self):
        """
        测试数学函数
        """
        # 测试abs
        self.assertEqual(abs(-10).value, 10)
        self.assertEqual(abs(10).value, 10)
        
        # 测试max
        self.assertEqual(max(1, 5, 3, 9, 2).value, 9)
        self.assertEqual(max(-1, -5, -3).value, -1)
        
        # 测试min
        self.assertEqual(min(1, 5, 3, 9, 2).value, 1)
        self.assertEqual(min(-1, -5, -3).value, -5)
        
        # 测试sum
        self.assertEqual(sum([1, 2, 3, 4, 5]).value, 15)
        self.assertEqual(sum([]).value, 0)
        
        # 测试round
        self.assertEqual(round(3.14159, 2), 3.14)
        self.assertEqual(round(3.5), 4)
        
        # 测试pow
        self.assertEqual(pow_func(2, 3).value, 8)
        self.assertEqual(pow_func(2, 3, 5).value, 3)
        
        # 测试divmod
        self.assertEqual(divmod_func(10, 3)[0].value, 3)
        self.assertEqual(divmod_func(10, 3)[1].value, 1)
        self.assertEqual(divmod_func(7, 2)[0].value, 3)
        self.assertEqual(divmod_func(7, 2)[1].value, 1)
    
    def test_type_functions(self):
        """
        测试类型函数
        """
        # 测试type
        self.assertEqual(type(42), "int")
        self.assertEqual(type(3.14), "float")
        self.assertEqual(type("hello"), "str")
        
        # 测试isinstance
        self.assertTrue(isinstance(42, int))
        self.assertFalse(isinstance(42, str))
        self.assertTrue(isinstance("hello", str))
    
    def test_conversion_functions(self):
        """
        测试转换函数
        """
        # 测试to_str
        self.assertEqual(to_str(123).value, "123")
        self.assertEqual(to_str(3.14).value, "3.14")
        
        # 测试to_int
        self.assertEqual(to_int("456").value, 456)
        self.assertEqual(to_int(3.14).value, 3)
        
        # 测试to_float
        self.assertEqual(to_float("78.9"), 78.9)
        self.assertEqual(to_float(42), 42.0)
    
    def test_container_functions(self):
        """
        测试容器函数
        """
        # 测试list
        lst = list(1, 2, 3)
        self.assertEqual(lst, [1, 2, 3])
        
        # 测试dict
        d = dict(a=1, b=2)
        self.assertEqual(d, {"a": 1, "b": 2})
        
        # 测试contains
        self.assertTrue(contains([1, 2, 3], 2))
        self.assertFalse(contains([1, 2, 3], 4))
        self.assertTrue(contains("hello", "ell"))
    
    def test_dict_functions(self):
        """
        测试字典函数
        """
        d = {"a": 1, "b": 2, "c": 3}
        
        # 测试keys
        self.assertEqual(sorted(keys(d)), ["a", "b", "c"])
        
        # 测试values
        self.assertEqual(sorted(values(d)), [1, 2, 3])
        
        # 测试items
        items_list = items(d)
        self.assertEqual(len(items_list), 3)
    
    def test_list_functions(self):
        """
        测试列表函数
        """
        lst = [1, 2, 3]
        
        # 测试append
        append(lst, 4)
        self.assertEqual(lst, [1, 2, 3, 4])
        
        # 测试remove
        remove(lst, 2)
        self.assertEqual(lst, [1, 3, 4])
        
        # 测试pop
        item = pop(lst)
        self.assertEqual(item, 4)
        self.assertEqual(lst, [1, 3])
        
        # 测试sort
        unsorted = [3, 1, 4, 1, 5]
        sorted_lst = sort(unsorted)
        self.assertEqual(sorted_lst, [1, 1, 3, 4, 5])
        
        # 测试reverse
        lst = [1, 2, 3]
        reversed_lst = reverse(lst)
        self.assertEqual(reversed_lst, [3, 2, 1])
        
        # 测试slice
        lst = [1, 2, 3, 4, 5]
        sliced = slice(lst, 1, 4)
        self.assertEqual(sliced, [2, 3, 4])
    
    def test_functional_programming(self):
        """
        测试函数式编程函数
        """
        # 测试map_func
        lst = [1, 2, 3, 4]
        mapped = map_func(lambda x: x * 2, lst)
        self.assertEqual(mapped, [2, 4, 6, 8])
        
        # 测试filter_func
        lst = [1, 2, 3, 4, 5]
        filtered = filter_func(lambda x: x % 2 == 0, lst)
        self.assertEqual(filtered, [2, 4])
        
        # 测试reduce_func
        lst = [1, 2, 3, 4]
        reduced = reduce_func(lambda x, y: x + y, lst)
        self.assertEqual(reduced, 10)
        
        # 测试reduce_func with initial
        reduced = reduce_func(lambda x, y: x + y, lst, 10)
        self.assertEqual(reduced, 20)
        
        # 测试zip_func
        lst1 = [1, 2, 3]
        lst2 = ['a', 'b', 'c']
        zipped = zip_func(lst1, lst2)
        self.assertEqual(zipped, [(1, 'a'), (2, 'b'), (3, 'c')])
    
    def test_logical_functions(self):
        """
        测试逻辑函数
        """
        # 测试any_func
        self.assertTrue(any_func([False, False, True]))
        self.assertFalse(any_func([False, False]))
        
        # 测试all_func
        self.assertTrue(all_func([True, True, True]))
        self.assertFalse(all_func([True, False, True]))
    
    def test_character_functions(self):
        """
        测试字符函数
        """
        # 测试chr_func
        self.assertEqual(chr_func(65).value, "A")
        self.assertEqual(chr_func(97).value, "a")
        
        # 测试ord_func
        self.assertEqual(ord_func("A").value, 65)
        self.assertEqual(ord_func("a").value, 97)
        
        # 测试hex_func
        self.assertEqual(hex_func(255).value, "0xff")
        self.assertEqual(hex_func(16).value, "0x10")
        
        # 测试oct_func
        self.assertEqual(oct_func(8).value, "0o10")
        self.assertEqual(oct_func(64).value, "0o100")
        
        # 测试bin_func
        self.assertEqual(bin_func(5).value, "0b101")
        self.assertEqual(bin_func(10).value, "0b1010")
    
    def test_object_functions(self):
        """
        测试对象函数
        """
        # 测试hash_func
        h1 = hash_func(42)
        h2 = hash_func(42)
        self.assertEqual(h1.value, h2.value)
        
        # 测试id_func
        obj = [1, 2, 3]
        obj_id = id_func(obj)
        self.assertIsInstance(obj_id, Int)
        self.assertGreater(obj_id.value, 0)

if __name__ == '__main__':
    unittest.main()
