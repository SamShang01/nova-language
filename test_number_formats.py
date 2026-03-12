from nova.compiler.lexer.scanner import Scanner

# 测试不同进制的数字
number_tests = [
    # 十进制
    '123',
    '0',
    '999999',
    
    # 十六进制
    '0x123',
    '0XABC',
    '0xFF',
    '0x0',
    
    # 八进制
    '0o123',
    '0O456',
    '0777',  # 0前缀
    '0',     # 单独的0
    
    # 二进制
    '0b1010',
    '0B1111',
    '0b0',
    
    # 浮点数
    '123.456',
    '0.123',
    '123.',
    
    # 双精度浮点数
    '123.456D',
    '0.123d',
    '1814.31850932850283049D',
    '1814.31850932850283049d',
]

for test in number_tests:
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
