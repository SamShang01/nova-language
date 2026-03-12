"""
Nova语言标准库Task模块
"""

from .future import Future

class Task(Future):
    """
    Task类，用于表示异步任务
    """
    
    def __init__(self, coroutine):
        """
        初始化Task
        
        Args:
            coroutine: 协程对象
        """
        super().__init__()
        self.coroutine = coroutine
        self._state = 'pending'
    
    def state(self):
        """
        获取Task的状态
        
        Returns:
            str: 状态
        """
        return self._state
    
    def cancel(self):
        """
        取消Task
        
        Returns:
            bool: 是否成功取消
        """
        if self._state == 'pending':
            self._state = 'cancelled'
            self.set_exception(CancelledError())
            return True
        return False
    
    def _step(self, value=None):
        """
        执行协程的一步
        
        Args:
            value: 传递给协程的值
        """
        try:
            if self._state == 'cancelled':
                return
            
            self._state = 'running'
            result = self.coroutine.send(value)
            
            # 处理协程的结果
            if isinstance(result, Future):
                # 如果是Future，等待其完成
                result.add_done_callback(self._future_done)
            else:
                # 如果是其他值，继续执行
                self._step(result)
        except StopIteration as e:
            # 协程完成
            self._state = 'done'
            self.set_result(e.value)
        except Exception as e:
            # 协程异常
            self._state = 'done'
            self.set_exception(e)
    
    def _future_done(self, future):
        """
        Future完成回调
        
        Args:
            future: Future对象
        """
        try:
            result = future.result()
            self._step(result)
        except Exception as e:
            self._step(e)
    
    def start(self):
        """
        开始执行Task
        """
        if self._state == 'pending':
            self._step()

class CancelledError(Exception):
    """
    取消错误
    """
    pass

# 便捷函数
def create_task(coroutine):
    """
    创建Task
    
    Args:
        coroutine: 协程对象
    
    Returns:
        Task: Task对象
    """
    task = Task(coroutine)
    task.start()
    return task

def async_func(func):
    """
    异步函数装饰器
    
    Args:
        func: 函数
    
    Returns:
        function: 异步函数
    """
    def wrapper(*args, **kwargs):
        return create_task(func(*args, **kwargs))
    return wrapper

def awaitable(obj):
    """
    检查对象是否可等待
    
    Args:
        obj: 对象
    
    Returns:
        bool: 是否可等待
    """
    return hasattr(obj, '__await__')

# 模拟await关键字
def await_(obj):
    """
    等待可等待对象
    
    Args:
        obj: 可等待对象
    
    Returns:
        Any: 结果
    """
    if isinstance(obj, Future):
        if not obj.done():
            # 这里需要在事件循环中处理
            # 简化实现，直接返回结果
            pass
        return obj.result()
    elif awaitable(obj):
        # 处理其他可等待对象
        return next(obj.__await__())
    else:
        return obj

__all__ = ['Task', 'create_task', 'async_func', 'await_', 'awaitable', 'CancelledError']
