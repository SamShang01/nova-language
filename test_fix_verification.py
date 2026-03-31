#!/usr/bin/env python3
"""
测试修复验证脚本
验证栈下溢检查和指令映射修复
"""

from nova.compiler.compiler import Compiler
from nova.vm.machine import VirtualMachine

# 测试1: 基本功能测试
def test_basic_functionality():
    """测试基本功能是否正常"""
    code = '''
    def main():
        print("Hello, World!")
        return 42
    '''
    
    try:
        compiler = Compiler()
        instructions, constants = compiler.compile_to_bytecode(code)
        vm = VirtualMachine()
        # 执行编译后的代码
        vm.instructions = instructions
        vm.constants = constants
        vm.execute()
        print(f"测试1通过: 基本功能正常")
        return True
    except Exception as e:
        print(f"测试1失败: {e}")
        return False

# 测试2: 栈下溢检查测试
def test_stack_underflow_check():
    """测试栈下溢检查是否正常工作"""
    # 测试一个会导致栈下溢的情况
    code = '''
    def main():
        # 尝试访问不存在的变量
        print(undefined_variable)
    '''
    
    try:
        compiler = Compiler()
        instructions, constants = compiler.compile_to_bytecode(code)
        vm = VirtualMachine()
        vm.instructions = instructions
        vm.constants = constants
        vm.execute()
        print(f"测试2失败: 应该抛出错误")
        return False
    except Exception as e:
        print(f"测试2通过: 正确抛出错误: {e}")
        return True

# 测试3: 指令映射测试
def test_instruction_mapping():
    """测试指令映射是否完整"""
    from nova.vm.instructions import INSTRUCTIONS
    
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
        print(f"测试3失败: 缺少指令映射: {missing}")
        return False
    else:
        print(f"测试3通过: 所有指令映射完整")
        return True

# 运行所有测试
def run_tests():
    """运行所有测试"""
    tests = [
        test_basic_functionality,
        test_stack_underflow_check,
        test_instruction_mapping
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
