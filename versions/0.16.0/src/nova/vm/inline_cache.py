"""
Nova语言方法调用内联缓存

实现内联缓存优化，加速方法调用
"""

from typing import Dict, Optional, Any, Callable, Tuple
from enum import Enum


class CacheState(Enum):
    """
    缓存状态
    """
    UNINITIALIZED = 0
    MONOMORPHIC = 1
    POLYMORPHIC = 2
    MEGAMORPHIC = 3


class InlineCacheEntry:
    """
    内联缓存条目
    
    存储方法查找的缓存信息
    """
    
    def __init__(self, class_type: type, method_name: str, method: Callable):
        """
        初始化缓存条目
        
        Args:
            class_type: 类类型
            method_name: 方法名
            method: 方法对象
        """
        self.class_type = class_type
        self.method_name = method_name
        self.method = method
        self.hit_count = 0
        self.miss_count = 0
    
    def hit(self):
        """
        记录缓存命中
        """
        self.hit_count += 1
    
    def miss(self):
        """
        记录缓存未命中
        """
        self.miss_count += 1
    
    def get_hit_rate(self) -> float:
        """
        获取命中率
        
        Returns:
            float: 命中率
        """
        total = self.hit_count + self.miss_count
        if total == 0:
            return 0.0
        return self.hit_count / total
    
    def __repr__(self):
        """
        缓存条目的字符串表示
        """
        return (f"InlineCacheEntry(class={self.class_type.__name__}, "
                f"method={self.method_name}, "
                f"hits={self.hit_count}, "
                f"misses={self.miss_count}, "
                f"hit_rate={self.get_hit_rate():.2f})")


class InlineCache:
    """
    内联缓存
    
    管理方法调用的缓存
    """
    
    def __init__(self, max_entries: int = 4):
        """
        初始化内联缓存
        
        Args:
            max_entries: 最大缓存条目数
        """
        self.max_entries = max_entries
        self.entries: Dict[Tuple[type, str], InlineCacheEntry] = {}
        self.state = CacheState.UNINITIALIZED
        self.total_hits = 0
        self.total_misses = 0
    
    def lookup(self, obj: Any, method_name: str) -> Optional[Callable]:
        """
        查找方法
        
        Args:
            obj: 对象
            method_name: 方法名
        
        Returns:
            Optional[Callable]: 方法对象，如果未找到返回None
        """
        if obj is None:
            self.total_misses += 1
            return None
        
        class_type = type(obj)
        cache_key = (class_type, method_name)
        
        if cache_key in self.entries:
            # 缓存命中
            entry = self.entries[cache_key]
            entry.hit()
            self.total_hits += 1
            self._update_state()
            return entry.method
        else:
            # 缓存未命中
            self.total_misses += 1
            return None
    
    def update(self, obj: Any, method_name: str, method: Callable):
        """
        更新缓存
        
        Args:
            obj: 对象
            method_name: 方法名
            method: 方法对象
        """
        if obj is None:
            return
        
        class_type = type(obj)
        cache_key = (class_type, method_name)
        
        # 如果缓存已满，移除最旧的条目
        if len(self.entries) >= self.max_entries:
            self._evict_oldest_entry()
        
        # 创建新的缓存条目
        entry = InlineCacheEntry(class_type, method_name, method)
        self.entries[cache_key] = entry
        self._update_state()
    
    def _evict_oldest_entry(self):
        """
        淘汰最旧的缓存条目
        
        基于命中率进行淘汰
        """
        if not self.entries:
            return
        
        # 找到命中率最低的条目
        worst_entry_key = None
        worst_hit_rate = 1.0
        
        for key, entry in self.entries.items():
            hit_rate = entry.get_hit_rate()
            if hit_rate < worst_hit_rate:
                worst_hit_rate = hit_rate
                worst_entry_key = key
        
        if worst_entry_key:
            del self.entries[worst_entry_key]
    
    def _update_state(self):
        """
        更新缓存状态
        """
        num_entries = len(self.entries)
        
        if num_entries == 0:
            self.state = CacheState.UNINITIALIZED
        elif num_entries == 1:
            self.state = CacheState.MONOMORPHIC
        elif num_entries <= self.max_entries:
            self.state = CacheState.POLYMORPHIC
        else:
            self.state = CacheState.MEGAMORPHIC
    
    def get_hit_rate(self) -> float:
        """
        获取总体命中率
        
        Returns:
            float: 命中率
        """
        total = self.total_hits + self.total_misses
        if total == 0:
            return 0.0
        return self.total_hits / total
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息
        
        Returns:
            Dict: 统计信息
        """
        return {
            'state': self.state.name,
            'entries': len(self.entries),
            'max_entries': self.max_entries,
            'total_hits': self.total_hits,
            'total_misses': self.total_misses,
            'hit_rate': self.get_hit_rate(),
            'entries_detail': [
                {
                    'class': entry.class_type.__name__,
                    'method': entry.method_name,
                    'hits': entry.hit_count,
                    'misses': entry.miss_count,
                    'hit_rate': entry.get_hit_rate()
                }
                for entry in self.entries.values()
            ]
        }
    
    def clear(self):
        """
        清空缓存
        """
        self.entries.clear()
        self.state = CacheState.UNINITIALIZED
        self.total_hits = 0
        self.total_misses = 0
    
    def invalidate(self, class_type: type, method_name: Optional[str] = None):
        """
        使缓存失效
        
        Args:
            class_type: 类类型
            method_name: 方法名，如果为None则使该类的所有方法失效
        """
        if method_name is None:
            # 使该类的所有方法失效
            keys_to_remove = [
                key for key in self.entries.keys()
                if key[0] == class_type
            ]
            for key in keys_to_remove:
                del self.entries[key]
        else:
            # 使指定方法失效
            cache_key = (class_type, method_name)
            if cache_key in self.entries:
                del self.entries[cache_key]
        
        self._update_state()


class InlineCacheManager:
    """
    内联缓存管理器
    
    管理多个内联缓存实例
    """
    
    def __init__(self, max_caches: int = 100, max_entries_per_cache: int = 4):
        """
        初始化内联缓存管理器
        
        Args:
            max_caches: 最大缓存数量
            max_entries_per_cache: 每个缓存的最大条目数
        """
        self.max_caches = max_caches
        self.max_entries_per_cache = max_entries_per_cache
        self.caches: Dict[str, InlineCache] = {}
        self.global_hits = 0
        self.global_misses = 0
    
    def get_cache(self, cache_key: str) -> InlineCache:
        """
        获取或创建缓存
        
        Args:
            cache_key: 缓存键
        
        Returns:
            InlineCache: 缓存实例
        """
        if cache_key not in self.caches:
            # 如果缓存数量超过限制，移除最不常用的缓存
            if len(self.caches) >= self.max_caches:
                self._evict_least_used_cache()
            
            self.caches[cache_key] = InlineCache(self.max_entries_per_cache)
        
        return self.caches[cache_key]
    
    def _evict_least_used_cache(self):
        """
        淘汰最不常用的缓存
        """
        if not self.caches:
            return
        
        # 找到命中率最低的缓存
        worst_cache_key = None
        worst_hit_rate = 1.0
        
        for key, cache in self.caches.items():
            hit_rate = cache.get_hit_rate()
            if hit_rate < worst_hit_rate:
                worst_hit_rate = hit_rate
                worst_cache_key = key
        
        if worst_cache_key:
            del self.caches[worst_cache_key]
    
    def get_global_stats(self) -> Dict[str, Any]:
        """
        获取全局统计信息
        
        Returns:
            Dict: 全局统计信息
        """
        total_hits = sum(cache.total_hits for cache in self.caches.values())
        total_misses = sum(cache.total_misses for cache in self.caches.values())
        total = total_hits + total_misses
        
        return {
            'num_caches': len(self.caches),
            'max_caches': self.max_caches,
            'total_hits': total_hits,
            'total_misses': total_misses,
            'global_hit_rate': total_hits / total if total > 0 else 0.0,
            'caches': {
                key: cache.get_stats()
                for key, cache in self.caches.items()
            }
        }
    
    def clear_all(self):
        """
        清空所有缓存
        """
        for cache in self.caches.values():
            cache.clear()
        self.caches.clear()
        self.global_hits = 0
        self.global_misses = 0
    
    def print_stats(self):
        """
        打印统计信息
        """
        stats = self.get_global_stats()
        
        print("=== 内联缓存统计 ===")
        print(f"缓存数量: {stats['num_caches']}/{stats['max_caches']}")
        print(f"总命中次数: {stats['total_hits']}")
        print(f"总未命中次数: {stats['total_misses']}")
        print(f"全局命中率: {stats['global_hit_rate']:.2%}")
        
        if stats['num_caches'] > 0:
            print("\n=== 缓存详情 ===")
            for key, cache_stats in stats['caches'].items():
                print(f"\n缓存: {key}")
                print(f"  状态: {cache_stats['state']}")
                print(f"  条目数: {cache_stats['entries']}/{cache_stats['max_entries']}")
                print(f"  命中率: {cache_stats['hit_rate']:.2%}")
                
                if cache_stats['entries_detail']:
                    print("  条目详情:")
                    for entry in cache_stats['entries_detail']:
                        print(f"    {entry['class']}.{entry['method']}: "
                              f"命中率={entry['hit_rate']:.2%} "
                              f"(命中={entry['hits']}, 未命中={entry['misses']})")