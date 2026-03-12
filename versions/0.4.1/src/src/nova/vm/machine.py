"""
Nova语言虚拟机核心实现
"""

from .instructions import INSTRUCTIONS
from .memory import MemoryManager
from .errors import VMError, StackError


class NovaFunction:
    """
    Nova函数代理对象
    
    封装Nova函数的定义和执行逻辑
    支持普通参数、默认值参数、可变参数和关键字可变参数
    """
    
    def __init__(self, name, instructions, params):
        """
        初始化Nova函数
        
        Args:
            name: 函数名
            instructions: 函数体指令
            params: 参数列表，格式为ParameterDefinition对象或元组(name, type)
        """
        self.name = name
        self.instructions = instructions
        self.params = params
        
        # 解析参数类型
        self._parse_params()
    
    def _parse_params(self):
        """
        解析参数，提取普通参数、可变参数和关键字参数
        """
        self.normal_params = []
        self.varargs_param = None
        self.kwargs_param = None
        self.default_values = {}
        
        for param in self.params:
            if isinstance(param, tuple):
                # 兼容旧格式：元组(name, type)
                self.normal_params.append((param[0], param[1]))
            else:
                # 新格式：ParameterDefinition对象
                if param.is_varargs:
                    self.varargs_param = param.name
                elif param.is_kwargs:
                    self.kwargs_param = param.name
                else:
                    self.normal_params.append((param.name, param.param_type))
                    if param.default_value is not None:
                        self.default_values[param.name] = param.default_value
    
    def __call__(self, *args, **kwargs):
        """
        调用函数
        
        Args:
            *args: 位置参数列表
            **kwargs: 关键字参数字典
        
        Returns:
            函数返回值
        """
        # 创建一个新的虚拟机实例来执行函数体
        from nova.vm.machine import VirtualMachine
        func_vm = VirtualMachine()
        
        # 处理位置参数
        used_args = 0
        for param_name, param_type in self.normal_params:
            if used_args < len(args):
                func_vm.environment[param_name] = args[used_args]
                used_args += 1
            elif param_name in self.default_values:
                func_vm.environment[param_name] = self.default_values[param_name]
            else:
                func_vm.environment[param_name] = None
        
        # 处理可变参数
        if self.varargs_param:
            remaining_args = args[used_args:]
            func_vm.environment[self.varargs_param] = remaining_args
        
        # 处理关键字参数
        if self.kwargs_param:
            func_vm.environment[self.kwargs_param] = kwargs
        else:
            # 将关键字参数绑定到对应的参数
            for key, value in kwargs.items():
                for param_name, param_type in self.normal_params:
                    if param_name == key:
                        func_vm.environment[param_name] = value
                        break
        
        # 执行函数体
        func_vm.load(self.instructions)
        result = func_vm.run()
        
        return result
    
    def __repr__(self):
        """
        函数的字符串表示
        """
        return f"<NovaFunction '{self.name}'>"


class VirtualMachine:
    """
    虚拟机
    
    负责执行Nova语言的字节码指令
    """
    
    def __init__(self):
        """
        初始化虚拟机
        """
        # 指令指针
        self.pc = 0
        # 栈
        self.stack = []
        # 环境（变量存储）
        self.environment = {}
        # 指令序列
        self.instructions = []
        # 运行状态
        self.running = False
        # 内存管理器
        self.memory = MemoryManager()
        # 内置函数
        self._initialize_builtins()
    
    def _initialize_builtins(self):
        """
        初始化内置函数
        """
        # print函数
        def print_func(value):
            print(value)
            return None
        self.environment['print'] = print_func
        
        # len函数
        def len_func(value):
            return len(value)
        self.environment['len'] = len_func
        
        # input函数
        def input_func(prompt=""):
            return input(prompt)
        self.environment['input'] = input_func
        
        # type函数
        def type_func(value):
            return type(value).__name__
        self.environment['type'] = type_func
        
        # str函数
        def str_func(value):
            return str(value)
        self.environment['str'] = str_func
        
        # int函数
        def int_func(value):
            return int(value)
        self.environment['int'] = int_func
        
        # float函数
        def float_func(value):
            return float(value)
        self.environment['float'] = float_func
        
        # abs函数
        def abs_func(value):
            return abs(value)
        self.environment['abs'] = abs_func
        
        # max函数
        def max_func(*args):
            return max(*args)
        self.environment['max'] = max_func
        
        # min函数
        def min_func(*args):
            return min(*args)
        self.environment['min'] = min_func
        
        # sum函数
        def sum_func(iterable):
            return sum(iterable)
        self.environment['sum'] = sum_func
        
        # round函数
        def round_func(value, ndigits=0):
            return round(value, ndigits)
        self.environment['round'] = round_func
    
    def load(self, instructions):
        """
        加载指令
        
        Args:
            instructions: 指令列表
        """
        self.instructions = instructions
        self.pc = 0
        self.stack = []
    
    def run(self):
        """
        运行虚拟机
        
        Returns:
            Any: 栈顶值
        """
        # 预加载跳转指令类型，避免每次循环都导入
        from .instructions import JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE
        jump_instruction_types = (JUMP, JUMP_IF_TRUE, JUMP_IF_FALSE)
        
        self.running = True
        while self.running:
            if self.pc >= len(self.instructions):
                self.running = False
                break
            
            instruction = self.instructions[self.pc]
            try:
                instruction.execute(self)
            except Exception as e:
                raise VMError(f"Error executing instruction {instruction}: {e}")
            
            # 除了跳转指令，其他指令自动递增PC
            if not isinstance(instruction, jump_instruction_types):
                self.pc += 1
        
        return self.stack[-1] if self.stack else None
    
    def execute(self, instructions):
        """
        执行指令序列
        
        Args:
            instructions: 指令列表
        
        Returns:
            Any: 执行结果
        """
        self.load(instructions)
        return self.run()
    
    def push(self, value):
        """
        压栈
        
        Args:
            value: 值
        """
        self.stack.append(value)
    
    def pop(self):
        """
        出栈
        
        Returns:
            Any: 栈顶值
        
        Raises:
            StackError: 如果栈为空
        """
        if not self.stack:
            raise StackError("Stack underflow")
        return self.stack.pop()
    
    def peek(self):
        """
        查看栈顶值
        
        Returns:
            Any: 栈顶值
        
        Raises:
            StackError: 如果栈为空
        """
        if not self.stack:
            raise StackError("Stack is empty")
        return self.stack[-1]
    
    def set_global(self, name, value):
        """
        设置全局变量
        
        Args:
            name: 变量名
            value: 值
        """
        self.environment[name] = value
    
    def get_global(self, name):
        """
        获取全局变量
        
        Args:
            name: 变量名
        
        Returns:
            Any: 变量值
        """
        return self.environment.get(name)
    
    def clear(self):
        """
        清空虚拟机状态
        """
        self.pc = 0
        self.stack = []
        self.environment = {}
        self.instructions = []
        self.running = False
        self._initialize_builtins()
    
    def get_state(self):
        """
        获取虚拟机状态
        
        Returns:
            dict: 虚拟机状态
        """
        return {
            'pc': self.pc,
            'stack': self.stack.copy(),
            'environment': self.environment.copy(),
            'instructions': [str(instr) for instr in self.instructions],
            'running': self.running,
            'memory_usage': self.memory.get_heap_usage(),
        }
