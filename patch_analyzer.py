"""
修改语义分析器以增强类型检查
"""

import re

def patch_analyzer():
    """修改语义分析器文件"""
    file_path = 'e:/nova/src/nova/compiler/semantic/analyzer.py'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修改 _types_compatible 函数，使其更严格
    old_types_compatible = '''    def _types_compatible(self, type1, type2):
        """
        检查类型兼容性
        
        Args:
            type1: 类型1
            type2: 类型2
        
        Returns:
            bool: 类型是否兼容
        """
        # 允许int和float之间的隐式转换
        if (type1 == INT_TYPE and type2 == FLOAT_TYPE) or (type1 == FLOAT_TYPE and type2 == INT_TYPE):
            return True
        return type1 == type2'''
    
    new_types_compatible = '''    def _types_compatible(self, type1, type2):
        """
        检查类型兼容性
        
        Args:
            type1: 类型1
            type2: 类型2
        
        Returns:
            bool: 类型是否兼容
        """
        # 严格类型检查：不允许隐式类型转换
        # 只有完全相同的类型才兼容
        return type1 == type2'''
    
    content = content.replace(old_types_compatible, new_types_compatible)
    
    # 2. 增强 visit_CallExpression 函数，添加参数类型检查
    old_call_expression = '''    def visit_CallExpression(self, node):
        """
        访问调用表达式节点
        """
        # 分析被调用对象
        callee_type = self._infer_type(node.callee)
        
        # 分析参数
        for arg in node.arguments:
            self._infer_type(arg)
        
        # 处理标识符调用（函数调用）
        if isinstance(node.callee, IdentifierExpression):
            # 尝试解析函数符号
            symbol = self.current_scope.resolve_symbol(node.callee.name)
            if symbol and hasattr(symbol, 'return_type'):
                return symbol.return_type
            
            # 处理内置函数
            if node.callee.name == "str":
                return STRING_TYPE
            elif node.callee.name == "print":
                return UNIT_TYPE
            elif node.callee.name == "len":
                return INT_TYPE
        
        # 处理泛型类型实例化（如 Pair<T, U>(...)）
        if isinstance(node.callee, GenericTypeExpression):
            # 返回泛型类型实例化的类型
            return node.callee.accept(self)
        
        # 简化实现，返回unit类型
        return UNIT_TYPE'''
    
    new_call_expression = '''    def visit_CallExpression(self, node):
        """
        访问调用表达式节点
        """
        # 分析被调用对象
        callee_type = self._infer_type(node.callee)
        
        # 处理标识符调用（函数调用）
        if isinstance(node.callee, IdentifierExpression):
            # 尝试解析函数符号
            symbol = self.current_scope.resolve_symbol(node.callee.name)
            
            # 如果是函数符号，检查参数类型
            if symbol and hasattr(symbol, 'params'):
                # 分析参数
                for i, arg in enumerate(node.arguments):
                    arg_type = self._infer_type(arg)
                    
                    # 获取参数类型
                    if hasattr(symbol, 'params'):
                        if i < len(symbol.params):
                            param_info = symbol.params[i]
                            if isinstance(param_info, tuple):
                                param_type = param_info[1]
                            else:
                                param_type = param_info.param_type
                            
                            # 检查参数类型兼容性
                            if not self._types_compatible(arg_type, param_type):
                                raise SemanticError(
                                    node.line, node.column,
                                    f"Parameter type mismatch: expected {param_type}, got {arg_type}"
                                )
            
            # 处理结构体实例化
            if symbol and hasattr(symbol, 'type') and isinstance(symbol.type, StructType):
                # 检查结构体实例化的参数类型
                struct_type = symbol.type
                for i, arg in enumerate(node.arguments):
                    arg_type = self._infer_type(arg)
                    
                    # 获取字段类型
                    if i < len(struct_type.fields):
                        field_name, field_type = struct_type.fields[i]
                        
                        # 检查参数类型兼容性
                        if not self._types_compatible(arg_type, field_type):
                            raise SemanticError(
                                node.line, node.column,
                                f"Field '{field_name}' type mismatch: expected {field_type}, got {arg_type}"
                            )
            
            # 处理内置函数
            if node.callee.name == "str":
                return STRING_TYPE
            elif node.callee.name == "print":
                return UNIT_TYPE
            elif node.callee.name == "len":
                return INT_TYPE
        
        # 处理泛型类型实例化（如 Pair<T, U>(...)）
        if isinstance(node.callee, GenericTypeExpression):
            # 返回泛型类型实例化的类型
            return node.callee.accept(self)
        
        # 简化实现，返回unit类型
        return UNIT_TYPE'''
    
    content = content.replace(old_call_expression, new_call_expression)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("语义分析器修改完成！")

if __name__ == '__main__':
    patch_analyzer()
