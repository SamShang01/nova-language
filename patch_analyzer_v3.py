"""
修改语义分析器以增强类型检查
"""

def patch_analyzer():
    """修改语义分析器文件"""
    file_path = 'e:/nova/src/nova/compiler/semantic/analyzer.py'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修改 _types_compatible 函数，使其更严格
    # 找到并替换旧的类型兼容性检查
    old_code = """        # 允许int和float之间的隐式转换
        if (type1 == INT_TYPE and type2 == FLOAT_TYPE) or (type1 == FLOAT_TYPE and type2 == INT_TYPE):
            return True"""
    
    new_code = """        # 严格类型检查：不允许隐式类型转换"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("已修改 _types_compatible 函数")
    else:
        print("未找到 _types_compatible 函数中的旧代码")
        # 手动查找并替换
        lines = content.split('\n')
        modified_lines = []
        for i, line in enumerate(lines):
            if '允许int和float之间的隐式转换' in line:
                # 修改这一行
                modified_lines.append('        # 严格类型检查：不允许隐式类型转换')
                # 跳过下一行（if语句）
                if i + 1 < len(lines):
                    lines[i + 1] = '        # 只有完全相同的类型才兼容'
            else:
                modified_lines.append(line)
        content = '\n'.join(modified_lines)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("语义分析器修改完成！")

if __name__ == '__main__':
    patch_analyzer()
