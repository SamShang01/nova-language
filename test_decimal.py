from decimal import Decimal
import sys

# 测试Decimal的精度
result1 = Decimal('0.1') + Decimal('0.2') - Decimal('0.2')
print(f"Test 1: Decimal('0.1') + Decimal('0.2') - Decimal('0.2') = {result1}")
sys.stdout.flush()

# 测试使用float字符串
result2 = Decimal(str(0.1)) + Decimal(str(0.2)) - Decimal(str(0.2))
print(f"Test 2: Decimal(str(0.1)) + Decimal(str(0.2)) - Decimal(str(0.2)) = {result2}")
sys.stdout.flush()

# 检查str(0.1)的值
print(f"str(0.1) = '{str(0.1)}'")
print(f"str(0.2) = '{str(0.2)}'")
sys.stdout.flush()
