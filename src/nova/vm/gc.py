"""
Nova语言分代垃圾回收器

实现基于分代的垃圾回收算法，提高内存管理效率
"""

import sys
import time
from typing import Set, Dict, List, Optional, Any
from enum import Enum


class Generation(Enum):
    """
    代枚举
    """
    YOUNG = 0
    OLD = 1


class GCStats:
    """
    垃圾回收统计信息
    """
    
    def __init__(self):
        self.total_collections = 0
        self.young_collections = 0
        self.old_collections = 0
        self.total_time = 0.0
        self.objects_collected = 0
        self.memory_freed = 0
        self.promotions = 0
    
    def reset(self):
        """
        重置统计信息
        """
        self.__init__()
    
    def __str__(self):
        """
        统计信息的字符串表示
        """
        return (f"GC Stats:\n"
                f"  Total collections: {self.total_collections}\n"
                f"  Young collections: {self.young_collections}\n"
                f"  Old collections: {self.old_collections}\n"
                f"  Total time: {self.total_time:.3f}s\n"
                f"  Objects collected: {self.objects_collected}\n"
                f"  Memory freed: {self.memory_freed} bytes\n"
                f"  Promotions: {self.promotions}")


class GenerationalGC:
    """
    分代垃圾回收器
    
    实现基于分代的垃圾回收算法，提高内存管理效率
    """
    
    def __init__(self, young_generation_size=1024, old_generation_size=4096):
        """
        初始化分代垃圾回收器
        
        Args:
            young_generation_size: 新生代大小
            old_generation_size: 老生代大小
        """
        # 代配置
        self.young_gen_size = young_generation_size
        self.old_gen_size = old_generation_size
        
        # 对象存储
        self.young_objects: Dict[int, Dict] = {}
        self.old_objects: Dict[int, Dict] = {}
        
        # 引用跟踪
        self.references: Dict[int, Set[int]] = {}
        self.reverse_references: Dict[int, Set[int]] = {}
        
        # 对象年龄跟踪
        self.object_ages: Dict[int, int] = {}
        
        # 统计信息
        self.stats = GCStats()
        
        # 配置参数
        self.promotion_age = 3  # 对象在新生代存活3次GC后晋升到老生代
        self.young_gc_threshold = 0.8  # 新生代使用率达到80%时触发GC
        self.old_gc_threshold = 0.9  # 老生代使用率达到90%时触发GC
        
        # 根集合
        self.roots: Set[int] = set()
        
        # 对象ID计数器
        self.next_object_id = 1
    
    def allocate(self, obj: Any, generation: Generation = Generation.YOUNG) -> int:
        """
        分配对象
        
        Args:
            obj: 要分配的对象
            generation: 分配的代
        
        Returns:
            int: 对象ID
        
        Raises:
            MemoryError: 如果内存不足
        """
        object_id = self.next_object_id
        self.next_object_id += 1
        
        obj_info = {
            'value': obj,
            'size': sys.getsizeof(obj),
            'allocated_at': time.time(),
            'generation': generation
        }
        
        if generation == Generation.YOUNG:
            if len(self.young_objects) >= self.young_gen_size:
                self._collect_young()
            
            if len(self.young_objects) >= self.young_gen_size:
                raise MemoryError("Young generation full")
            
            self.young_objects[object_id] = obj_info
            self.object_ages[object_id] = 0
        else:
            if len(self.old_objects) >= self.old_gen_size:
                self._collect_old()
            
            if len(self.old_objects) >= self.old_gen_size:
                raise MemoryError("Old generation full")
            
            self.old_objects[object_id] = obj_info
            self.object_ages[object_id] = self.promotion_age
        
        self.references[object_id] = set()
        self.reverse_references[object_id] = set()
        
        return object_id
    
    def add_reference(self, from_id: int, to_id: int):
        """
        添加引用关系
        
        Args:
            from_id: 引用者对象ID
            to_id: 被引用对象ID
        """
        if from_id not in self.references:
            self.references[from_id] = set()
        if to_id not in self.reverse_references:
            self.reverse_references[to_id] = set()
        
        self.references[from_id].add(to_id)
        self.reverse_references[to_id].add(from_id)
    
    def remove_reference(self, from_id: int, to_id: int):
        """
        移除引用关系
        
        Args:
            from_id: 引用者对象ID
            to_id: 被引用对象ID
        """
        if from_id in self.references and to_id in self.references[from_id]:
            self.references[from_id].remove(to_id)
        if to_id in self.reverse_references and from_id in self.reverse_references[to_id]:
            self.reverse_references[to_id].remove(from_id)
    
    def add_root(self, object_id: int):
        """
        添加根对象
        
        Args:
            object_id: 对象ID
        """
        self.roots.add(object_id)
    
    def remove_root(self, object_id: int):
        """
        移除根对象
        
        Args:
            object_id: 对象ID
        """
        self.roots.discard(object_id)
    
    def _collect_young(self):
        """
        收集新生代垃圾
        
        使用复制算法，快速回收新生代垃圾
        """
        start_time = time.time()
        
        # 标记阶段
        marked = self._mark_from_roots(generation=Generation.YOUNG)
        
        # 复制存活对象到新的新生代
        new_young_objects = {}
        new_object_ages = {}
        
        for obj_id, obj_info in self.young_objects.items():
            if obj_id in marked:
                # 对象存活
                new_object_ages[obj_id] = self.object_ages[obj_id] + 1
                
                # 检查是否需要晋升
                if new_object_ages[obj_id] >= self.promotion_age:
                    # 晋升到老生代
                    if len(self.old_objects) < self.old_gen_size:
                        self.old_objects[obj_id] = obj_info
                        self.old_objects[obj_id]['generation'] = Generation.OLD
                        self.stats.promotions += 1
                    else:
                        # 老生代已满，保留在新生代
                        new_young_objects[obj_id] = obj_info
                else:
                    # 保留在新生代
                    new_young_objects[obj_id] = obj_info
            else:
                # 对象死亡
                self._cleanup_object(obj_id)
                self.stats.objects_collected += 1
                self.stats.memory_freed += obj_info['size']
        
        self.young_objects = new_young_objects
        self.object_ages.update(new_object_ages)
        
        # 更新统计信息
        self.stats.total_collections += 1
        self.stats.young_collections += 1
        self.stats.total_time += time.time() - start_time
    
    def _collect_old(self):
        """
        收集老生代垃圾
        
        使用标记-清除算法，全面回收老生代垃圾
        """
        start_time = time.time()
        
        # 标记阶段
        marked = self._mark_from_roots(generation=Generation.OLD)
        
        # 清除阶段
        to_remove = []
        for obj_id, obj_info in self.old_objects.items():
            if obj_id not in marked:
                to_remove.append(obj_id)
                self._cleanup_object(obj_id)
                self.stats.objects_collected += 1
                self.stats.memory_freed += obj_info['size']
        
        for obj_id in to_remove:
            del self.old_objects[obj_id]
            if obj_id in self.object_ages:
                del self.object_ages[obj_id]
        
        # 更新统计信息
        self.stats.total_collections += 1
        self.stats.old_collections += 1
        self.stats.total_time += time.time() - start_time
    
    def _mark_from_roots(self, generation: Generation) -> Set[int]:
        """
        从根对象开始标记
        
        Args:
            generation: 要标记的代
        
        Returns:
            Set[int]: 标记的对象ID集合
        """
        marked = set()
        worklist = list(self.roots)
        
        while worklist:
            obj_id = worklist.pop()
            
            if obj_id in marked:
                continue
            
            # 检查对象是否在指定的代中
            if generation == Generation.YOUNG and obj_id not in self.young_objects:
                continue
            if generation == Generation.OLD and obj_id not in self.old_objects:
                continue
            
            marked.add(obj_id)
            
            # 添加引用的对象到工作列表
            if obj_id in self.references:
                for ref_id in self.references[obj_id]:
                    if ref_id not in marked:
                        worklist.append(ref_id)
        
        return marked
    
    def _cleanup_object(self, obj_id: int):
        """
        清理对象
        
        Args:
            obj_id: 对象ID
        """
        # 移除引用关系
        if obj_id in self.references:
            for ref_id in self.references[obj_id]:
                if ref_id in self.reverse_references:
                    self.reverse_references[ref_id].discard(obj_id)
            del self.references[obj_id]
        
        if obj_id in self.reverse_references:
            for ref_id in self.reverse_references[obj_id]:
                if ref_id in self.references:
                    self.references[ref_id].discard(obj_id)
            del self.reverse_references[obj_id]
    
    def collect(self, generation: Optional[Generation] = None):
        """
        执行垃圾回收
        
        Args:
            generation: 要回收的代，None表示自动选择
        """
        if generation is None:
            # 自动选择要回收的代
            young_usage = len(self.young_objects) / self.young_gen_size
            old_usage = len(self.old_objects) / self.old_gen_size
            
            if young_usage >= self.young_gc_threshold:
                self._collect_young()
            elif old_usage >= self.old_gc_threshold:
                self._collect_old()
        elif generation == Generation.YOUNG:
            self._collect_young()
        elif generation == Generation.OLD:
            self._collect_old()
    
    def get_stats(self) -> GCStats:
        """
        获取垃圾回收统计信息
        
        Returns:
            GCStats: 统计信息
        """
        return self.stats
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        获取内存使用情况
        
        Returns:
            Dict: 内存使用信息
        """
        young_usage = len(self.young_objects) / self.young_gen_size
        old_usage = len(self.old_objects) / self.old_gen_size
        
        young_memory = sum(obj['size'] for obj in self.young_objects.values())
        old_memory = sum(obj['size'] for obj in self.old_objects.values())
        
        return {
            'young_generation': {
                'count': len(self.young_objects),
                'capacity': self.young_gen_size,
                'usage': young_usage,
                'memory': young_memory
            },
            'old_generation': {
                'count': len(self.old_objects),
                'capacity': self.old_gen_size,
                'usage': old_usage,
                'memory': old_memory
            },
            'total_objects': len(self.young_objects) + len(self.old_objects),
            'total_memory': young_memory + old_memory
        }
    
    def reset(self):
        """
        重置垃圾回收器
        """
        self.young_objects.clear()
        self.old_objects.clear()
        self.references.clear()
        self.reverse_references.clear()
        self.object_ages.clear()
        self.roots.clear()
        self.next_object_id = 1
        self.stats.reset()