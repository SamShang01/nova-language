#!/usr/bin/env python3
# 简单的命令行测试脚本，验证Nova编译器核心功能

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

def test_nova_code(code):
    print(f"测试代码: {code}")
    print("-" * 50)
    
    try:
        # 词法分析
        print("1. 词法分析...")
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        print(f"   生成 {len(tokens)} 个token")
        
        # 语法分析
        print("2. 语法分析...")
        parser = Parser(tokens)
        ast = parser.parse()
        print("   AST创建成功")
        
        # 语义分析
        print("3. 语义分析...")
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        print("   语义分析完成")
        
        # 代码生成
        print("4. 代码生成...")
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(analyzed_ast)
        print(f"   生成 {len(instructions)} 条指令")
        
        # 执行
        print("5. 执行...")
        vm = VirtualMachine()
        vm.load(instructions, constants)
        result = vm.run()
        print(f"   执行结果: {result}")
        
        print("-" * 50)
        print("✓ 测试成功！\n")
        return result
        
    except Exception as e:
        import traceback
        print("-" * 50)
        print(f"✗ 测试失败: {e}")
        print(f"详细错误信息:\n{traceback.format_exc()}")
        print()
        return None

if __name__ == '__main__':
    print("Nova 编译器核心功能测试")
    print("=" * 50)
    print()
    
    # 测试1: 简单的数学表达式
    test_nova_code("1 + 2;")
    
    # 测试2: 复杂表达式
    test_nova_code("(3 + 4) * 2;")
    
    # 测试3: 布尔表达式
    test_nova_code("true && false;")
    
    # 测试4: 字符串
    test_nova_code('"Hello, Nova!";')
    
    # 测试5: 数字比较
    test_nova_code("10 > 5;")
    
    print("=" * 50)
    print("所有测试完成！")
