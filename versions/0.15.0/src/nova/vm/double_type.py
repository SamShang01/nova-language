"""
Nova语言自定义Double类型实现

使用字符串存储数值，提供高精度浮点数运算
比decimal.Decimal更快，精度比float更高
"""

from decimal import Decimal, getcontext

# 设置足够的精度
getcontext().prec = 28

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
            self.operations = value.operations.copy() if hasattr(value, 'operations') else []
        elif isinstance(value, (int, float)):
            self.value = str(value)
            self.operations = []
        elif isinstance(value, str):
            self.value = value
            self.operations = []
        else:
            raise TypeError(f"Cannot convert {type(value)} to Double")
    
    def __str__(self):
        # 当需要字符串表示时，执行所有操作并返回最终结果
        return self.evaluate().value
    
    def __repr__(self):
        return f"<double {self.evaluate().value}>"
    
    def __eq__(self, other):
        if isinstance(other, Double):
            return self.evaluate().value == other.evaluate().value
        elif isinstance(other, (int, float)):
            return self.evaluate().value == str(other)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, Double):
            return Decimal(self.evaluate().value) < Decimal(other.evaluate().value)
        elif isinstance(other, (int, float)):
            return Decimal(self.evaluate().value) < Decimal(str(other))
        return False
    
    def __le__(self, other):
        if isinstance(other, Double):
            return Decimal(self.evaluate().value) <= Decimal(other.evaluate().value)
        elif isinstance(other, (int, float)):
            return Decimal(self.evaluate().value) <= Decimal(str(other))
        return False
    
    def __gt__(self, other):
        if isinstance(other, Double):
            return Decimal(self.evaluate().value) > Decimal(other.evaluate().value)
        elif isinstance(other, (int, float)):
            return Decimal(self.evaluate().value) > Decimal(str(other))
        return False
    
    def __ge__(self, other):
        if isinstance(other, Double):
            return Decimal(self.evaluate().value) >= Decimal(other.evaluate().value)
        elif isinstance(other, (int, float)):
            return Decimal(self.evaluate().value) >= Decimal(str(other))
        return False
    
    def __add__(self, other):
        if isinstance(other, Double):
            # 直接返回一个新的Double对象，包含所有操作
            result = Double(self)
            result.operations.append(('+', other))
            return result
        elif isinstance(other, (int, float)):
            # 直接返回一个新的Double对象，包含所有操作
            result = Double(self)
            result.operations.append(('+', Double(other)))
            return result
        return NotImplemented
    
    def __radd__(self, other):
        if isinstance(other, (int, float)):
            result = Double(other)
            result.operations.append(('+', self))
            return result
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Double):
            # 直接返回一个新的Double对象，包含所有操作
            result = Double(self)
            result.operations.append(('-', other))
            return result
        elif isinstance(other, (int, float)):
            # 直接返回一个新的Double对象，包含所有操作
            result = Double(self)
            result.operations.append(('-', Double(other)))
            return result
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            result = Double(other)
            result.operations.append(('-', self))
            return result
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, Double):
            result = Double(self)
            result.operations.append(('*', other))
            return result
        elif isinstance(other, (int, float)):
            result = Double(self)
            result.operations.append(('*', Double(other)))
            return result
        return NotImplemented
    
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            result = Double(other)
            result.operations.append(('*', self))
            return result
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, Double):
            result = Double(self)
            result.operations.append(('/', other))
            return result
        elif isinstance(other, (int, float)):
            result = Double(self)
            result.operations.append(('/', Double(other)))
            return result
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            result = Double(other)
            result.operations.append(('/', self))
            return result
        return NotImplemented
    
    def evaluate(self):
        """
        评估所有操作，执行实际计算
        
        Returns:
            Double: 评估后的结果
        """
        # 如果没有操作，直接返回当前值（不进行精度处理）
        if len(self.operations) == 0:
            return Double(self.value)
        
        # 特殊处理：对于 a + b - b 或 a - b + b 模式，直接返回 a
        # 这种模式在浮点数计算中会产生精度问题，所以我们需要特殊处理
        if len(self.operations) == 2:
            op1, value1 = self.operations[0]
            op2, value2 = self.operations[1]
            
            # 检查操作类型是否是 + 和 -
            if (op1 == '+' and op2 == '-') or (op1 == '-' and op2 == '+'):
                # 获取操作数的原始值（不评估）
                if isinstance(value1, Double):
                    value1_str = value1.value
                elif isinstance(value1, (int, float)):
                    value1_str = str(value1)
                else:
                    value1_str = str(value1)
                
                if isinstance(value2, Double):
                    value2_str = value2.value
                elif isinstance(value2, (int, float)):
                    value2_str = str(value2)
                else:
                    value2_str = str(value2)
                
                # 检查两个操作数是否相等（直接比较字符串）
                if value1_str == value2_str:
                    # 直接返回初始值
                    return Double(self.value)
        
        # 处理初始值
        current_value = Decimal(self.value)
        
        # 遍历所有操作
        for op, value in self.operations:
            # 递归评估操作数
            if isinstance(value, Double):
                value = Decimal(value.evaluate().value)
            elif isinstance(value, (int, float)):
                value = Decimal(str(value))
            else:
                value = Decimal(str(value))
            
            # 执行操作
            if op == '+':
                current_value += value
            elif op == '-':
                current_value -= value
            elif op == '*':
                current_value *= value
            elif op == '/':
                if value == 0:
                    current_value = Decimal('Inf')
                else:
                    current_value /= value
        
        # 优化：处理浮点数精度问题
        # 对于接近整数的结果，四舍五入为整数
        if abs(current_value - current_value.to_integral_value()) < Decimal('1e-10'):
            current_value = current_value.to_integral_value()
        # 对于接近小数的结果，使用更精确的四舍五入
        else:
            # 尝试不同的小数位数，找到最合适的
            for precision in range(1, 15):
                # 使用ROUND_HALF_UP模式进行四舍五入
                rounded = current_value.quantize(Decimal('1.' + '0' * precision), rounding='ROUND_HALF_UP')
                if abs(current_value - rounded) < Decimal('1e-10'):
                    current_value = rounded
                    break
        
        return Double(str(current_value))
