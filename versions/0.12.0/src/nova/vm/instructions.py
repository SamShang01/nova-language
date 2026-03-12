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
        if self.args[0] not in vm.environment:
            raise VMError(f"Name '{self.args[0]}' not defined")
        value = vm.environment[self.args[0]]
        vm.stack.append(value)

class STORE_NAME(Instruction):
    """
    存储变量
    """
    
    def __init__(self, name):
        super().__init__("STORE_NAME", name)
    
    def execute(self, vm):
        value = vm.stack.pop()
        # 如果值是NovaFunction对象，设置其环境为当前环境
        from nova.vm.machine import NovaFunction, NovaClass
        if isinstance(value, NovaFunction):
            value.environment = vm.environment.copy()
        # 如果值是NovaClass对象且有父类名称，解析父类
        elif isinstance(value, NovaClass):
            if value.parent_name and value.parent is None:
                if value.parent_name in vm.environment:
                    parent_class = vm.environment[value.parent_name]
                    if isinstance(parent_class, NovaClass):
                        value.parent = parent_class
        vm.environment[self.args[0]] = value

# 属性存储指令
class STORE_ATTR(Instruction):
    """
    存储属性到对象
    """
    
    def __init__(self, attr_name):
        super().__init__("STORE_ATTR", attr_name)
    
    def execute(self, vm):
        obj = vm.stack.pop()
        value = vm.stack.pop()
        
        # 设置对象的属性
        if hasattr(obj, 'fields') and isinstance(obj.fields, dict):
            obj.fields[self.args[0]] = value
        elif hasattr(obj, '__setattr__'):
            obj.__setattr__(self.args[0], value)
        else:
            setattr(obj, self.args[0], value)

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
        # 检查是否有__add__方法，并且不是基本类型
        if (hasattr(left, "__add__") and callable(left.__add__) and 
            not isinstance(left, (int, float, str, bool, list, dict, tuple))):
            # 直接调用__add__方法，避免使用Python的+运算符导致递归
            result = left.__add__(right)
        else:
            # 如果没有__add__方法或是基本类型，使用Python的+运算符
            try:
                result = left + right
            except Exception as e:
                raise VMError(f"Error executing BINARY_ADD: {e}")
        # 评估延迟表达式，防止浮点数精度问题
        if hasattr(result, "evaluate"):
            result = result.evaluate()
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
        # 检查是否有__sub__方法，并且不是基本类型
        if (hasattr(left, "__sub__") and callable(left.__sub__) and 
            not isinstance(left, (int, float, str, bool, list, dict, tuple))):
            # 直接调用__sub__方法，避免使用Python的-运算符导致递归
            result = left.__sub__(right)
        else:
            # 如果没有__sub__方法或是基本类型，使用Python的-运算符
            try:
                result = left - right
            except Exception as e:
                raise VMError(f"Error executing BINARY_SUB: {e}")
        # 评估延迟表达式，防止浮点数精度问题
        if hasattr(result, "evaluate"):
            result = result.evaluate()
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
        # 检查是否有__mul__方法，并且不是基本类型
        if (hasattr(left, "__mul__") and callable(left.__mul__) and 
            not isinstance(left, (int, float, str, bool, list, dict, tuple))):
            # 直接调用__mul__方法
            result = left.__mul__(right)
        else:
            # 如果没有__mul__方法或是基本类型，使用Python的*运算符
            try:
                result = left * right
            except Exception as e:
                raise VMError(f"Error executing BINARY_MUL: {e}")
        # 评估延迟表达式，防止浮点数精度问题
        if hasattr(result, "evaluate"):
            result = result.evaluate()
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
        # 检查是否有__truediv__方法，并且不是基本类型
        if (hasattr(left, "__truediv__") and callable(left.__truediv__) and 
            not isinstance(left, (int, float, str, bool, list, dict, tuple))):
            # 直接调用__truediv__方法
            result = left.__truediv__(right)
        else:
            # 如果没有__truediv__方法或是基本类型，使用Python的/运算符
            try:
                result = left / right
            except Exception as e:
                raise VMError(f"Error executing BINARY_DIV: {e}")
        # 评估延迟表达式，防止浮点数精度问题
        if hasattr(result, "evaluate"):
            result = result.evaluate()
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
        # 检查是否有__eq__方法
        if hasattr(left, "__eq__") and callable(left.__eq__):
            result = left.__eq__(right)
        else:
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
        # 检查是否有__ne__方法
        if hasattr(left, "__ne__") and callable(left.__ne__):
            result = left.__ne__(right)
        else:
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
        # 检查是否有__lt__方法
        if hasattr(left, "__lt__") and callable(left.__lt__):
            result = left.__lt__(right)
        else:
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
        # 检查是否有__le__方法
        if hasattr(left, "__le__") and callable(left.__le__):
            result = left.__le__(right)
        else:
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
        # 检查是否有__gt__方法
        if hasattr(left, "__gt__") and callable(left.__gt__):
            result = left.__gt__(right)
        else:
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
        # 检查是否有__ge__方法
        if hasattr(left, "__ge__") and callable(left.__ge__):
            result = left.__ge__(right)
        else:
            result = left >= right
        vm.stack.append(result)

# 指针操作指令
class ADDR_OF(Instruction):
    """
    取地址指令
    
    将栈顶值的地址压入栈
    """
    
    def __init__(self, name):
        super().__init__("ADDR_OF", name)
    
    def execute(self, vm):
        # 获取变量名
        name = self.args[0]
        # 从环境中获取变量的地址（这里使用变量名作为地址标识）
        address = vm.environment.get_address(name)
        vm.stack.append(address)

class DEREF(Instruction):
    """
    解引用指令
    
    解引用栈顶的指针值
    """
    
    def __init__(self):
        super().__init__("DEREF")
    
    def execute(self, vm):
        # 弹出指针地址
        address = vm.stack.pop()
        # 从内存中加载值
        value = vm.memory.load(address)
        vm.stack.append(value)

class STORE_DEREF(Instruction):
    """
    通过指针存储指令
    
    将值存储到指针指向的地址
    """
    
    def __init__(self):
        super().__init__("STORE_DEREF")
    
    def execute(self, vm):
        # 弹出值和地址
        value = vm.stack.pop()
        address = vm.stack.pop()
        # 存储到内存
        vm.memory.store(address, value)

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
        else:
            vm.pc += 1

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
        else:
            vm.pc += 1

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

class LABEL(Instruction):
    """
    标签指令（用于跳转目标）
    """
    
    def __init__(self, name):
        super().__init__("LABEL", name)
    
    def execute(self, vm):
        # 标签指令不执行任何操作，只是作为跳转目标
        pass

class DELETE_NAME(Instruction):
    """
    删除变量
    """
    
    def __init__(self, name):
        super().__init__("DELETE_NAME", name)
    
    def execute(self, vm):
        if self.args[0] in vm.environment:
            del vm.environment[self.args[0]]

# 指令映射
INSTRUCTIONS = {
    "LOAD_CONST": LOAD_CONST,
    "LOAD_NAME": LOAD_NAME,
    "STORE_NAME": STORE_NAME,
    "DELETE_NAME": DELETE_NAME,
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
