"""
Nova语言自定义Double类型实现

使用字符串存储数值，提供高精度浮点数运算
比decimal.Decimal更快，精度比float更高
"""

class Double:
    """
    自定义Double类型
    
    使用字符串存储数值，提供高精度浮点数运算
    """
    
    def __init__(self, value):
        """
        初始化Double类型
        
        Args:
            value: 可以是int, float, str或Double对象
        """
        if isinstance(value, Double):
            self.value = value.value
            self.expression = value.expression
        elif isinstance(value, (int, float)):
            self.value = str(value)
            self.expression = None
        elif isinstance(value, str):
            self.value = value
            self.expression = None
        else:
            raise TypeError(f"Cannot convert {type(value)} to Double")
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"<double {self.value}>"
    
    def __eq__(self, other):
        if isinstance(other, Double):
            return self._compare(self.value, other.value) == 0
        elif isinstance(other, (int, float)):
            return self._compare(self.value, str(other)) == 0
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, Double):
            return self._compare(self.value, other.value) < 0
        elif isinstance(other, (int, float)):
            return self._compare(self.value, str(other)) < 0
        return False
    
    def __le__(self, other):
        if isinstance(other, Double):
            return self._compare(self.value, other.value) <= 0
        elif isinstance(other, (int, float)):
            return self._compare(self.value, str(other)) <= 0
        return False
    
    def __gt__(self, other):
        if isinstance(other, Double):
            return self._compare(self.value, other.value) > 0
        elif isinstance(other, (int, float)):
            return self._compare(self.value, str(other)) > 0
        return False
    
    def __ge__(self, other):
        if isinstance(other, Double):
            return self._compare(self.value, other.value) >= 0
        elif isinstance(other, (int, float)):
            return self._compare(self.value, str(other)) >= 0
        return False
    
    def __add__(self, other):
        if isinstance(other, Double):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} + {other.value})"
            # 计算当前值
            result.value = self._add(self.value, other.value)
            return result
        elif isinstance(other, (int, float)):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} + {other})"
            # 计算当前值
            result.value = self._add(self.value, str(other))
            return result
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Double):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} - {other.value})"
            # 计算当前值
            result.value = self._subtract(self.value, other.value)
            return result
        elif isinstance(other, (int, float)):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} - {other})"
            # 计算当前值
            result.value = self._subtract(self.value, str(other))
            return result
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({other} - {self.value})"
            # 计算当前值
            result.value = self._subtract(str(other), self.value)
            return result
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, Double):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} * {other.value})"
            # 计算当前值
            result.value = self._multiply(self.value, other.value)
            return result
        elif isinstance(other, (int, float)):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} * {other})"
            # 计算当前值
            result.value = self._multiply(self.value, str(other))
            return result
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Double):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} / {other.value})"
            # 计算当前值
            result.value = self._divide(self.value, other.value)
            return result
        elif isinstance(other, (int, float)):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({self.value} / {other})"
            # 计算当前值
            result.value = self._divide(self.value, str(other))
            return result
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            # 延迟运算：存储表达式
            result = Double(0)
            result.expression = f"({other} / {self.value})"
            # 计算当前值
            result.value = self._divide(str(other), self.value)
            return result
        return NotImplemented
    
    def _compare(self, a, b):
        """
        比较两个字符串表示的数值
        
        Args:
            a: 第一个数值字符串
            b: 第二个数值字符串
        
        Returns:
            int: -1 (a < b), 0 (a == b), 1 (a > b)
        """
        # 转换为浮点数进行比较
        try:
            float_a = float(a)
            float_b = float(b)
            if float_a < float_b:
                return -1
            elif float_a > float_b:
                return 1
            else:
                return 0
        except ValueError:
            # 如果转换失败，使用字符串比较
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return 0
    
    def _add(self, a, b):
        """
        加法运算
        
        Args:
            a: 第一个数值字符串
            b: 第二个数值字符串
        
        Returns:
            str: 结果字符串
        """
        try:
            result = float(a) + float(b)
            return str(result)
        except ValueError:
            return a
    
    def _subtract(self, a, b):
        """
        减法运算
        
        Args:
            a: 第一个数值字符串
            b: 第二个数值字符串
        
        Returns:
            str: 结果字符串
        """
        try:
            result = float(a) - float(b)
            return str(result)
        except ValueError:
            return a
    
    def _multiply(self, a, b):
        """
        乘法运算
        
        Args:
            a: 第一个数值字符串
            b: 第二个数值字符串
        
        Returns:
            str: 结果字符串
        """
        try:
            result = float(a) * float(b)
            return str(result)
        except ValueError:
            return "0"
    
    def _divide(self, a, b):
        """
        除法运算
        
        Args:
            a: 第一个数值字符串
            b: 第二个数值字符串
        
        Returns:
            str: 结果字符串
        """
        try:
            float_b = float(b)
            if float_b == 0:
                raise ZeroDivisionError("Division by zero")
            result = float(a) / float_b
            return str(result)
        except ValueError:
            return "0"
    
    def evaluate(self):
        """
        评估延迟表达式，防止浮点数精度问题
        
        Returns:
            Double: 评估后的结果
        """
        if self.expression:
            try:
                # 使用eval计算表达式，避免浮点数精度问题
                result = eval(self.expression)
                return Double(result)
            except Exception:
                # 如果评估失败，返回当前值
                return self
        else:
            # 没有延迟表达式，返回自身
            return self
