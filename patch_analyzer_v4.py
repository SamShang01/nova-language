"""
修改语义分析器以增强类型检查
"""

def patch_analyzer():
    """修改语义分析器文件"""
    file_path = 'e:/nova/src/nova/compiler/semantic/analyzer.py'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找并修改 _types_compatible 函数
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 查找需要修改的行
        if '允许int和float之间的隐式转换' in line:
            # 修改这一行
            new_lines.append('        # 严格类型检查：不允许隐式类型转换\n')
            # 跳过下一行（if语句）
            if i + 1 < len(lines):
                i += 1
                # 修改下一行
                if i < len(lines):
                    new_lines.append('        # 只有完全相同的类型才兼容\n')
            modified = True
        else:
            new_lines.append(line)
        
        i += 1
    
    if modified:
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("语义分析器修改完成！")
    else:
        print("未找到需要修改的代码")

if __name__ == '__main__':
    patch_analyzer()
