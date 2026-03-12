"""
修复参数类型检查中的类型解析问题
"""

def fix_param_type_check():
    """修复参数类型检查"""
    file_path = 'e:/nova/src/nova/compiler/semantic/analyzer.py'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改参数类型检查部分
    old_code = '''                        if isinstance(param_info, tuple):
                                param_type = param_info[1]
                            else:
                                param_type = param_info.param_type'''
    
    new_code = '''                        if isinstance(param_info, tuple):
                                param_type = param_info[1]
                            else:
                                param_type = param_info.param_type
                            
                            # 如果param_type是TypeExpression对象，需要先解析
                            if hasattr(param_type, 'name'):
                                param_type = self._resolve_type(param_type)'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("已修复参数类型检查")
    else:
        print("未找到需要修复的代码")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("参数类型检查修复完成！")

if __name__ == '__main__':
    fix_param_type_check()
