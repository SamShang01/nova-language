"""
Nova性能分析工具 - 执行时间统计、内存使用分析、热点识别
"""

import time
import sys
import os
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import json


class PerformanceStats:
    """
    性能统计类
    """
    
    def __init__(self):
        """
        初始化性能统计
        """
        self.function_calls: Dict[str, List[float]] = defaultdict(list)
        self.function_depths: Dict[str, int] = {}
        self.total_time = 0.0
        self.memory_usage: Dict[str, List[float]] = defaultdict(list)
        self.call_stack: List[Tuple[str, float]] = []
        self.current_depth = 0
    
    def record_function_call(self, function_name: str, duration: float):
        """
        记录函数调用
        
        Args:
            function_name: 函数名
            duration: 执行时间（秒）
        """
        self.function_calls[function_name].append(duration)
        self.total_time += duration
    
    def record_memory_usage(self, function_name: str, memory_mb: float):
        """
        记录内存使用
        
        Args:
            function_name: 函数名
            memory_mb: 内存使用量（MB）
        """
        self.memory_usage[function_name].append(memory_mb)
    
    def get_function_stats(self, function_name: str) -> Dict:
        """
        获取函数统计信息
        
        Args:
            function_name: 函数名
        
        Returns:
            Dict: 统计信息
        """
        if function_name not in self.function_calls:
            return {}
        
        calls = self.function_calls[function_name]
        total_time = sum(calls)
        avg_time = total_time / len(calls)
        min_time = min(calls)
        max_time = max(calls)
        
        stats = {
            'name': function_name,
            'call_count': len(calls),
            'total_time': total_time,
            'avg_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'percentage': (total_time / self.total_time * 100) if self.total_time > 0 else 0
        }
        
        if function_name in self.memory_usage:
            mem_calls = self.memory_usage[function_name]
            stats['avg_memory'] = sum(mem_calls) / len(mem_calls)
            stats['max_memory'] = max(mem_calls)
        
        return stats
    
    def get_all_stats(self) -> List[Dict]:
        """
        获取所有函数统计信息
        
        Returns:
            List[Dict]: 统计信息列表
        """
        stats = []
        for function_name in self.function_calls:
            stats.append(self.get_function_stats(function_name))
        
        stats.sort(key=lambda x: x['total_time'], reverse=True)
        return stats
    
    def get_hotspots(self, threshold: float = 5.0) -> List[Dict]:
        """
        获取热点函数
        
        Args:
            threshold: 时间百分比阈值
        
        Returns:
            List[Dict]: 热点函数列表
        """
        stats = self.get_all_stats()
        hotspots = [s for s in stats if s['percentage'] >= threshold]
        return hotspots
    
    def print_summary(self):
        """
        打印性能摘要
        """
        print("\n" + "=" * 60)
        print("性能分析摘要")
        print("=" * 60)
        print(f"总执行时间: {self.total_time:.6f} 秒")
        print(f"函数调用总数: {sum(len(calls) for calls in self.function_calls.values())}")
        print(f"唯一函数数: {len(self.function_calls)}")
        print()
    
    def print_function_stats(self, limit: int = 10):
        """
        打印函数统计信息
        
        Args:
            limit: 显示的函数数量限制
        """
        stats = self.get_all_stats()[:limit]
        
        print("\n" + "=" * 60)
        print("函数性能统计")
        print("=" * 60)
        print(f"{'函数名':<30} {'调用次数':<10} {'总时间':<12} {'平均时间':<12} {'占比':<10}")
        print("-" * 60)
        
        for stat in stats:
            print(f"{stat['name']:<30} {stat['call_count']:<10} "
                  f"{stat['total_time']:<12.6f} {stat['avg_time']:<12.6f} "
                  f"{stat['percentage']:<10.2f}%")
    
    def print_hotspots(self, threshold: float = 5.0):
        """
        打印热点函数
        
        Args:
            threshold: 时间百分比阈值
        """
        hotspots = self.get_hotspots(threshold)
        
        if not hotspots:
            print(f"\n没有找到热点函数（阈值: {threshold}%）")
            return
        
        print("\n" + "=" * 60)
        print(f"热点函数（时间占比 >= {threshold}%）")
        print("=" * 60)
        
        for i, hotspot in enumerate(hotspots, 1):
            print(f"\n{i}. {hotspot['name']}")
            print(f"   调用次数: {hotspot['call_count']}")
            print(f"   总时间: {hotspot['total_time']:.6f} 秒")
            print(f"   平均时间: {hotspot['avg_time']:.6f} 秒")
            print(f"   时间占比: {hotspot['percentage']:.2f}%")
            
            if 'avg_memory' in hotspot:
                print(f"   平均内存: {hotspot['avg_memory']:.2f} MB")
                print(f"   最大内存: {hotspot['max_memory']:.2f} MB")
    
    def print_memory_stats(self, limit: int = 10):
        """
        打印内存统计信息
        
        Args:
            limit: 显示的函数数量限制
        """
        if not self.memory_usage:
            print("\n没有内存使用数据")
            return
        
        print("\n" + "=" * 60)
        print("内存使用统计")
        print("=" * 60)
        
        memory_stats = []
        for function_name, mem_calls in self.memory_usage.items():
            avg_mem = sum(mem_calls) / len(mem_calls)
            max_mem = max(mem_calls)
            memory_stats.append({
                'name': function_name,
                'avg_memory': avg_mem,
                'max_memory': max_mem,
                'call_count': len(mem_calls)
            })
        
        memory_stats.sort(key=lambda x: x['max_memory'], reverse=True)
        memory_stats = memory_stats[:limit]
        
        print(f"{'函数名':<30} {'调用次数':<10} {'平均内存':<12} {'最大内存':<12}")
        print("-" * 60)
        
        for stat in memory_stats:
            print(f"{stat['name']:<30} {stat['call_count']:<10} "
                  f"{stat['avg_memory']:<12.2f} {stat['max_memory']:<12.2f} MB")
    
    def export_to_json(self, file_path: str):
        """
        导出统计信息到JSON文件
        
        Args:
            file_path: 文件路径
        """
        data = {
            'total_time': self.total_time,
            'function_stats': self.get_all_stats(),
            'hotspots': self.get_hotspots(),
            'memory_stats': [
                {
                    'name': name,
                    'avg_memory': sum(calls) / len(calls),
                    'max_memory': max(calls),
                    'call_count': len(calls)
                }
                for name, calls in self.memory_usage.items()
            ]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n性能统计已导出到: {file_path}")


class Profiler:
    """
    性能分析器
    
    功能：
    - 执行时间统计
    - 内存使用分析
    - 热点识别
    """
    
    def __init__(self):
        """
        初始化性能分析器
        """
        self.stats = PerformanceStats()
        self.enabled = True
        self.current_function: Optional[str] = None
        self.start_time: Optional[float] = None
    
    def start_profiling(self):
        """
        开始性能分析
        """
        self.enabled = True
        self.stats = PerformanceStats()
        print("性能分析已启动")
    
    def stop_profiling(self):
        """
        停止性能分析
        """
        self.enabled = False
        print("性能分析已停止")
    
    def enter_function(self, function_name: str):
        """
        进入函数
        
        Args:
            function_name: 函数名
        """
        if not self.enabled:
            return
        
        self.current_function = function_name
        self.start_time = time.time()
        self.stats.current_depth += 1
    
    def exit_function(self, function_name: str):
        """
        退出函数
        
        Args:
            function_name: 函数名
        """
        if not self.enabled or self.start_time is None:
            return
        
        duration = time.time() - self.start_time
        self.stats.record_function_call(function_name, duration)
        
        memory_mb = self._get_memory_usage()
        if memory_mb > 0:
            self.stats.record_memory_usage(function_name, memory_mb)
        
        self.current_function = None
        self.start_time = None
        self.stats.current_depth -= 1
    
    def _get_memory_usage(self) -> float:
        """
        获取内存使用量
        
        Returns:
            float: 内存使用量（MB）
        """
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0
    
    def report(self, show_summary: bool = True, show_functions: bool = True,
              show_hotspots: bool = True, show_memory: bool = True,
              hotspot_threshold: float = 5.0, function_limit: int = 10):
        """
        生成性能报告
        
        Args:
            show_summary: 是否显示摘要
            show_functions: 是否显示函数统计
            show_hotspots: 是否显示热点
            show_memory: 是否显示内存统计
            hotspot_threshold: 热点阈值
            function_limit: 函数显示限制
        """
        if show_summary:
            self.stats.print_summary()
        
        if show_functions:
            self.stats.print_function_stats(function_limit)
        
        if show_hotspots:
            self.stats.print_hotspots(hotspot_threshold)
        
        if show_memory:
            self.stats.print_memory_stats(function_limit)
    
    def export_report(self, file_path: str):
        """
        导出性能报告
        
        Args:
            file_path: 文件路径
        """
        self.stats.export_to_json(file_path)
    
    def get_stats(self) -> PerformanceStats:
        """
        获取性能统计
        
        Returns:
            PerformanceStats: 性能统计对象
        """
        return self.stats


def profile_function(profiler: Profiler):
    """
    函数性能分析装饰器
    
    Args:
        profiler: 性能分析器
    
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            profiler.enter_function(func.__name__)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                profiler.exit_function(func.__name__)
        return wrapper
    return decorator


def main():
    """
    主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Nova性能分析工具')
    parser.add_argument('--threshold', type=float, default=5.0,
                       help='热点函数时间百分比阈值（默认: 5.0%%）')
    parser.add_argument('--limit', type=int, default=10,
                       help='显示的函数数量限制（默认: 10）')
    parser.add_argument('--no-hotspots', action='store_true',
                       help='不显示热点函数')
    parser.add_argument('--no-memory', action='store_true',
                       help='不显示内存统计')
    parser.add_argument('--export', type=str,
                       help='导出报告到JSON文件')
    
    args = parser.parse_args()
    
    profiler = Profiler()
    
    print("Nova性能分析工具 v0.2.0")
    print("=" * 60)
    
    profiler.report(
        show_summary=True,
        show_functions=True,
        show_hotspots=not args.no_hotspots,
        show_memory=not args.no_memory,
        hotspot_threshold=args.threshold,
        function_limit=args.limit
    )
    
    if args.export:
        profiler.export_report(args.export)


if __name__ == '__main__':
    main()
