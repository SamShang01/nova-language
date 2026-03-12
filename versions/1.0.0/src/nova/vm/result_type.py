"""
Nova语言Result<T,E>错误处理

实现类型安全的错误处理机制
"""

from typing import Generic, TypeVar, Optional, Any, Callable, Union
from enum import Enum


T = TypeVar('T')  # 成功值类型
E = TypeVar('E')  # 错误类型


class ResultState(Enum):
    """
    Result状态
    """
    OK = 0
    ERR = 1


class Result(Generic[T, E]):
    """
    Result<T,E>类型
    
    表示可能失败的操作结果，提供类型安全的错误处理
    """
    
    def __init__(self, state: ResultState, value: Optional[T] = None, error: Optional[E] = None):
        """
        初始化Result
        
        Args:
            state: 结果状态
            value: 成功值（如果状态为OK）
            error: 错误值（如果状态为ERR）
        """
        self._state = state
        self._value = value
        self._error = error
    
    @staticmethod
    def ok(value: T) -> 'Result[T, E]':
        """
        创建成功结果
        
        Args:
            value: 成功值
        
        Returns:
            Result[T, E]: 成功结果
        
        Example:
            result = Result.ok(42)
        """
        return Result(ResultState.OK, value=value)
    
    @staticmethod
    def err(error: E) -> 'Result[T, E]':
        """
        创建错误结果
        
        Args:
            error: 错误值
        
        Returns:
            Result[T, E]: 错误结果
        
        Example:
            result = Result.err("Division by zero")
        """
        return Result(ResultState.ERR, error=error)
    
    def is_ok(self) -> bool:
        """
        检查是否为成功结果
        
        Returns:
            bool: 如果为成功结果返回True
        """
        return self._state == ResultState.OK
    
    def is_err(self) -> bool:
        """
        检查是否为错误结果
        
        Returns:
            bool: 如果为错误结果返回True
        """
        return self._state == ResultState.ERR
    
    def unwrap(self) -> T:
        """
        解包结果
        
        Returns:
            T: 成功值
        
        Raises:
            RuntimeError: 如果结果为错误
        
        Example:
            result = Result.ok(42)
            value = result.unwrap()  # 42
        """
        if self.is_ok():
            return self._value
        else:
            raise RuntimeError(f"Called unwrap on error result: {self._error}")
    
    def unwrap_err(self) -> E:
        """
        解包错误
        
        Returns:
            E: 错误值
        
        Raises:
            RuntimeError: 如果结果为成功
        
        Example:
            result = Result.err("Division by zero")
            error = result.unwrap_err()  # "Division by zero"
        """
        if self.is_err():
            return self._error
        else:
            raise RuntimeError("Called unwrap_err on ok result")
    
    def unwrap_or(self, default: T) -> T:
        """
        解包结果或返回默认值
        
        Args:
            default: 默认值
        
        Returns:
            T: 成功值或默认值
        
        Example:
            result = Result.ok(42)
            value = result.unwrap_or(0)  # 42
            
            result = Result.err("Error")
            value = result.unwrap_or(0)  # 0
        """
        if self.is_ok():
            return self._value
        else:
            return default
    
    def unwrap_or_else(self, default_func: Callable[[], T]) -> T:
        """
        解包结果或调用默认函数
        
        Args:
            default_func: 默认值生成函数
        
        Returns:
            T: 成功值或默认函数的返回值
        
        Example:
            result = Result.ok(42)
            value = result.unwrap_or_else(lambda: 0)  # 42
            
            result = Result.err("Error")
            value = result.unwrap_or_else(lambda: 0)  # 0
        """
        if self.is_ok():
            return self._value
        else:
            return default_func()
    
    def map(self, func: Callable[[T], T]) -> 'Result[T, E]':
        """
        映射成功值
        
        Args:
            func: 映射函数
        
        Returns:
            Result[T, E]: 映射后的结果
        
        Example:
            result = Result.ok(5)
            mapped = result.map(lambda x: x * 2)  # Result.ok(10)
            
            result = Result.err("Error")
            mapped = result.map(lambda x: x * 2)  # Result.err("Error")
        """
        if self.is_ok():
            try:
                return Result.ok(func(self._value))
            except Exception as e:
                return Result.err(e)
        else:
            return Result.err(self._error)
    
    def map_err(self, func: Callable[[E], E]) -> 'Result[T, E]':
        """
        映射错误值
        
        Args:
            func: 映射函数
        
        Returns:
            Result[T, E]: 映射后的结果
        
        Example:
            result = Result.err("Error")
            mapped = result.map_err(lambda e: e.upper())  # Result.err("ERROR")
            
            result = Result.ok(42)
            mapped = result.map_err(lambda e: e.upper())  # Result.ok(42)
        """
        if self.is_err():
            try:
                return Result.err(func(self._error))
            except Exception as e:
                return Result.err(e)
        else:
            return Result.ok(self._value)
    
    def and_then(self, func: Callable[[T], 'Result[T, E]']) -> 'Result[T, E]':
        """
        链式调用
        
        Args:
            func: 返回Result的函数
        
        Returns:
            Result[T, E]: 链式调用结果
        
        Example:
            result = Result.ok(5)
            chained = result.and_then(lambda x: Result.ok(x * 2))  # Result.ok(10)
            
            result = Result.err("Error")
            chained = result.and_then(lambda x: Result.ok(x * 2))  # Result.err("Error")
        """
        if self.is_ok():
            return func(self._value)
        else:
            return Result.err(self._error)
    
    def or_else(self, func: Callable[[E], 'Result[T, E]']) -> 'Result[T, E]':
        """
        错误处理链式调用
        
        Args:
            func: 返回Result的函数
        
        Returns:
            Result[T, E]: 链式调用结果
        
        Example:
            result = Result.err("Error")
            handled = result.or_else(lambda e: Result.ok(0))  # Result.ok(0)
            
            result = Result.ok(42)
            handled = result.or_else(lambda e: Result.ok(0))  # Result.ok(42)
        """
        if self.is_err():
            return func(self._error)
        else:
            return Result.ok(self._value)
    
    def match(self, ok_func: Callable[[T], Any], err_func: Callable[[E], Any]) -> Any:
        """
        模式匹配
        
        Args:
            ok_func: 成功时的处理函数
            err_func: 错误时的处理函数
        
        Returns:
            Any: 处理函数的返回值
        
        Example:
            result = Result.ok(42)
            value = result.match(
                lambda x: x * 2,
                lambda e: 0
            )  # 84
            
            result = Result.err("Error")
            value = result.match(
                lambda x: x * 2,
                lambda e: 0
            )  # 0
        """
        if self.is_ok():
            return ok_func(self._value)
        else:
            return err_func(self._error)
    
    def __repr__(self):
        """
        Result的字符串表示
        """
        if self.is_ok():
            return f"Result.ok({self._value})"
        else:
            return f"Result.err({self._error})"
    
    def __eq__(self, other) -> bool:
        """
        相等比较
        """
        if not isinstance(other, Result):
            return False
        
        if self._state != other._state:
            return False
        
        if self.is_ok():
            return self._value == other._value
        else:
            return self._error == other._error
    
    def __hash__(self):
        """
        哈希值
        """
        return hash((self._state, self._value, self._error))


class Option(Generic[T]):
    """
    Option<T>类型
    
    表示可能不存在的值
    """
    
    def __init__(self, is_some: bool, value: Optional[T] = None):
        """
        初始化Option
        
        Args:
            is_some: 是否有值
            value: 值（如果有）
        """
        self._is_some = is_some
        self._value = value
    
    @staticmethod
    def some(value: T) -> 'Option[T]':
        """
        创建有值的Option
        
        Args:
            value: 值
        
        Returns:
            Option[T]: 有值的Option
        """
        return Option(True, value)
    
    @staticmethod
    def none() -> 'Option[T]':
        """
        创建无值的Option
        
        Returns:
            Option[T]: 无值的Option
        """
        return Option(False)
    
    def is_some(self) -> bool:
        """
        检查是否有值
        
        Returns:
            bool: 如果有值返回True
        """
        return self._is_some
    
    def is_none(self) -> bool:
        """
        检查是否无值
        
        Returns:
            bool: 如果无值返回True
        """
        return not self._is_some
    
    def unwrap(self) -> T:
        """
        解包值
        
        Returns:
            T: 值
        
        Raises:
            RuntimeError: 如果无值
        """
        if self.is_some():
            return self._value
        else:
            raise RuntimeError("Called unwrap on None option")
    
    def unwrap_or(self, default: T) -> T:
        """
        解包值或返回默认值
        
        Args:
            default: 默认值
        
        Returns:
            T: 值或默认值
        """
        if self.is_some():
            return self._value
        else:
            return default
    
    def map(self, func: Callable[[T], T]) -> 'Option[T]':
        """
        映射值
        
        Args:
            func: 映射函数
        
        Returns:
            Option[T]: 映射后的Option
        """
        if self.is_some():
            try:
                return Option.some(func(self._value))
            except Exception:
                return Option.none()
        else:
            return Option.none()
    
    def __repr__(self):
        """
        Option的字符串表示
        """
        if self.is_some():
            return f"Option.some({self._value})"
        else:
            return "Option.none()"
    
    def __eq__(self, other) -> bool:
        """
        相等比较
        """
        if not isinstance(other, Option):
            return False
        
        if self._is_some != other._is_some:
            return False
        
        if self.is_some():
            return self._value == other._value
        
        return True
    
    def __hash__(self):
        """
        哈希值
        """
        return hash((self._is_some, self._value))