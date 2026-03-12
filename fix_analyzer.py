"""
修复语义分析器中的多余代码
"""

def fix_analyzer():
    """修复语义分析器文件"""
    file_path = 'e:/nova/src/nova/compiler/semantic/analyzer.py'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找并修复多余的 return True
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 查找多余的 return True
        if i > 0 and '只有完全相同的类型才兼容' in lines[i-1] and 'return True' in line and line.strip().startswith('return True'):
            # 跳过这一行
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("语义分析器修复完成！")

if __name__ == '__main__':
    fix_analyzer()
