"""
Typing module for Nova programming language

This module provides type hinting utilities and decorators for Nova.
"""

__version__ = (0, 6, 0)

# Type aliases
Any = object
Optional = lambda T: T
List = lambda T: list
Dict = lambda K, V: dict
Tuple = lambda *Ts: tuple
Set = lambda T: set

# Decorators
def overload(func):
    """
    Decorator to mark function overloads.
    
    Usage:
    @overload
    def foo(x: int) -> int:
        pass
    
    @overload
    def foo(x: str) -> str:
        pass
    
    def foo(x):
        if isinstance(x, int):
            return x
        elif isinstance(x, str):
            return x
        else:
            raise TypeError("Invalid argument type")
    """
    return func

def final(cls):
    """
    Decorator to mark a class as final (cannot be subclassed).
    
    Usage:
    @final
    class MyClass:
        pass
    
    # This will raise an error
    class SubClass(MyClass):
        pass
    """
    return cls

def abstractmethod(func):
    """
    Decorator to mark a method as abstract.
    
    Usage:
    class MyAbstractClass:
        @abstractmethod
        def my_method(self):
            pass
    
    class MyConcreteClass(MyAbstractClass):
        def my_method(self):
            return "Implemented"
    """
    return func

def staticmethod(func):
    """
    Decorator to mark a method as static.
    
    Usage:
    class MyClass:
        @staticmethod
        def my_static_method(x, y):
            return x + y
    
    # Call without instantiating
    MyClass.my_static_method(1, 2)
    """
    return func

def classmethod(func):
    """
    Decorator to mark a method as a class method.
    
    Usage:
    class MyClass:
        @classmethod
        def my_class_method(cls, x):
            return cls.__name__ + str(x)
    
    # Call without instantiating
    MyClass.my_class_method(1)
    """
    return func

# Type checking utilities
def get_type(obj):
    """
    Get the type of an object.
    
    Args:
        obj: The object to get the type of.
        
    Returns:
        The type of the object.
    """
    return type(obj)

def is_instance(obj, type_):
    """
    Check if an object is an instance of a type.
    
    Args:
        obj: The object to check.
        type_: The type to check against.
        
    Returns:
        True if the object is an instance of the type, False otherwise.
    """
    return isinstance(obj, type_)

def is_subclass(cls, subclass):
    """
    Check if a class is a subclass of another class.
    
    Args:
        cls: The class to check.
        subclass: The class to check against.
        
    Returns:
        True if cls is a subclass of subclass, False otherwise.
    """
    return issubclass(cls, subclass)