"""
Nova语言虚拟机内存管理
"""

class MemoryManager:
    """
    内存管理器
    
    负责管理虚拟机的内存分配和释放
    """
    
    def __init__(self, heap_size=1024):
        """
        初始化内存管理器
        
        Args:
            heap_size: 堆大小
        """
        self.heap_size = heap_size
        self.heap = [None] * heap_size
        self.free_list = list(range(heap_size))
        self.allocated = {}
    
    def allocate(self, size):
        """
        分配内存
        
        Args:
            size: 内存大小
        
        Returns:
            int: 内存地址
        
        Raises:
            MemoryError: 如果内存不足
        """
        if size <= 0:
            raise ValueError("Size must be positive")
        
        if len(self.free_list) < size:
            raise MemoryError("Out of memory")
        
        # 如果空闲列表为空，直接返回
        if not self.free_list:
            raise MemoryError("Out of memory")
        
        # 排序空闲列表，确保连续内存分配
        self.free_list.sort()
        
        # 分配连续内存
        address = self.free_list[0]
        # 批量弹出，减少列表操作次数
        allocated = self.free_list[:size]
        self.free_list = self.free_list[size:]
        
        self.allocated[address] = size
        return address
    
    def free(self, address):
        """
        释放内存
        
        Args:
            address: 内存地址
        
        Raises:
            ValueError: 如果地址无效
        """
        if address not in self.allocated:
            raise ValueError(f"Invalid memory address: {address}")
        
        size = self.allocated.pop(address)
        # 释放内存并添加到空闲列表
        # 不立即排序，而是在分配时处理
        for i in range(size):
            self.free_list.append(address + i)
    
    def write(self, address, value):
        """
        写入内存
        
        Args:
            address: 内存地址
            value: 值
        
        Raises:
            ValueError: 如果地址无效
        """
        if address < 0 or address >= self.heap_size:
            raise ValueError(f"Invalid memory address: {address}")
        
        # 检查地址是否已分配
        # 使用更高效的检查方法
        valid = False
        # 遍历已分配的内存块
        for addr, size in self.allocated.items():
            if addr <= address < addr + size:
                valid = True
                break
        
        if not valid:
            raise ValueError(f"Memory address {address} not allocated")
        
        self.heap[address] = value
    
    def read(self, address):
        """
        读取内存
        
        Args:
            address: 内存地址
        
        Returns:
            Any: 内存值
        
        Raises:
            ValueError: 如果地址无效
        """
        if address < 0 or address >= self.heap_size:
            raise ValueError(f"Invalid memory address: {address}")
        
        # 检查地址是否已分配
        # 使用更高效的检查方法
        valid = False
        # 遍历已分配的内存块
        for addr, size in self.allocated.items():
            if addr <= address < addr + size:
                valid = True
                break
        
        if not valid:
            raise ValueError(f"Memory address {address} not allocated")
        
        return self.heap[address]
    
    def load(self, address):
        """
        加载内存值（与read相同）
        
        Args:
            address: 内存地址
        
        Returns:
            Any: 内存值
        """
        return self.read(address)
    
    def store(self, address, value):
        """
        存储内存值（与write相同）
        
        Args:
            address: 内存地址
            value: 值
        """
        self.write(address, value)
    
    def get_heap_usage(self):
        """
        获取堆使用情况
        
        Returns:
            tuple: (已使用大小, 总大小)
        """
        used = sum(self.allocated.values())
        return used, self.heap_size
    
    def get_free_memory(self):
        """
        获取空闲内存大小
        
        Returns:
            int: 空闲内存大小
        """
        return len(self.free_list)
