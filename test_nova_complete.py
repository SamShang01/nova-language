#!/usr/bin/env python3
# 完整的 Nova 编译器功能测试

from nova.compiler.lexer.scanner import Scanner
from nova.compiler.parser.parser import Parser
from nova.compiler.semantic.analyzer import SemanticAnalyzer
from nova.compiler.codegen.generator import CodeGenerator
from nova.vm.machine import VirtualMachine

def test_nova_code(code, description):
    """
    测试 Nova 代码
    
    Args:
        code: Nova 代码
        description: 测试描述
    """
    print(f"\n{'='*60}")
    print(f"测试: {description}")
    print(f"代码: {code}")
    print(f"{'='*60}")
    
    try:
        # 词法分析
        print("1. 词法分析...")
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        print(f"   ✓ 生成 {len(tokens)} 个token")
        
        # 语法分析
        print("2. 语法分析...")
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"   ✓ AST创建成功")
        
        # 语义分析
        print("3. 语义分析...")
        analyzer = SemanticAnalyzer()
        analyzed_ast = analyzer.analyze(ast)
        print(f"   ✓ 语义分析完成")
        
        # 代码生成
        print("4. 代码生成...")
        codegen = CodeGenerator()
        instructions, constants = codegen.generate(analyzed_ast)
        print(f"   ✓ 生成 {len(instructions)} 条指令")
        
        # 执行
        print("5. 执行...")
        vm = VirtualMachine()
        vm.load(instructions, constants)
        result = vm.run()
        print(f"   ✓ 执行结果: {result}")
        
        print(f"\n{'='*60}")
        print(f"✓ 测试成功！")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"\n{'='*60}")
        print(f"✗ 测试失败: {e}")
        print(f"详细错误信息:\n{traceback.format_exc()}")
        print(f"{'='*60}\n")
        
        return False

if __name__ == '__main__':
    print("Nova 编译器完整功能测试")
    print("="*60)
    
    # 测试用例
    test_cases = [
        ("1 + 2;", "简单数学表达式"),
        ("(3 + 4) * 2;", "复杂数学表达式"),
        ("true && false;", "布尔表达式"),
        ('"Hello, Nova!";', "字符串"),
        ("10 > 5;", "数字比较"),
        ("1 + 2 + 3;", "多个运算符"),
        ("(1 + 2) * (3 + 4);", "嵌套表达式"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for code, description in test_cases:
        if test_nova_code(code, description):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"测试总结: {success_count}/{total_count} 成功")
    print("="*60)
    
    if success_count == total_count:
        print("✓ 所有测试通过！Nova 编译器核心功能正常工作！")
    else:
        print(f"✗ {total_count - success_count} 个测试失败，需要修复")
