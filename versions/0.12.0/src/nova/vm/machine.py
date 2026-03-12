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
        self.parent = None  # 父类对象
        self.parent_name = None  # 父类名称（用于延迟解析）
        self.init_method = None  # 构造函数
        self.static_fields = {}  # 静态字段 {name: value}
        self.static_methods = {}  # 静态方法 {name: function}
        self.is_abstract = False  # 是否是抽象类
        self._create_field_dict()
    
    def _create_field_dict(self):
        """
        创建字段字典
        """
        self.field_dict = {}
        for field in self.fields:
            if isinstance(field, tuple):
                if len(field) >= 2:
                    field_name = field[0]
                    self.field_dict[field_name] = None
                else:
                    # 只有一个元素，假设是字段名
                    self.field_dict[field] = None
            else:
                self.field_dict[field] = None
    
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
        # 检查是否是抽象类，抽象类不能被实例化
        if self.is_abstract:
            raise TypeError(f"Cannot instantiate abstract class '{self.name}'")
        
        # 解析父类（如果需要）
        self._try_resolve_parent()
        
        # 处理类型参数
        type_args = []
        actual_args = []
        
        if args:
            # 检查第一个参数是否是类型参数
            first_arg = args[0]
            if hasattr(first_arg, '__class__') and first_arg.__class__.__name__ == 'TypeNode':
                # 第一个参数是类型参数
                type_args = first_arg.types
                actual_args = args[1:]
            else:
                # 没有类型参数
                actual_args = args
        
        # 如果有构造函数，使用构造函数的参数
        if self.init_method:
            # 检查构造函数参数数量
            init_param_count = len(self.init_method.params)
            if len(actual_args) != init_param_count:
                raise TypeError(
                    f"{self.name}() takes {init_param_count} positional arguments "
                    f"but {len(actual_args)} were given"
                )
            
            # 创建实例（先不设置字段值）
            instance = NovaInstance(self)
            
            # 将参数存储到实例字段中
            for i, (param_name, param_type) in enumerate(self.init_method.params):
                if param_name in instance.fields:
                    instance.fields[param_name] = actual_args[i]
            
            return instance
        
        # 获取所有字段（包括继承的）
        all_fields = self._get_all_fields()
        
        # 检查位置参数数量
        field_count = len(all_fields)
        if len(actual_args) > field_count:
            raise TypeError(
                f"{self.name}() takes {field_count} positional arguments "
                f"but {len(actual_args)} were given"
            )
        
        # 检查关键字参数是否有效
        field_names = []
        for field in all_fields:
            if isinstance(field, tuple):
                field_names.append(field[0])
            else:
                field_names.append(field)
        
        for key in kwargs:
            if key not in field_names:
                raise TypeError(
                    f"{self.name}() got an unexpected keyword argument '{key}'"
                )
        
        # 将位置参数转换为关键字参数
        for i, arg in enumerate(actual_args):
            field = all_fields[i]
            if isinstance(field, tuple):
                field_name = field[0]
            else:
                field_name = field
            kwargs[field_name] = arg
        
        return NovaInstance(self, **kwargs)
    
    def _resolve_parent(self, environment):
        """
        解析父类对象
        
        Args:
            environment: 环境字典，用于查找父类
        """
        if self.parent_name and self.parent is None:
            if self.parent_name in environment:
                parent_class = environment[self.parent_name]
                if isinstance(parent_class, NovaClass):
                    self.parent = parent_class
    
    def _try_resolve_parent(self):
        """
        尝试从全局环境解析父类对象
        """
        if self.parent_name and self.parent is None:
            # 尝试从全局环境查找父类
            import __main__
            if hasattr(__main__, '_nova_global_env'):
                env = __main__._nova_global_env
                if self.parent_name in env:
                    parent_class = env[self.parent_name]
                    if isinstance(parent_class, NovaClass):
                        self.parent = parent_class
    
    def _get_all_fields(self):
        """
        获取所有字段（包括继承的）
        
        Returns:
            list: 所有字段列表
        """
        all_fields = list(self.fields)
        
        # 如果有父类，递归获取父类的字段
        if self.parent and isinstance(self.parent, NovaClass):
            parent_fields = self.parent._get_all_fields()
            all_fields = parent_fields + all_fields
        
        return all_fields
    
    def _get_all_methods(self):
        """
        获取所有方法（包括继承的）
        
        Returns:
            list: 所有方法列表
        """
        all_methods = list(self.methods)
        
        # 如果有父类，递归获取父类的方法
        if self.parent and isinstance(self.parent, NovaClass):
            parent_methods = self.parent._get_all_methods()
            # 父类方法在前，子类方法可以覆盖
            all_methods = parent_methods + all_methods
        
        return all_methods
    
    def __repr__(self):
        """
        类的字符串表示
        """
        return f"<class '{self.name}'>"
    
    def __getattr__(self, name):
        """
        获取静态字段或静态方法
        
        Args:
            name: 字段名或方法名
        
        Returns:
            静态字段值或静态方法
        """
        # 检查静态字段
        if name in self.static_fields:
            return self.static_fields[name]
        
        # 检查静态方法
        if name in self.static_methods:
            static_method_info = self.static_methods[name]
            if isinstance(static_method_info, tuple):
                static_method, access_modifier = static_method_info
            else:
                static_method = static_method_info
            
            # 返回绑定的方法
            def bound_static_method(*args, **kwargs):
                if hasattr(static_method, 'call'):
                    return static_method.call(*args, **kwargs)
                elif callable(static_method):
                    return static_method(*args, **kwargs)
            
            return bound_static_method
        
        raise AttributeError(f"'{self.name}' object has no attribute '{name}'")
    
    def get_method(self, method_name):
        """
        获取方法（支持继承）
        
        Args:
            method_name: 方法名
        
        Returns:
            方法函数或None
        """
        # 首先在当前类中查找
        for method_item in self.methods:
            if isinstance(method_item, tuple):
                if len(method_item) >= 2:
                    # 检查是否是 (name, method, access_modifier, is_abstract) 格式
                    if len(method_item) == 4:
                        name = method_item[0]
                        method = method_item[1]
                        is_abstract = method_item[3]
                        if name == method_name:
                            if is_abstract:
                                raise NotImplementedError(f"Cannot call abstract method '{method_name}' in class '{self.name}'")
                            return method
                    elif len(method_item) == 3:
                        name = method_item[0]
                        method = method_item[1]
                        if name == method_name:
                            return method
                    elif len(method_item) == 2:
                        # (name, method) 或 (method, access_modifier) 格式
                        first = method_item[0]
                        second = method_item[1]
                        
                        # 如果第一个是字符串，第二个是方法
                        if isinstance(first, str) and hasattr(second, 'name'):
                            if first == method_name:
                                return second
                        # 如果第一个是方法，检查方法名
                        elif hasattr(first, 'name') and first.name == method_name:
                            return first
                else:
                    # 只有一个元素
                    method = method_item[0]
                    if hasattr(method, 'name') and method.name == method_name:
                        return method
            else:
                # 不是元组，直接是方法对象
                if hasattr(method_item, 'name') and method_item.name == method_name:
                    return method_item
        
        # 如果在当前类中找不到，递归在父类中查找
        if self.parent and isinstance(self.parent, NovaClass):
            return self.parent.get_method(method_name)
        
        return None


class SuperProxy:
    """
    Super代理对象
    
    用于在子类中调用父类的方法和访问父类的字段
    """
    
    def __init__(self, instance):
        """
        初始化Super代理对象
        
        Args:
            instance: 子类实例
        """
        self.instance = instance
        self.nova_class = instance.nova_class
    
    def __getattr__(self, name):
        """
        获取父类的字段或方法
        
        Args:
            name: 字段名或方法名
        
        Returns:
            字段值或方法
        """
        # 获取父类
        parent_class = self.nova_class.parent
        if not parent_class:
            raise AttributeError(f"'super' object has no attribute '{name}' (no parent class)")
        
        # 检查是否是字段
        if hasattr(parent_class, 'field_dict') and name in parent_class.field_dict:
            # 返回父类实例的字段值
            if hasattr(self.instance, 'fields') and name in self.instance.fields:
                return self.instance.fields[name]
            return None
        
        # 检查是否是方法
        method = parent_class.get_method(name)
        if method:
            # 绑定到当前实例
            def bound_super_method(*args, **kwargs):
                return method(self.instance, *args, **kwargs)
            return bound_super_method
        
        raise AttributeError(f"'super' object has no attribute '{name}'")


class NovaInstance:
    """
    Nova类实例
    
    表示Nova结构体/类的实例，支持继承的字段和方法
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
        self.field_access = {}  # 存储字段的访问修饰符
        self._super = None  # Super代理对象（延迟创建）
        
        # 获取所有字段（包括继承的）
        all_fields = nova_class._get_all_fields()
        
        # 初始化字段
        for field in all_fields:
            if isinstance(field, tuple):
                if len(field) >= 3:
                    field_name = field[0]
                    field_type = field[1]
                    access_modifier = field[2]
                elif len(field) == 2:
                    field_name = field[0]
                    field_type = field[1]
                    access_modifier = 'public'
                else:
                    field_name = field[0]
                    field_type = None
                    access_modifier = 'public'
            else:
                field_name = field
                field_type = None
                access_modifier = 'public'
            
            if field_name in kwargs:
                self.fields[field_name] = kwargs[field_name]
            else:
                self.fields[field_name] = None
            
            self.field_access[field_name] = access_modifier
    
    def __getattr__(self, name):
        """
        获取字段或方法
        
        Args:
            name: 字段名或方法名
        
        Returns:
            字段值或方法
        """
        # 支持 this 关键字
        if name == 'this':
            return self
        
        # 支持 super 关键字
        if name == 'super':
            if self._super is None:
                self._super = SuperProxy(self)
            return self._super
        
        if name in self.fields:
            # 检查访问权限
            access = self.field_access.get(name, 'public')
            if access == 'private':
                # private 字段只能在类内部访问
                # 简化实现：始终允许访问（实际应该在语义分析阶段检查）
                pass
            elif access == 'protected':
                # protected 字段可以在类内部和子类中访问
                # 简化实现：始终允许访问
                pass
            return self.fields[name]
        
        method = self.nova_class.get_method(name)
        if method:
            # 绑定self参数
            def bound_method(*args, **kwargs):
                # 直接执行方法，不创建新的虚拟机实例
                # 这里需要手动处理参数和环境
                # 简化实现：直接调用方法
                return method(self, *args, **kwargs)
            return bound_method
        
        raise AttributeError(f"'{self.nova_class.name}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """
        设置字段值
        
        Args:
            name: 字段名
            value: 字段值
        """
        if name in ['nova_class', 'fields', 'field_access']:
            super().__setattr__(name, value)
        elif hasattr(self, 'fields') and name in self.fields:
            self.fields[name] = value
        else:
            # 允许设置新属性（用于初始化）
            super().__setattr__(name, value)
    
    def __add__(self, other):
        """
        加法运算
        
        Args:
            other: 另一个实例
        
        Returns:
            加法结果
        """
        # 尝试从nova_class中获取__add__方法
        method = self.nova_class.get_method("__add__")
        if method:
            # 调用__add__方法
            result = method(self, other)
            return result
        return NotImplemented
    
    def __sub__(self, other):
        """
        减法运算
        
        Args:
            other: 另一个实例
        
        Returns:
            减法结果
        """
        # 尝试从nova_class中获取__sub__方法
        method = self.nova_class.get_method("__sub__")
        if method:
            # 调用__sub__方法
            result = method(self, other)
            return result
        return NotImplemented
    
    def __eq__(self, other):
        """
        相等比较
        
        Args:
            other: 另一个实例
        
        Returns:
            bool: 是否相等
        """
        # 尝试从nova_class中获取__eq__方法
        method = self.nova_class.get_method("__eq__")
        if method:
            # 调用__eq__方法
            result = method(self, other)
            return result
        # 如果没有__eq__方法，使用默认比较（比较字段值）
        if not isinstance(other, NovaInstance):
            return False
        return self.nova_class == other.nova_class and self.fields == other.fields
    
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
    
    def __init__(self, name, instructions, params, is_async=False, environment=None):
        """
        初始化Nova函数
        
        Args:
            name: 函数名
            instructions: 函数体指令
            params: 参数列表，格式为ParameterDefinition对象或元组(name, type)
            is_async: 是否是异步函数
            environment: 函数的环境
        """
        self.name = name
        self.instructions = instructions
        self.params = params
        self.is_async = is_async
        self.environment = environment
        
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
        
        # 复制环境
        if self.environment:
            func_vm.environment.update(self.environment)
        
        # 检查第一个参数是否是实例（用于方法调用）
        # 如果是，设置 this 关键字，并从 args 中跳过
        used_args = 0
        if args and hasattr(args[0], 'nova_class'):
            func_vm.environment['this'] = args[0]
            used_args = 1  # 跳过第一个参数（this）
        
        # 处理位置参数
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


class Environment(dict):
    """
    环境类，支持变量地址获取
    """
    
    def __init__(self, memory_manager):
        super().__init__()
        self.memory = memory_manager
        self.variable_addresses = {}
    
    def get_address(self, name):
        """
        获取变量的内存地址
        
        Args:
            name: 变量名
        
        Returns:
            int: 内存地址
        """
        if name not in self.variable_addresses:
            # 分配新的内存地址
            address = self.memory.allocate(1)
            self.variable_addresses[name] = address
            # 如果变量已经有值，存储到内存
            if name in self:
                self.memory.store(address, self[name])
        return self.variable_addresses[name]
    
    def __setitem__(self, key, value):
        """
        设置变量值，同时更新内存
        """
        super().__setitem__(key, value)
        # 如果变量已经有地址，更新内存中的值
        if key in self.variable_addresses:
            self.memory.store(self.variable_addresses[key], value)


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
        # 内存管理器
        self.memory = MemoryManager()
        # 环境（变量存储）
        self.environment = Environment(self.memory)
        # 指令序列
        self.instructions = []
        # 运行状态
        self.running = False
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
        
        # dis函数 - 反汇编Nova代码
        def dis_func(code):
            """
            反汇编Nova代码，显示字节码
            
            Args:
                code: Nova源代码字符串
            """
            from nova.compiler.lexer.scanner import Scanner
            from nova.compiler.parser.parser import Parser
            from nova.compiler.optimizer.optimizer import Optimizer
            from nova.compiler.codegen.generator import CodeGenerator
            from nova.compiler.features import get_feature_manager
            from nova.compiler.parser.ast import FeatureStatement
            
            print(f"Source code:\n  {code.strip()}\n")
            
            try:
                # 词法分析
                scanner = Scanner(code)
                tokens = scanner.scan_tokens()
                
                # 语法分析
                parser = Parser(tokens)
                ast = parser.parse()
                
                # 检查并处理特性导入
                feature_manager = get_feature_manager()
                enabled_features = []
                
                # 遍历AST查找特性导入语句
                def find_feature_imports(node):
                    if isinstance(node, FeatureStatement):
                        feature_manager.enable(node.feature_name)
                        enabled_features.append(node.feature_name)
                    
                    # 递归处理子节点
                    for attr_name in dir(node):
                        if not attr_name.startswith('_'):
                            attr_value = getattr(node, attr_name, None)
                            if isinstance(attr_value, list):
                                for item in attr_value:
                                    find_feature_imports(item)
                            elif hasattr(attr_value, 'accept'):
                                find_feature_imports(attr_value)
                
                find_feature_imports(ast)
                
                if enabled_features:
                    print(f"Enabled features: {', '.join(enabled_features)}")
                
                # 优化（跳过语义分析，直接优化AST）
                optimizer = Optimizer()
                ast = optimizer.optimize(ast)
                print("Optimization: ENABLED")
                
                # 代码生成
                codegen = CodeGenerator()
                instructions, constants = codegen.generate(ast)
                
                print(f"\nConstants ({len(constants)}):")
                for i, const in enumerate(constants):
                    print(f"  {i}: {repr(const)}")
                
                print(f"\nInstructions ({len(instructions)}):")
                print("  Offset  Instruction")
                print("  " + "-" * 50)
                
                for offset, instr in enumerate(instructions):
                    print(f"  {offset:04X}    {instr}")
                
                print()
                
                # 禁用临时启用的特性
                for feature_name in enabled_features:
                    feature_manager.disable(feature_name)
                
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None
        
        self.environment['dis'] = BuiltinFunction('dis', dis_func)
    
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
