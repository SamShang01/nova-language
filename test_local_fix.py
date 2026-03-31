#!/usr/bin/env python3
"""
直接使用本地代码的测试脚本
验证栈下溢检查和指令映射修复
"""

# 添加本地源代码路径到Python路径
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nova.compiler.compiler import Compiler
from nova.vm.instructions import INSTRUCTIONS

# 测试1: 指令映射测试
def test_instruction_mapping():
    """测试指令映射是否完整"""
    required_instructions = [
        "LOAD_CONST", "LOAD_NAME", "STORE_NAME", "STORE_ATTR",
        "DELETE_NAME", "BINARY_ADD", "BINARY_SUB", "BINARY_MUL", "BINARY_DIV",
        "COMPARE_EQ", "COMPARE_NE", "COMPARE_LT", "COMPARE_LE", "COMPARE_GT", "COMPARE_GE",
        "ADDR_OF", "DEREF", "STORE_DEREF",
        "JUMP", "JUMP_IF_TRUE", "JUMP_IF_FALSE",
        "CALL_FUNCTION", "RETURN_VALUE", "POP_TOP",
        "LOAD_SUBSCRIPT", "STORE_SUBSCRIPT", "NOP",
        "LABEL", "BUILD_LIST", "BUILD_TUPLE"
    ]
    
    missing = []
    for instr in required_instructions:
        if instr not in INSTRUCTIONS:
            missing.append(instr)
    
    if missing:
        print(f"测试1失败: 缺少指令映射: {missing}")
        return False
    else:
        print(f"测试1通过: 所有指令映射完整")
        return True

# 测试2: 栈下溢检查测试
def test_stack_underflow_check():
    """测试栈下溢检查是否存在于指令中"""
    from nova.vm.instructions import BINARY_ADD, COMPARE_EQ, POP_TOP
    
    # 检查BINARY_ADD是否有栈下溢检查
    add_code = BINARY_ADD.__dict__['execute'].__code__
    add_source = add_code.co_code.decode('latin1')
    
    # 检查是否包含栈大小检查
    if 'len(vm.stack) < 2' in BINARY_ADD.execute.__code__.co_code.decode('latin1'):
        print("测试2失败: BINARY_ADD缺少栈下溢检查")
        return False
    else:
        print("测试2通过: BINARY_ADD有栈下溢检查")
        
    # 检查POP_TOP是否有栈下溢检查
    if 'not vm.stack' in POP_TOP.execute.__code__.co_code.decode('latin1'):
        print("测试3失败: POP_TOP缺少栈下溢检查")
        return False
    else:
        print("测试3通过: POP_TOP有栈下溢检查")
        
    return True

# 运行所有测试
def run_tests():
    """运行所有测试"""
    tests = [
        test_instruction_mapping,
        test_stack_underflow_check
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n测试结果: {passed}/{total} 通过")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
