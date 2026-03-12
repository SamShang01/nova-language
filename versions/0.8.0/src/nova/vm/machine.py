"""
Nova语言虚拟机核心实现
"""

from .double_type import Double
from .instructions import INSTRUCTIONS
from .memory import MemoryManager
from .errors import VMError, StackError


class BuiltinFunction:
    """
    内置函数包装器
    
    为内置函数提供更好的字符串表示
    """
    
    def __init__(self, name, func):
        """
        初始化内置函数包装器
        
        Args:
            name: 函数名
            func: 函数对象
        """
        self.name = name
        self.func = func
    
    def __call__(self, *args, **kwargs):
        """
        调用函数
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            函数返回值
        """
        return self.func(*args, **kwargs)
    
    def __repr__(self):
        """
        函数的字符串表示
        """
        return f"<builtin function '{self.name}'>"
    
    def __str__(self):
        """
        函数的字符串表示
        """
        return f"<builtin function '{self.name}'>"


class NovaEnum:
    """
    Nova枚举对象代理
    
    封装Nova枚举的定义和访问逻辑
    """
    
    def __init__(self, name, variants):
        """
        初始化Nova枚举
        
        Args:
            name: 枚举名（可为None表示匿名枚举）
            variants: 变体列表，格式为["Variant1", "Variant2", ...]
        """
        self.name = name
        self.variants = variants
        self._create_variant_dict()
    
    def _create_variant_dict(self):
        """
        创建变体字典
        """
        self.variant_dict = {}
        for i, variant in enumerate(self.variants):
            self.variant_dict[variant] = i
    
    def __call__(self, variant_name):
        """
        创建枚举实例
        
        Args:
            variant_name: 变体名称
        
        Returns:
            NovaEnumInstance: 枚举实例
        
        Raises:
            ValueError: 变体不存在
        """
        if variant_name not in self.variant_dict:
            raise ValueError(f"'{variant_name}' is not a valid variant of enum '{self.name}'")
        
        return NovaEnumInstance(self, variant_name)
    
    def __getattr__(self, name):
        """
        获取变体
        
        Args:
            name: 变体名
        
        Returns:
            NovaEnumInstance: 枚举实例
        """
        if name in self.variant_dict:
            return NovaEnumInstance(self, name)
        
        raise AttributeError(f"'{self.name}' enum has no variant '{name}'")
    
    def __repr__(self):
        """
        枚举的字符串表示
        """
        if self.name:
            return f"<NovaEnum '{self.name}'>"
        return f"<NovaEnum (anonymous)>"


class NovaEnumInstance:
    """
    Nova枚举实例
    
    表示Nova枚举的实例
    """
    
    def __init__(self, nova_enum, variant):
        """
        初始化枚举实例
        
        Args:
            nova_enum: NovaEnum对象
            variant: 变体名称
        """
        self.nova_enum = nova_enum
        self.variant = variant
    
    def __eq__(self, other):
        """
        相等比较
        
        Args:
            other: 另一个枚举实例
        
        Returns:
            bool: 是否相等
        """
        if not isinstance(other, NovaEnumInstance):
            return False
        return self.nova_enum == other.nova_enum and self.variant == other.variant
    
    def __repr__(self):
        """
        实例的字符串表示
        """
        if self.nova_enum.name:
            return f"{self.nova_enum.name}.{self.variant}"
        return f"<enum.{self.variant}>"


class NovaUnion:
    """
    Nova联合体对象代理
    
    封装Nova联合体的定义和访问逻辑
    """
    
    def __init__(self, name, variants):
        """
        初始化Nova联合体
        
        Args:
            name: 联合体名（可为None表示匿名联合体）
            variants: 变体类型列表，格式为[type1, type2, ...]
        """
        self.name = name
        self.variants = variants
    
    def __call__(self, value):
        """
        创建联合体实例
        
        Args:
            value: 联合体值
        
        Returns:
            NovaUnionInstance: 联合体实例
        """
        return NovaUnionInstance(self, value)
    
    def __repr__(self):
        """
        联合体的字符串表示
        """
        if self.name:
            return f"<NovaUnion '{self.name}'>"
        return f"<NovaUnion (anonymous)>"


class NovaUnionInstance:
    """
    Nova联合体实例
    
    表示Nova联合体的实例
    """
    
    def __init__(self, nova_union, value):
        """
        初始化联合体实例
        
        Args:
            nova_union: NovaUnion对象
            value: 联合体值
        """
        self.nova_union = nova_union
        self.value = value
    
    def __eq__(self, other):
        """
        相等比较
        
        Args:
            other: 另一个联合体实例
        
        Returns:
            bool: 是否相等
        """
        if not isinstance(other, NovaUnionInstance):
            return False
        return self.value == other.value
    
    def __repr__(self):
        """
        实例的字符串表示
        """
        if self.nova_union.name:
            return f"{self.nova_union.name}({self.value})"
        return f"<union({self.value})>"


class NovaClass:
    """
    Nova类对象代理
    
    封装Nova结构体/类的定义和实例化逻辑
    """
    
    def __init__(self, name, fields, methods):
        """
        初始化Nova类
        
        Args:
            name: 类名
            fields: 字段列表，格式为[(field_name, field_type), ...]
            methods: 方法列表，格式为[method_name, method_function, ...]
        """
        self.name = name
        self.fields = fields
        self.methods = methods
        self._create_field_dict()
    
    def _create_field_dict(self):
        """
        创建字段字典
        """
        self.field_dict = {}
        for field_name, field_type in self.fields:
            self.field_dict[field_name] = None
    
    def __call__(self, *args, **kwargs):
        """
        实例化类
        
        Args:
            *args: 位置参数，按字段顺序赋值
            **kwargs: 字段初始值（关键字参数）
        
        Returns:
            NovaInstance: 类实例
        
        Raises:
            TypeError: 参数数量或类型不匹配
        """
        # 检查位置参数数量
        if len(args) > len(self.fields):
            raise TypeError(
                f"{self.name}() takes {len(self.fields)} positional arguments "
                f"but {len(args)} were given"
            )
        
        # 检查关键字参数是否有效
        field_names = [field[0] for field in self.fields]
        for key in kwargs:
            if key not in field_names:
                raise TypeError(
                    f"{self.name}() got an unexpected keyword argument '{key}'"
                )
        
        # 将位置参数转换为关键字参数
        for i, arg in enumerate(args):
            field_name = self.fields[i][0]
            kwargs[field_name] = arg
        
        return NovaInstance(self, **kwargs)
    
    def __repr__(self):
        """
        类的字符串表示
        """
        return f"<class '{self.name}'>"
    
    def get_method(self, method_name):
        """
        获取方法
        
        Args:
            method_name: 方法名
        
        Returns:
            方法函数或None
        """
        for name, method in self.methods:
            if name == method_name:
                return method
        return None


class NovaInstance:
    """
    Nova类实例
    
    表示Nova结构体/类的实例
    """
    
    def __init__(self, nova_class, **kwargs):
        """
        初始化实例
        
        Args:
            nova_class: NovaClass对象
            **kwargs: 字段初始值
        """
        self.nova_class = nova_class
        self.fields = {}
        
        # 初始化字段
        for field_name, field_type in nova_class.fields:
            if field_name in kwargs:
                self.fields[field_name] = kwargs[field_name]
            else:
                self.fields[field_name] = None
    
    def __getattr__(self, name):
        """
        获取字段或方法
        
        Args:
            name: 字段名或方法名
        
        Returns:
            字段值或方法
        """
        if name in self.fields:
            return self.fields[name]
        
        method = self.nova_class.get_method(name)
        if method:
            return method
        
        raise AttributeError(f"'{self.nova_class.name}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """
        设置字段值
        
        Args:
            name: 字段名
            value: 字段值
        """
        if name in ['nova_class', 'fields']:
            super().__setattr__(name, value)
        elif name in self.fields:
            self.fields[name] = value
        else:
            raise AttributeError(f"'{self.nova_class.name}' object has no attribute '{name}'")
    
    def __repr__(self):
        """
        实例的字符串表示
        """
        fields_str = ', '.join(f'{k}={v}' for k, v in self.fields.items())
        return f"<{self.nova_class.name}({fields_str})>"


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
        self.mandatory_params = []
        
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
                    if param.is_mandatory:
                        self.mandatory_params.append(param.name)
                    if param.default_value is not None:
                        # 求值默认值
                        evaluated_value = self._evaluate_default_value(param.default_value)
                        self.default_values[param.name] = evaluated_value
    
    def _evaluate_default_value(self, default_value):
        """
        求值默认值表达式
        
        Args:
            default_value: 默认值表达式（AST节点）
        
        Returns:
            求值后的值
        """
        # 简化实现：只支持字面量
        if hasattr(default_value, 'literal'):
            return default_value.literal
        elif hasattr(default_value, 'value'):
            return default_value.value
        else:
            # 复杂表达式，暂时返回None
            return None
    
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
            elif param_name in self.mandatory_params:
                # 强制参数未提供
                raise TypeError(f"Missing mandatory argument '{param_name}' for function '{self.name}'")
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
        return f"<function '{self.name}'>"


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
        self.environment['print'] = BuiltinFunction('print', print_func)
        
        # len函数
        def len_func(value):
            return len(value)
        self.environment['len'] = BuiltinFunction('len', len_func)
        
        # input函数
        def input_func(prompt=""):
            return input(prompt)
        self.environment['input'] = BuiltinFunction('input', input_func)
        
        # type函数
        def type_func(value):
            return type(value).__name__
        self.environment['type'] = BuiltinFunction('type', type_func)
        
        # str函数
        def str_func(value):
            return str(value)
        self.environment['str'] = BuiltinFunction('str', str_func)
        
        # int函数
        def int_func(value):
            return int(value)
        self.environment['int'] = BuiltinFunction('int', int_func)
        
        # float函数
        def float_func(value):
            return float(value)
        self.environment['float'] = BuiltinFunction('float', float_func)
        
        # abs函数
        def abs_func(value):
            return abs(value)
        self.environment['abs'] = BuiltinFunction('abs', abs_func)
        
        # max函数
        def max_func(*args):
            return max(*args)
        self.environment['max'] = BuiltinFunction('max', max_func)
        
        # min函数
        def min_func(*args):
            return min(*args)
        self.environment['min'] = BuiltinFunction('min', min_func)
        
        # sum函数
        def sum_func(iterable):
            return sum(iterable)
        self.environment['sum'] = BuiltinFunction('sum', sum_func)
        
        # round函数
        def round_func(value, ndigits=0):
            return round(value, ndigits)
        self.environment['round'] = BuiltinFunction('round', round_func)
        
        # Double类型构造函数
        def double_func(value):
            return Double(value)
        self.environment['Double'] = BuiltinFunction('Double', double_func)
    
    def load(self, instructions, constants=None):
        """
        加载指令
        
        Args:
            instructions: 指令列表
            constants: 常量列表（可选）
        """
        self.instructions = instructions
        self.pc = 0
        self.stack = []
        # 处理常量（如果提供）
        if constants:
            self.constants = constants
    
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
