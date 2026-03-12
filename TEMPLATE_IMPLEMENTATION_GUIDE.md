# Nova 模板功能实现指南

## 概述

本文档详细说明Nova语言模板功能的实现细节，供开发参考。

## 1. 模板类实现参考

### 1.1 AST节点定义

**文件**: `src/nova/compiler/parser/ast.py`

```python
class GenericClassDefinition(ClassDefinition):
    """
    泛型类定义节点（支持访问修饰符、构造函数、静态成员、抽象类和模板类）
    """
    
    def __init__(self, line, column, name, type_params, fields, methods=None, 
                 parent=None, init_method=None, static_fields=None, 
                 static_methods=None, is_abstract=False):
        super().__init__(line, column, name, fields, methods, parent, 
                        init_method, static_fields, static_methods, is_abstract)
        self.type_params = type_params  # 类型参数列表，如 ['T', 'U']
```

**关键属性**:
- `type_params`: 类型参数列表
- 继承自 `ClassDefinition`，复用类的所有功能

### 1.2 词法分析

**文件**: `src/nova/compiler/lexer/tokens.py`

```python
class TokenType(Enum):
    # ... 其他token类型
    TEMPLATE = 'TEMPLATE'  # template关键字
    # ...

# 关键字映射
KEYWORDS = {
    # ... 其他关键字
    'template': TokenType.TEMPLATE,
    # ...
}
```

### 1.3 语法分析

**文件**: `src/nova/compiler/parser/parser.py`

解析器需要处理 `template class` 语法：

```python
def parse_template_class(self):
    """
    解析模板类定义
    template class ClassName<T, U> { ... }
    """
    line = self.current_token.line
    column = self.current_token.column
    
    # 消费 'template' 关键字
    self.consume(TokenType.TEMPLATE)
    
    # 消费 'class' 关键字
    self.consume(TokenType.CLASS)
    
    # 获取类名
    class_name = self.current_token.value
    self.consume(TokenType.IDENTIFIER)
    
    # 解析类型参数 <T, U>
    self.consume(TokenType.LT)  # '<'
    type_params = []
    
    while self.current_token.type != TokenType.GT:
        type_params.append(self.current_token.value)
        self.consume(TokenType.IDENTIFIER)
        
        if self.current_token.type == TokenType.COMMA:
            self.consume(TokenType.COMMA)
    
    self.consume(TokenType.GT)  # '>'
    
    # 解析类体（复用现有的类解析逻辑）
    fields, methods = self.parse_class_body()
    
    return GenericClassDefinition(line, column, class_name, type_params, fields, methods)
```

### 1.4 语义分析

**文件**: `src/nova/compiler/semantic/analyzer.py`

```python
def visit_GenericClassDefinition(self, node):
    """
    处理泛型类定义的语义分析
    """
    # 1. 创建泛型类类型
    class_type = GenericClassType(node.name, node.type_params)
    
    # 2. 注册到符号表
    self.current_scope.define(node.name, class_type)
    
    # 3. 创建新的作用域用于类型参数
    type_scope = Scope(self.current_scope)
    for type_param in node.type_params:
        type_scope.define(type_param, TypeParameter(type_param))
    
    # 4. 保存当前作用域，切换到类型作用域
    old_scope = self.current_scope
    self.current_scope = type_scope
    
    # 5. 分析字段
    for field in node.fields:
        field_type = self.resolve_type(field.type)
        class_type.add_field(field.name, field_type)
    
    # 6. 分析方法
    for method in node.methods:
        self.visit(method)
    
    # 7. 恢复作用域
    self.current_scope = old_scope
    
    return class_type
```

### 1.5 代码生成

**文件**: `src/nova/compiler/codegen/generator.py`

```python
def visit_GenericClassDefinition(self, node):
    """
    生成泛型类的代码
    """
    # 1. 创建类定义
    class_def = {
        'name': node.name,
        'type_params': node.type_params,
        'fields': [],
        'methods': {}
    }
    
    # 2. 处理字段
    for field in node.fields:
        field_type = self.get_type_code(field.type)
        class_def['fields'].append({
            'name': field.name,
            'type': field_type
        })
    
    # 3. 处理方法
    for method in node.methods:
        method_code = self.visit(method)
        class_def['methods'][method.name] = method_code
    
    # 4. 生成类定义指令
    self.instructions.append(LOAD_CONST(class_def))
    self.instructions.append(STORE_NAME(node.name))
    
    return class_def
```

## 2. 模板结构体实现方案

### 2.1 AST节点设计

**建议**: 创建新的 `GenericStructDefinition` 节点

```python
class GenericStructDefinition(StructDefinition):
    """
    泛型结构体定义节点
    
    与GenericClassDefinition的区别：
    1. 结构体是值类型（is_value_type = True）
    2. 默认使用值拷贝语义
    3. 内存布局更紧凑
    """
    
    def __init__(self, line, column, name, type_params, fields, methods=None):
        super().__init__(line, column, name, fields, methods)
        self.type_params = type_params  # 类型参数列表
        self.is_value_type = True  # 标记为值类型
```

### 2.2 词法分析

无需修改，复用现有的 `TEMPLATE` 关键字。

### 2.3 语法分析

在 `parser.py` 中添加：

```python
def parse_generic_struct(self):
    """
    解析模板结构体定义
    template struct StructName<T, U> { ... }
    """
    line = self.current_token.line
    column = self.current_token.column
    
    # 消费 'template' 关键字
    self.consume(TokenType.TEMPLATE)
    
    # 消费 'struct' 关键字
    self.consume(TokenType.STRUCT)
    
    # 获取结构体名
    struct_name = self.current_token.value
    self.consume(TokenType.IDENTIFIER)
    
    # 解析类型参数 <T, U>
    self.consume(TokenType.LT)
    type_params = []
    
    while self.current_token.type != TokenType.GT:
        type_params.append(self.current_token.value)
        self.consume(TokenType.IDENTIFIER)
        
        if self.current_token.type == TokenType.COMMA:
            self.consume(TokenType.COMMA)
    
    self.consume(TokenType.GT)
    
    # 解析结构体体（复用现有的结构体解析逻辑）
    fields, methods = self.parse_struct_body()
    
    return GenericStructDefinition(line, column, struct_name, type_params, fields, methods)
```

### 2.4 语义分析

```python
def visit_GenericStructDefinition(self, node):
    """
    处理泛型结构体定义的语义分析
    
    与泛型类的主要区别：
    1. 标记为值类型
    2. 使用值拷贝语义
    3. 内存分配在栈上
    """
    # 1. 创建泛型结构体类型
    struct_type = GenericStructType(node.name, node.type_params)
    struct_type.is_value_type = True  # 标记为值类型
    
    # 2. 注册到符号表
    self.current_scope.define(node.name, struct_type)
    
    # 3. 创建新的作用域用于类型参数
    type_scope = Scope(self.current_scope)
    for type_param in node.type_params:
        type_scope.define(type_param, TypeParameter(type_param))
    
    # 4. 保存当前作用域，切换到类型作用域
    old_scope = self.current_scope
    self.current_scope = type_scope
    
    # 5. 分析字段
    for field in node.fields:
        field_type = self.resolve_type(field.type)
        struct_type.add_field(field.name, field_type)
    
    # 6. 分析方法
    for method in node.methods:
        self.visit(method)
    
    # 7. 恢复作用域
    self.current_scope = old_scope
    
    return struct_type
```

### 2.5 代码生成

```python
def visit_GenericStructDefinition(self, node):
    """
    生成泛型结构体的代码
    
    与泛型类的主要区别：
    1. 使用值类型语义
    2. 生成拷贝构造函数
    3. 栈上分配内存
    """
    # 1. 创建结构体定义
    struct_def = {
        'name': node.name,
        'type_params': node.type_params,
        'fields': [],
        'methods': {},
        'is_value_type': True  # 标记为值类型
    }
    
    # 2. 处理字段
    for field in node.fields:
        field_type = self.get_type_code(field.type)
        struct_def['fields'].append({
            'name': field.name,
            'type': field_type
        })
    
    # 3. 处理方法
    for method in node.methods:
        method_code = self.visit(method)
        struct_def['methods'][method.name] = method_code
    
    # 4. 生成拷贝构造函数（值类型需要）
    struct_def['copy_constructor'] = self.generate_copy_constructor(node)
    
    # 5. 生成结构体定义指令
    self.instructions.append(LOAD_CONST(struct_def))
    self.instructions.append(STORE_NAME(node.name))
    
    return struct_def

def generate_copy_constructor(self, node):
    """
    为结构体生成拷贝构造函数
    """
    copy_code = []
    for field in node.fields:
        copy_code.append(LOAD_FIELD(field.name))
        copy_code.append(STORE_FIELD(field.name))
    return copy_code
```

## 3. 关键差异总结

### 3.1 类 vs 结构体

| 特性 | 类 (Class) | 结构体 (Struct) |
|------|------------|-----------------|
| 类型 | 引用类型 | 值类型 |
| 存储位置 | 堆 (Heap) | 栈 (Stack) |
| 拷贝语义 | 引用拷贝 | 值拷贝 |
| 内存布局 | 包含对象头 | 紧凑布局 |
| 继承 | 支持 | 不支持 |
| 多态 | 支持 | 不支持 |

### 3.2 实现差异

1. **AST节点**: 
   - 类: `GenericClassDefinition`
   - 结构体: `GenericStructDefinition` (新增)

2. **类型标记**:
   - 类: `is_value_type = False`
   - 结构体: `is_value_type = True`

3. **代码生成**:
   - 类: 生成对象分配代码
   - 结构体: 生成栈分配和拷贝代码

## 4. 测试用例

**文件**: `test_generic_struct.nova`

已创建完整的测试用例，包括：
1. 基本模板结构体
2. 多类型参数
3. 模板结构体方法
4. 作为函数参数和返回值
5. 嵌套模板结构体
6. 模板结构体数组
7. 复杂模板结构体
8. 值类型特性验证
9. 边界情况

## 5. 相关文件

- `src/nova/compiler/parser/ast.py` - AST节点定义
- `src/nova/compiler/parser/parser.py` - 语法分析器
- `src/nova/compiler/semantic/analyzer.py` - 语义分析器
- `src/nova/compiler/codegen/generator.py` - 代码生成器
- `src/nova/compiler/lexer/tokens.py` - 词法分析器
- `test_generic_struct.nova` - 测试用例
- `talkToTheOtherProgrammer.md` - 协作沟通记录

## 6. 实现建议

### 6.1 开发顺序

1. **AST节点** (`ast.py`)
   - 创建 `GenericStructDefinition` 类
   - 参考 `GenericClassDefinition` 实现

2. **词法分析** (`tokens.py`)
   - 确认 `STRUCT` 关键字已定义

3. **语法分析** (`parser.py`)
   - 添加 `parse_generic_struct` 方法
   - 在 `parse_statement` 中添加对 `template struct` 的识别

4. **语义分析** (`analyzer.py`)
   - 添加 `visit_GenericStructDefinition` 方法
   - 处理值类型特性

5. **代码生成** (`generator.py`)
   - 添加 `visit_GenericStructDefinition` 方法
   - 生成值类型相关的代码

6. **测试验证**
   - 运行 `test_generic_struct.nova`
   - 验证所有测试用例通过

### 6.2 注意事项

1. **值类型处理**: 确保结构体的拷贝语义正确实现
2. **内存管理**: 结构体在栈上分配，无需垃圾回收
3. **类型检查**: 在语义分析阶段进行完整的类型检查
4. **错误处理**: 提供清晰的错误信息

## 7. 协作沟通

请随时在 `talkToTheOtherProgrammer.md` 中记录进展和遇到的问题！

---

**最后更新**: 2026-03-01  
**作者**: AI助手（架构/STL负责人）
