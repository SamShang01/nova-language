"""
Nova语言异步执行器

实现async/await异步语法支持
"""

import asyncio
import inspect
from typing import Any, Coroutine, Callable, Optional, Dict
from enum import Enum


class AsyncState(Enum):
    """
    异步状态
    """
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    FAILED = 3


class AsyncResult:
    """
    异步结果
    
    表示异步操作的结果
    """
    
    def __init__(self):
        self.state = AsyncState.PENDING
        self.value = None
        self.exception = None
        self._callbacks = []
    
    def set_value(self, value: Any):
        """
        设置结果值
        
        Args:
            value: 结果值
        """
        self.state = AsyncState.COMPLETED
        self.value = value
        self._notify_callbacks()
    
    def set_exception(self, exception: Exception):
        """
        设置异常
        
        Args:
            exception: 异常对象
        """
        self.state = AsyncState.FAILED
        self.exception = exception
        self._notify_callbacks()
    
    def add_callback(self, callback: Callable):
        """
        添加回调函数
        
        Args:
            callback: 回调函数
        """
        if self.state == AsyncState.COMPLETED or self.state == AsyncState.FAILED:
            callback(self)
        else:
            self._callbacks.append(callback)
    
    def _notify_callbacks(self):
        """
        通知所有回调函数
        """
        for callback in self._callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def await_result(self):
        """
        等待结果
        
        Returns:
            Any: 结果值
        
        Raises:
            Exception: 如果异步操作失败
        """
        if self.state == AsyncState.PENDING or self.state == AsyncState.RUNNING:
            raise RuntimeError("Async operation is still pending")
        
        if self.state == AsyncState.FAILED:
            raise self.exception
        
        return self.value
    
    def __repr__(self):
        """
        异步结果的字符串表示
        """
        return (f"AsyncResult(state={self.state.name}, "
                f"value={self.value}, "
                f"exception={self.exception})")


class AsyncFunction:
    """
    异步函数包装器
    
    将普通函数包装为异步函数
    """
    
    def __init__(self, func: Callable):
        """
        初始化异步函数包装器
        
        Args:
            func: 要包装的函数
        """
        self.func = func
        self.name = func.__name__
    
    def __call__(self, *args, **kwargs) -> AsyncResult:
        """
        调用异步函数
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            AsyncResult: 异步结果
        """
        result = AsyncResult()
        
        async def async_wrapper():
            try:
                value = await self._execute_async(*args, **kwargs)
                result.set_value(value)
            except Exception as e:
                result.set_exception(e)
        
        # 在事件循环中运行异步任务
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果事件循环正在运行，创建任务
                asyncio.create_task(async_wrapper())
            else:
                # 如果事件循环没有运行，运行直到完成
                loop.run_until_complete(async_wrapper())
        except RuntimeError:
            # 没有事件循环，创建新的
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(async_wrapper())
            loop.close()
        
        return result
    
    async def _execute_async(self, *args, **kwargs) -> Any:
        """
        执行异步操作
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            Any: 执行结果
        """
        if inspect.iscoroutinefunction(self.func):
            # 如果函数本身就是协程，直接调用
            return await self.func(*args, **kwargs)
        else:
            # 如果是普通函数，在线程池中执行
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: self.func(*args, **kwargs))
    
    def __repr__(self):
        """
        异步函数的字符串表示
        """
        return f"<async function '{self.name}'>"


class AsyncExecutor:
    """
    异步执行器
    
    管理异步任务的执行
    """
    
    def __init__(self):
        """
        初始化异步执行器
        """
        self.tasks: Dict[str, AsyncResult] = {}
        self.event_loop = None
    
    def create_async_function(self, func: Callable) -> AsyncFunction:
        """
        创建异步函数
        
        Args:
            func: 要包装的函数
        
        Returns:
            AsyncFunction: 异步函数包装器
        """
        return AsyncFunction(func)
    
    async def await_all(self, *results: AsyncResult) -> list:
        """
        等待所有异步结果
        
        Args:
            *results: 异步结果列表
        
        Returns:
            list: 所有结果值
        """
        async def wait_for_result(result: AsyncResult):
            while result.state == AsyncState.PENDING or result.state == AsyncState.RUNNING:
                await asyncio.sleep(0.01)
            
            if result.state == AsyncState.FAILED:
                raise result.exception
            
            return result.value
        
        tasks = [asyncio.create_task(wait_for_result(r)) for r in results]
        return await asyncio.gather(*tasks)
    
    async def await_any(self, *results: AsyncResult) -> Any:
        """
        等待任意一个异步结果
        
        Args:
            *results: 异步结果列表
        
        Returns:
            Any: 第一个完成的结果值
        """
        async def wait_for_result(result: AsyncResult):
            while result.state == AsyncState.PENDING or result.state == AsyncState.RUNNING:
                await asyncio.sleep(0.01)
            
            if result.state == AsyncState.FAILED:
                raise result.exception
            
            return result.value
        
        done, _ = await asyncio.wait([wait_for_result(r) for r in results], return_when=asyncio.FIRST_COMPLETED)
            task = list(done)[0]
            if task.exception():
                raise task.exception()
            return task.result()
    
    def run_event_loop(self):
        """
        运行事件循环
        
        这个方法应该在主程序中调用，保持事件循环运行
        """
        if self.event_loop is None:
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
        
        if not self.event_loop.is_running():
            self.event_loop.run_forever()
    
    def stop_event_loop(self):
        """
        停止事件循环
        """
        if self.event_loop:
            self.event_loop.stop()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取执行器统计信息
        
        Returns:
            Dict: 统计信息
        """
        total = len(self.tasks)
        pending = sum(1 for r in self.tasks.values() if r.state == AsyncState.PENDING)
        running = sum(1 for r in self.tasks.values() if r.state == AsyncState.RUNNING)
        completed = sum(1 for r in self.tasks.values() if r.state == AsyncState.COMPLETED)
        failed = sum(1 for r in self.tasks.values() if r.state == AsyncState.FAILED)
        
        return {
            'total_tasks': total,
            'pending': pending,
            'running': running,
            'completed': completed,
            'failed': failed
        }


# 全局异步执行器实例
_global_executor = None


def get_global_executor() -> AsyncExecutor:
    """
    获取全局异步执行器
    
    Returns:
        AsyncExecutor: 全局异步执行器
    """
    global _global_executor
    if _global_executor is None:
        _global_executor = AsyncExecutor()
    return _global_executor


def async_func(func: Callable) -> AsyncFunction:
    """
    异步函数装饰器
    
    Args:
        func: 要装饰的函数
    
    Returns:
        AsyncFunction: 异步函数包装器
    
    Example:
        @async_func
        def my_async_function(x):
            return x * 2
        
        result = my_async_function(5)
        value = result.await_result()  # 10
    """
    return AsyncFunction(func)