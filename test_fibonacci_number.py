from nova.compiler.lexer.scanner import Scanner

# 测试斐波那契进制数字
# 斐波那契进制规则：
# - 使用0和1表示
# - 没有连续的1
# - 基数是斐波那契数列：1, 2, 3, 5, 8, 13, ...
# 示例：
# 0f1 -> 1
# 0f10 -> 2
# 0f100 -> 3
# 0f101 -> 4 (3+1)
# 0f1000 -> 5
# 0f1001 -> 6 (5+1)
# 0f1010 -> 7 (5+2)

fibonacci_tests = [
    # 基本测试
    '0f0',      # 0
    '0f1',      # 1
    '0f10',     # 2
    '0f100',    # 3
    '0f101',    # 4 (3+1)
    '0f1000',   # 5
    '0f1001',   # 6 (5+1)
    '0f1010',   # 7 (5+2)
    '0f10000',  # 8
    '0f10001',  # 9 (8+1)
    '0f10010',  # 10 (8+2)
    '0f10100',  # 11 (8+3)
    '0f10101',  # 12 (8+3+1)
    
    # 大写前缀测试
    '0F1',      # 1
    '0F10',     # 2
    '0F100',    # 3
    
    # 边界测试
    '0f',       # 空斐波那契数字
]

for test in fibonacci_tests:
    try:
        scanner = Scanner(test)
        tokens = scanner.scan_tokens()
        # 过滤掉EOF token
        valid_tokens = [t for t in tokens if t.type != 'EOF']
        if valid_tokens:
            token = valid_tokens[0]
            print(f"'{test}' -> {token.type}: {token.literal}")
        else:
            print(f"'{test}' -> No tokens")
    except Exception as e:
        print(f"'{test}' -> Error: {e}")

print("\n测试完成！")
