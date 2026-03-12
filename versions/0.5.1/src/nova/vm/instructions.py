"""
Nova语言虚拟机指令集
"""

from .errors import VMError

class Instruction:
    """
    虚拟机指令基类
    """
    
    def __init__(self, opcode, *args):
        """
        初始化指令
        
        Args:
            opcode: 操作码
            *args: 指令参数
        """
        self.opcode = opcode
        self.args = args
    
    def execute(self, vm):
        """
        执行指令
        
        Args:
            vm: 虚拟机实例
        """
        raise NotImplementedError(f"Instruction {self.opcode} not implemented")
    
    def __str__(self):
        return f"{self.opcode} {' '.join(map(str, self.args))}"

# 常量指令
class LOAD_CONST(Instruction):
    """
    加载常量
    """
    
    def __init__(self, value):
        super().__init__("LOAD_CONST", value)
    
    def execute(self, vm):
        vm.stack.append(self.args[0])

class LOAD_NAME(Instruction):
    """
    加载变量
    """
    
    def __init__(self, name):
        super().__init__("LOAD_NAME", name)
    
    def execute(self, vm):
        value = vm.environment.get(self.args[0])
        if value is None:
            raise VMError(f"Name '{self.args[0]}' not defined")
        vm.stack.append(value)

class STORE_NAME(Instruction):
    """
    存储变量
    """
    
    def __init__(self, name):
        super().__init__("STORE_NAME", name)
    
    def execute(self, vm):
        value = vm.stack.pop()
        vm.environment[self.args[0]] = value

# 算术指令
class BINARY_ADD(Instruction):
    """
    二元加法
    """
    
    def __init__(self):
        super().__init__("BINARY_ADD")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left + right
        vm.stack.append(result)

class BINARY_SUB(Instruction):
    """
    二元减法
    """
    
    def __init__(self):
        super().__init__("BINARY_SUB")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left - right
        vm.stack.append(result)

class BINARY_MUL(Instruction):
    """
    二元乘法
    """
    
    def __init__(self):
        super().__init__("BINARY_MUL")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left * right
        vm.stack.append(result)

class BINARY_DIV(Instruction):
    """
    二元除法
    """
    
    def __init__(self):
        super().__init__("BINARY_DIV")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left / right
        vm.stack.append(result)

# 比较指令
class COMPARE_EQ(Instruction):
    """
    比较等于
    """
    
    def __init__(self):
        super().__init__("COMPARE_EQ")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left == right
        vm.stack.append(result)

class COMPARE_NE(Instruction):
    """
    比较不等于
    """
    
    def __init__(self):
        super().__init__("COMPARE_NE")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left != right
        vm.stack.append(result)

class COMPARE_LT(Instruction):
    """
    比较小于
    """
    
    def __init__(self):
        super().__init__("COMPARE_LT")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left < right
        vm.stack.append(result)

class COMPARE_LE(Instruction):
    """
    比较小于等于
    """
    
    def __init__(self):
        super().__init__("COMPARE_LE")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left <= right
        vm.stack.append(result)

class COMPARE_GT(Instruction):
    """
    比较大于
    """
    
    def __init__(self):
        super().__init__("COMPARE_GT")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left > right
        vm.stack.append(result)

class COMPARE_GE(Instruction):
    """
    比较大于等于
    """
    
    def __init__(self):
        super().__init__("COMPARE_GE")
    
    def execute(self, vm):
        right = vm.stack.pop()
        left = vm.stack.pop()
        result = left >= right
        vm.stack.append(result)

# 控制流指令
class JUMP(Instruction):
    """
    无条件跳转
    """
    
    def __init__(self, target):
        super().__init__("JUMP", target)
    
    def execute(self, vm):
        vm.pc = self.args[0]

class JUMP_IF_TRUE(Instruction):
    """
    条件跳转（为真时）
    """
    
    def __init__(self, target):
        super().__init__("JUMP_IF_TRUE", target)
    
    def execute(self, vm):
        value = vm.stack.pop()
        if value:
            vm.pc = self.args[0]

class JUMP_IF_FALSE(Instruction):
    """
    条件跳转（为假时）
    """
    
    def __init__(self, target):
        super().__init__("JUMP_IF_FALSE", target)
    
    def execute(self, vm):
        value = vm.stack.pop()
        if not value:
            vm.pc = self.args[0]

class CALL_FUNCTION(Instruction):
    """
    调用函数
    """
    
    def __init__(self, arg_count, keyword_arg_names=None):
        if keyword_arg_names is None:
            super().__init__("CALL_FUNCTION", arg_count, [])
        else:
            super().__init__("CALL_FUNCTION", arg_count, keyword_arg_names)
    
    def execute(self, vm):
        positional_count = self.args[0]
        keyword_arg_names = self.args[1]
        
        # 从栈中弹出命名参数值（逆序）
        keyword_args = {}
        for name in reversed(keyword_arg_names):
            keyword_args[name] = vm.stack.pop()
        
        # 从栈中弹出位置参数（逆序）
        args = []
        for _ in range(positional_count):
            args.insert(0, vm.stack.pop())
        
        # 弹出函数
        func = vm.stack.pop()
        
        # 调用函数
        if keyword_args:
            result = func(*args, **keyword_args)
        else:
            result = func(*args)
        
        vm.stack.append(result)

class RETURN_VALUE(Instruction):
    """
    返回值
    """
    
    def __init__(self):
        super().__init__("RETURN_VALUE")
    
    def execute(self, vm):
        value = vm.stack.pop()
        vm.stack.append(value)
        vm.running = False

class POP_TOP(Instruction):
    """
    弹出栈顶元素
    """
    
    def __init__(self):
        super().__init__("POP_TOP")
    
    def execute(self, vm):
        if vm.stack:
            vm.stack.pop()

class NOP(Instruction):
    """
    空操作
    """
    
    def __init__(self):
        super().__init__("NOP")
    
    def execute(self, vm):
        pass

# 指令映射
INSTRUCTIONS = {
    "LOAD_CONST": LOAD_CONST,
    "LOAD_NAME": LOAD_NAME,
    "STORE_NAME": STORE_NAME,
    "BINARY_ADD": BINARY_ADD,
    "BINARY_SUB": BINARY_SUB,
    "BINARY_MUL": BINARY_MUL,
    "BINARY_DIV": BINARY_DIV,
    "COMPARE_EQ": COMPARE_EQ,
    "COMPARE_NE": COMPARE_NE,
    "COMPARE_LT": COMPARE_LT,
    "COMPARE_LE": COMPARE_LE,
    "COMPARE_GT": COMPARE_GT,
    "COMPARE_GE": COMPARE_GE,
    "JUMP": JUMP,
    "JUMP_IF_TRUE": JUMP_IF_TRUE,
    "JUMP_IF_FALSE": JUMP_IF_FALSE,
    "CALL_FUNCTION": CALL_FUNCTION,
    "RETURN_VALUE": RETURN_VALUE,
    "POP_TOP": POP_TOP,
    "NOP": NOP,
}
