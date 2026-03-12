import sys
sys.path.insert(0, 'e:\\nova\\src')

from nova.vm.double_type import Double

# 测试Double的精度
d1 = Double(0.1)
d2 = Double(0.2)
d3 = Double(0.2)

print(f"d1.value = '{d1.value}'")
print(f"d2.value = '{d2.value}'")
print(f"d3.value = '{d3.value}'")

# 执行加法
result = d1 + d2
print(f"d1 + d2 operations = {result.operations}")

# 执行减法
result2 = result - d3
print(f"(d1 + d2) - d3 operations = {result2.operations}")

# 评估结果
evaluated = result2.evaluate()
print(f"Result = {evaluated.value}")
