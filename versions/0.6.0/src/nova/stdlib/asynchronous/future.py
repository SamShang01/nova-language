"""
Nova语言标准库Future模块
"""

class Future:
    """
    Future类，用于表示异步操作的结果
    """
    
    def __init__(self):
        """
        初始化Future
        """
        self._done = False
        self._result = None
        self._exception = None
        self._callbacks = []
    
    def done(self):
        """
        检查Future是否完成
        
        Returns:
            bool: 是否完成
        """
        return self._done
    
    def result(self):
        """
        获取Future的结果
        
        Returns:
            Any: 结果
        
        Raises:
            Exception: 如果Future有异常
        """
        if not self._done:
            raise ValueError("Future not done")
        if self._exception:
            raise self._exception
        return self._result
    
    def exception(self):
        """
        获取Future的异常
        
        Returns:
            Exception: 异常
        """
        if not self._done:
            raise ValueError("Future not done")
        return self._exception
    
    def add_done_callback(self, callback):
        """
        添加完成回调
        
        Args:
            callback: 回调函数
        """
        if self._done:
            callback(self)
        else:
            self._callbacks.append(callback)
    
    def set_result(self, result):
        """
        设置Future的结果
        
        Args:
            result: 结果
        """
        if self._done:
            raise ValueError("Future already done")
        self._result = result
        self._done = True
        self._notify_callbacks()
    
    def set_exception(self, exception):
        """
        设置Future的异常
        
        Args:
            exception: 异常
        """
        if self._done:
            raise ValueError("Future already done")
        self._exception = exception
        self._done = True
        self._notify_callbacks()
    
    def _notify_callbacks(self):
        """
        通知回调函数
        """
        for callback in self._callbacks:
            callback(self)
        self._callbacks = []
