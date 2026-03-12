"""
Nova语言语法分析器
"""

from nova.compiler.lexer import TokenType
from nova.compiler.parser.ast import *
from nova.compiler.parser.errors import ParserError

class Parser:
    """
    语法分析器
    
    负责将Token序列转换为抽象语法树(AST)，是Nova语言编译过程中的核心组件之一。
    
    工作原理:
    1. 从词法分析器(lexer)接收Token序列
    2. 使用递归下降解析法分析Token序列的语法结构
    3. 构建并返回表示整个程序的AST
    
    主要功能:
    - 支持Nova语言的所有语法结构，包括函数、结构体、枚举、联合等
    - 支持泛型类型和函数
    - 支持装饰器
    - 提供详细的错误信息
    - 优化链式调用的解析性能
    
    核心方法:
    - parse(): 主解析方法，解析整个Token序列
    - parse_statement(): 解析单个语句
    - parse_expression(): 解析表达式
    - parse_function_definition(): 解析函数定义
    - parse_struct_definition(): 解析结构体定义
    """
    
    def __init__(self, tokens, repl_mode=False):
        """
        初始化解析器
        
        Args:
            tokens: Token列表
            repl_mode: 是否为REPL模式（REPL模式下表达式语句可以没有分号）
        """
        self.tokens = tokens
        self.current = 0
        self.repl_mode = repl_mode
    
    def parse(self):
        """
        解析Token序列，生成AST
        
        Returns:
            Program: 程序节点
        
        Raises:
            ParserError: 语法分析错误
        """
        statements = []
        
        while not self.is_at_end():
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        
        return Program(
            self.peek().line if not self.is_at_end() else 1,
            self.peek().column if not self.is_at_end() else 1,
            statements
        )
    
    def parse_statement(self):
        """
        解析语句
        
        Returns:
            Node: 语句节点
        """
        # 检查是否是装饰器
        decorators = []
        while self.peek().type == TokenType.AT:
            # 消耗@符号
            self.advance()
            # 解析装饰器名称
            decorator_name = self.consume(TokenType.IDENTIFIER, "Expect decorator name")
            # 创建装饰器表达式
            decorator = DecoratorExpression(
                decorator_name.line, decorator_name.column,
                IdentifierExpression(
                    decorator_name.line, decorator_name.column,
                    decorator_name.lexeme
                )
            )
            decorators.append(decorator)
        
        # 检查是否是函数定义
        if decorators and self.peek().type == TokenType.FUNC:
            # 解析函数定义
            func_def = self.parse_function_definition()
            # 添加装饰器
            func_def.decorators = decorators + func_def.decorators
            return func_def
        elif decorators:
            # 有装饰器但不是函数定义，报错
            self.error("Expect 'func' keyword after decorator")
        
        token = self.peek()
        
        # 检查是否是异步函数定义
        if token.type == TokenType.ASYNC:
            return self.parse_function_definition()
        
        if token.type == TokenType.MOD:
            return self.parse_module_declaration()
        elif token.type == TokenType.FROM:
            return self.parse_from_import_statement()
        elif token.type == TokenType.USE:
            return self.parse_import_statement()
        elif token.type == TokenType.FEATURE:
            return self.parse_feature_statement()
        elif token.type == TokenType.FUNC:
            return self.parse_function_definition()
        elif token.type == TokenType.LET:
            return self.parse_variable_declaration()
        elif token.type == TokenType.VAR:
            return self.parse_variable_declaration(mutable=True)
        elif token.type == TokenType.CONST:
            return self.parse_constant_declaration()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.FOR:
            return self.parse_for_loop()
        elif token.type == TokenType.WHILE:
            return self.parse_while_loop()
        elif token.type == TokenType.LOOP:
            return self.parse_loop_statement()
        elif token.type == TokenType.MATCH:
            return self.parse_match_statement()
        elif token.type == TokenType.GENERIC:
            # 检查是否是泛型结构体声明
            if not self.is_at_end() and self.current + 1 < len(self.tokens):
                next_token = self.tokens[self.current + 1]
                if next_token.type == TokenType.STRUCT:
                    return self.parse_struct_definition()
                elif next_token.type == TokenType.FUNC:
                    # 泛型函数定义，跳过generic关键字
                    self.advance()
                    # 不要消费FUNC关键字，让parse_function_definition来消费
                    return self.parse_function_definition(is_generic=True)
            # 尝试解析表达式语句
            return self.parse_expression_statement()
        elif token.type == TokenType.TEMPLATE:
            # 检查是否是模板类或函数声明
            if not self.is_at_end() and self.current + 1 < len(self.tokens):
                next_token = self.tokens[self.current + 1]
                if next_token.type == TokenType.CLASS:
                    # 模板类定义
                    self.advance()  # 跳过TEMPLATE关键字
                    return self.parse_class_definition()
                elif next_token.type == TokenType.STRUCT:
                    # 模板结构体定义
                    self.advance()  # 跳过TEMPLATE关键字
                    return self.parse_struct_definition(is_template=True)
                elif next_token.type == TokenType.FUNC:
                    # 模板函数定义
                    self.advance()  # 跳过TEMPLATE关键字
                    return self.parse_function_definition(is_generic=True)
            # 尝试解析表达式语句
            return self.parse_expression_statement()
        elif token.type == TokenType.STRUCT:
            return self.parse_struct_definition()
        elif token.type == TokenType.CLASS or token.type == TokenType.ABSTRACT:
            return self.parse_class_definition()
        elif token.type == TokenType.UNION:
            return self.parse_union_definition()
        elif token.type == TokenType.ENUM:
            return self.parse_enum_definition()
        elif token.type == TokenType.TRAIT:
            return self.parse_trait_definition()
        elif token.type == TokenType.IMPL:
            return self.parse_impl_block()
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.BREAK:
            return self.parse_break_statement()
        elif token.type == TokenType.CONTINUE:
            return self.parse_continue_statement()
        elif token.type == TokenType.DEL:
            return self.parse_delete_variable()
        else:
            # 尝试解析表达式语句
            return self.parse_expression_statement()
    
    def parse_module_declaration(self):
        """
        解析模块声明
        """
        token = self.consume(TokenType.MOD, "Expect 'mod' keyword")
        name = self.consume(TokenType.IDENTIFIER, "Expect module name")
        
        # 模块声明可以带或不带分号
        if self.peek().type == TokenType.SEMICOLON:
            self.advance()
        
        return ModuleDeclaration(token.line, token.column, name.lexeme)
    
    def parse_from_import_statement(self):
        """
        解析from ... import ... 语句
        支持两种语法：
        1. from __future__ import feature;
        2. from path::to::module import name;
        """
        token = self.consume(TokenType.FROM, "Expect 'from' keyword")
        
        # 解析导入路径
        path = []
        while self.peek().type == TokenType.IDENTIFIER:
            identifier = self.consume(TokenType.IDENTIFIER, "Expect identifier in import path").lexeme
            path.append(identifier)
            
            if self.peek().type == TokenType.DOT:
                self.advance()
            else:
                break
        
        # 解析 import 关键字
        self.consume(TokenType.IMPORT, "Expect 'import' keyword")
        
        # 解析导入的名称
        import_name = self.consume(TokenType.IDENTIFIER, "Expect import name").lexeme
        
        # 解析别名
        alias = None
        if self.peek().type == TokenType.AS:
            self.advance()
            alias = self.consume(TokenType.IDENTIFIER, "Expect alias name").lexeme
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after import statement")
        
        # 特殊处理 __future__ 导入
        if path == ["__future__"]:
            return FeatureStatement(token.line, token.column, import_name)
        
        # 将 from ... import ... 转换为标准 ImportStatement
        # 路径部分加上导入的名称
        full_path = path + [import_name]
        return ImportStatement(token.line, token.column, full_path, alias)
    
    def parse_feature_statement(self):
        """
        解析feature语句
        语法：feature FeatureName;
        """
        token = self.consume(TokenType.FEATURE, "Expect 'feature' keyword")
        feature_name = self.consume(TokenType.IDENTIFIER, "Expect feature name")
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after feature statement")
        
        # 返回FeatureStatement节点
        return FeatureStatement(token.line, token.column, feature_name.lexeme)
    
    def parse_import_statement(self):
        """
        解析导入语句
        支持语法：use path::to::module;
        """
        token = self.consume(TokenType.USE, "Expect 'use' keyword")
        
        # 传统的 use path::to::module 语法
        # 解析导入路径
        path = []
        while self.peek().type == TokenType.IDENTIFIER:
            path.append(self.consume(TokenType.IDENTIFIER, "Expect identifier in import path").lexeme)
            if self.peek().type == TokenType.DOT:
                self.advance()
            else:
                break
        
        # 解析别名
        alias = None
        if self.peek().type == TokenType.AS:
            self.advance()
            alias = self.consume(TokenType.IDENTIFIER, "Expect alias name").lexeme
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after import statement")
        
        return ImportStatement(token.line, token.column, path, alias)
    
    def _parse_function_common(self, token, name, is_abstract=False):
        """
        解析函数定义的公共部分
        
        Args:
            token: func关键字的token
            name: 函数名的token
            is_abstract: 是否是抽象方法（没有方法体）
            
        Returns:
            tuple: (params, return_type, where_clause, body)
        """
        # 解析参数
        self.consume(TokenType.LPAREN, "Expect '(' after function name")
        params = []
        if self.peek().type != TokenType.RPAREN:
            while True:
                # 检查是否是可变参数（*args）
                is_varargs = False
                is_kwargs = False
                if self.peek().type == TokenType.STAR:
                    self.advance()
                    is_varargs = True
                elif self.peek().type == TokenType.STAR_STAR:
                    self.advance()
                    is_kwargs = True
                
                # 检查是否是强制参数（manda）
                is_mandatory = False
                if self.peek().type == TokenType.MANDA:
                    self.advance()
                    is_mandatory = True
                
                # 参数名可以是IDENTIFIER或SELF关键字
                if self.peek().type == TokenType.SELF:
                    param_name = self.advance()
                else:
                    param_name = self.consume(TokenType.IDENTIFIER, "Expect parameter name")
                
                self.consume(TokenType.COLON, "Expect ':' after parameter name")
                param_type = self.parse_type()
                
                # 检查是否有默认值（default关键字或=）
                default_value = None
                if self.peek().type == TokenType.DEFAULT:
                    self.advance()
                    default_value = self.parse_expression()
                elif self.peek().type == TokenType.ASSIGN:
                    self.advance()
                    default_value = self.parse_expression()
                
                # 创建ParameterDefinition对象
                from nova.compiler.parser.ast import ParameterDefinition
                params.append(ParameterDefinition(
                    param_name.line, param_name.column,
                    param_name.lexeme, param_type, default_value,
                    is_varargs, is_kwargs, is_mandatory
                ))
                
                # 检查是否是逗号或右括号
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                elif self.peek().type == TokenType.RPAREN:
                    break
                else:
                    # 如果不是逗号或右括号，报错
                    self.error("Expect ',' or ')' after parameter")
        self.consume(TokenType.RPAREN, "Expect ')' after parameters")
        
        # 解析返回类型（支持 -> 和 : 两种语法）
        return_type = None
        if self.peek().type == TokenType.ARROW:
            self.advance()
            return_type = self.parse_type()
        elif self.peek().type == TokenType.COLON:
            self.advance()
            return_type = self.parse_type()
        
        # 解析where子句
        where_clause = None
        if self.match(TokenType.WHERE):
            where_clause = self.parse_where_clause()
        
        # 解析函数体（抽象方法没有方法体）
        body = None
        if not is_abstract:
            body = self.parse_block()
        else:
            # 抽象方法以分号结尾
            self.consume(TokenType.SEMICOLON, "Expect ';' after abstract method declaration")
        
        return params, return_type, where_clause, body
    
    def parse_function_definition(self, is_generic=False, is_abstract=False):
        """
        解析函数定义
        
        Args:
            is_generic: 是否是泛型函数（从parse_statement传入）
            is_abstract: 是否是抽象方法（没有方法体）
        """
        # 初始化装饰器列表
        decorators = []
        
        # 检查是否是异步函数
        is_async = False
        if self.peek().type == TokenType.ASYNC:
            self.advance()
            is_async = True
        
        # 检查是否是泛型函数
        type_params = None
        token = None
        name = None
        
        # 首先处理func关键字和函数名
        token = self.consume(TokenType.FUNC, "Expect 'func' keyword")
        name = self.consume(TokenType.IDENTIFIER, "Expect function name")
        
        # 检查是否有类型参数（函数名后面的类型参数）
        if self.peek().type == TokenType.LESS_THAN:
            # 带有类型参数的函数
            type_params = self.parse_type_parameters()
        elif is_generic:
            # 泛型函数但没有显式的类型参数
            type_params = []
        
        # 解析函数的公共部分
        params, return_type, where_clause, body = self._parse_function_common(token, name, is_abstract)
        
        # 如果是泛型函数，返回GenericFunctionDefinition
        if type_params is not None:
            return GenericFunctionDefinition(
                token.line, token.column,
                name.lexeme, type_params, params, return_type, body, where_clause,
                is_async=is_async, is_abstract=is_abstract
            )
        
        return FunctionDefinition(
            token.line, token.column,
            name.lexeme, params, return_type, body, decorators,
            is_async=is_async, is_abstract=is_abstract
        )
    
    def parse_decorator(self):
        """
        解析装饰器
        
        支持以下形式的装饰器：
        @decorator
        @decorator()
        @decorator(arg1, arg2)
        @decorator(name=value)
        """
        # 消耗@符号
        at_token = self.consume(TokenType.AT, "Expect '@' for decorator")
        
        # 解析装饰器名称
        identifier = self.consume(TokenType.IDENTIFIER, "Expect decorator name")
        decorator = IdentifierExpression(
            identifier.line, identifier.column,
            identifier.lexeme
        )
        
        # 检查是否是调用表达式
        if self.peek().type == TokenType.LPAREN:
            # 消耗左括号
            self.consume(TokenType.LPAREN, "Expect '(' after decorator name")
            
            # 解析参数
            arguments = []
            if self.peek().type != TokenType.RPAREN:
                while True:
                    # 解析简单表达式作为参数
                    if self.peek().type == TokenType.IDENTIFIER:
                        # 标识符
                        id_token = self.consume(TokenType.IDENTIFIER, "Expect argument")
                        arg = IdentifierExpression(
                            id_token.line, id_token.column,
                            id_token.lexeme
                        )
                    elif self.peek().type in (TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.TRUE, TokenType.FALSE, TokenType.NULL):
                        # 字面量
                        token = self.advance()
                        arg = LiteralExpression(
                            token.line, token.column,
                            token.lexeme
                        )
                    else:
                        # 其他表达式类型，暂时不支持
                        self.error("Expect identifier or literal as argument")
                    
                    arguments.append(arg)
                    
                    # 检查是否是逗号或右括号
                    if self.peek().type == TokenType.COMMA:
                        self.advance()
                    elif self.peek().type == TokenType.RPAREN:
                        break
                    else:
                        # 如果不是逗号或右括号，报错
                        self.error("Expect ',' or ')' after argument")
            
            # 消耗右括号
            self.consume(TokenType.RPAREN, "Expect ')' after arguments")
            
            # 创建调用表达式
            decorator = CallExpression(
                at_token.line, at_token.column,
                decorator,
                arguments
            )
        
        # 不需要分号，直接返回装饰器表达式
        return DecoratorExpression(
            at_token.line, at_token.column,
            decorator
        )
    
    def parse_function_definition_with_type_params(self, type_params):
        """
        解析带有类型参数的函数定义
        
        Args:
            type_params: 类型参数列表
        """
        # 消费func关键字
        token = self.consume(TokenType.FUNC, "Expect 'func' keyword")
        
        # 解析函数名
        name = self.consume(TokenType.IDENTIFIER, "Expect function name")
        
        # 解析函数的公共部分
        params, return_type, where_clause, body = self._parse_function_common(token, name)
        
        # 返回GenericFunctionDefinition
        return GenericFunctionDefinition(
            token.line, token.column,
            name.lexeme, type_params, params, return_type, body, where_clause
        )
    
    def parse_variable_declaration(self, mutable=False):
        """
        解析变量声明
        """
        token = self.consume(TokenType.LET if not mutable else TokenType.VAR, 
                           "Expect 'let' or 'var' keyword")
        
        # 检查是否是解构赋值
        if self.peek().type == TokenType.LBRACKET:
            # 解析数组解构
            self.advance()
            bindings = []
            while self.peek().type != TokenType.RBRACKET:
                if self.peek().type == TokenType.IDENTIFIER:
                    bindings.append(self.consume(TokenType.IDENTIFIER, "Expect variable name in destructuring").lexeme)
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                elif self.peek().type != TokenType.RBRACKET:
                    self.error("Expect ',' or ']' in array destructuring")
            self.consume(TokenType.RBRACKET, "Expect ']' to close array destructuring")
            
            # 解析类型注解（可选）
            var_type = None
            if self.peek().type == TokenType.COLON:
                self.advance()
                var_type = self.parse_type()
            
            # 解析赋值
            value = None
            if self.peek().type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
            
            # 变量声明可以带或不带分号
            if self.peek().type == TokenType.SEMICOLON:
                self.advance()
            
            return DestructuringDeclaration(
                token.line, token.column,
                bindings, var_type, value, mutable, "array"
            )
        elif self.peek().type == TokenType.LPAREN:
            # 解析元组解构
            self.advance()
            bindings = []
            while self.peek().type != TokenType.RPAREN:
                if self.peek().type == TokenType.IDENTIFIER:
                    bindings.append(self.consume(TokenType.IDENTIFIER, "Expect variable name in destructuring").lexeme)
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                elif self.peek().type != TokenType.RPAREN:
                    self.error("Expect ',' or ')' in tuple destructuring")
            self.consume(TokenType.RPAREN, "Expect ')' to close tuple destructuring")
            
            # 解析类型注解（可选）
            var_type = None
            if self.peek().type == TokenType.COLON:
                self.advance()
                var_type = self.parse_type()
            
            # 解析赋值
            value = None
            if self.peek().type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
            
            # 变量声明可以带或不带分号
            if self.peek().type == TokenType.SEMICOLON:
                self.advance()
            
            return DestructuringDeclaration(
                token.line, token.column,
                bindings, var_type, value, mutable, "tuple"
            )
        elif self.peek().type == TokenType.LBRACE:
            # 解析对象解构
            self.advance()
            bindings = []
            while self.peek().type != TokenType.RBRACE:
                if self.peek().type == TokenType.IDENTIFIER:
                    name = self.consume(TokenType.IDENTIFIER, "Expect property name in destructuring").lexeme
                    if self.peek().type == TokenType.AS:
                        self.advance()
                        alias = self.consume(TokenType.IDENTIFIER, "Expect alias name in destructuring").lexeme
                        bindings.append((name, alias))
                    else:
                        bindings.append((name, name))
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                elif self.peek().type != TokenType.RBRACE:
                    self.error("Expect ',' or '}' in object destructuring")
            self.consume(TokenType.RBRACE, "Expect '}' to close object destructuring")
            
            # 解析类型注解（可选）
            var_type = None
            if self.peek().type == TokenType.COLON:
                self.advance()
                var_type = self.parse_type()
            
            # 解析赋值
            value = None
            if self.peek().type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
            
            # 变量声明可以带或不带分号
            if self.peek().type == TokenType.SEMICOLON:
                self.advance()
            
            return DestructuringDeclaration(
                token.line, token.column,
                bindings, var_type, value, mutable, "object"
            )
        else:
            # 普通变量声明
            name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
            
            # 解析类型注解
            var_type = None
            if self.peek().type == TokenType.COLON:
                self.advance()
                var_type = self.parse_type()
            
            # 解析赋值
            value = None
            if self.peek().type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
            
            # 变量声明可以带或不带分号
            if self.peek().type == TokenType.SEMICOLON:
                self.advance()
            
            return VariableDeclaration(
                token.line, token.column,
                name.lexeme, var_type, value, mutable
            )
    
    def parse_constant_declaration(self):
        """
        解析常量声明
        """
        token = self.consume(TokenType.CONST, "Expect 'const' keyword")
        name = self.consume(TokenType.IDENTIFIER, "Expect constant name")
        
        # 解析类型注解
        const_type = None
        if self.peek().type == TokenType.COLON:
            self.advance()
            const_type = self.parse_type()
        
        # 解析赋值
        self.consume(TokenType.ASSIGN, "Expect '=' after constant declaration")
        value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after constant declaration")
        
        return ConstantDeclaration(
            token.line, token.column,
            name.lexeme, const_type, value
        )
    
    def parse_if_statement(self):
        """
        解析If语句
        """
        token = self.consume(TokenType.IF, "Expect 'if' keyword")
        
        # 解析条件表达式
        condition = self.parse_expression()
        
        # 确保条件后面跟着代码块
        if self.peek().type != TokenType.LBRACE:
            self.error("Expect '{' after condition")
        
        # 解析then分支
        then_branch = self.parse_block()
        else_branch = None
        
        # 解析else分支
        if self.peek().type == TokenType.ELSE:
            self.advance()
            if self.peek().type == TokenType.IF:
                else_branch = self.parse_if_statement()
            else:
                # 确保else后面跟着代码块
                if self.peek().type != TokenType.LBRACE:
                    self.error("Expect '{' after 'else'")
                else_branch = self.parse_block()
        
        return IfStatement(token.line, token.column, condition, then_branch, else_branch)
    
    def parse_for_loop(self):
        """
        解析For循环
        """
        token = self.consume(TokenType.FOR, "Expect 'for' keyword")
        
        # 解析变量
        variable = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        
        self.consume(TokenType.IN, "Expect 'in' after variable")
        iterable = self.parse_expression()
        
        body = self.parse_block()
        
        return ForLoop(token.line, token.column, variable.lexeme, iterable, body)
    
    def parse_while_loop(self):
        """
        解析While循环
        """
        token = self.consume(TokenType.WHILE, "Expect 'while' keyword")
        
        # 解析条件表达式
        condition = self.parse_expression()
        
        # 确保条件后面跟着代码块
        if self.peek().type != TokenType.LBRACE:
            self.error("Expect '{' after condition")
        
        # 解析循环体
        body = self.parse_block()
        
        return WhileLoop(token.line, token.column, condition, body)
    
    def parse_loop_statement(self):
        """
        解析Loop语句
        """
        token = self.consume(TokenType.LOOP, "Expect 'loop' keyword")
        body = self.parse_block()
        
        return LoopStatement(token.line, token.column, body)
    
    def parse_match_statement(self):
        """
        解析Match语句
        """
        token = self.consume(TokenType.MATCH, "Expect 'match' keyword")
        expression = self.parse_expression()
        
        self.consume(TokenType.LBRACE, "Expect '{' after expression")
        cases = []
        
        while self.peek().type != TokenType.RBRACE:
            # 解析模式
            pattern = self.parse_pattern()
            # 支持 => 箭头
            if self.peek().type == TokenType.DOUBLE_ARROW:
                self.advance()
            else:
                self.consume(TokenType.ARROW, "Expect '->' or '=>' after pattern")
            
            # 解析表达式
            case_body = self.parse_expression()
            cases.append((pattern, case_body))
            
            if self.peek().type == TokenType.COMMA:
                self.advance()
        
        self.consume(TokenType.RBRACE, "Expect '}' after match cases")
        
        return MatchStatement(token.line, token.column, expression, cases)
    
    def parse_return_statement(self):
        """
        解析Return语句
        """
        token = self.consume(TokenType.RETURN, "Expect 'return' keyword")
        
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        
        # 可选的分号
        if self.peek().type == TokenType.SEMICOLON:
            self.consume(TokenType.SEMICOLON, "Expect ';' after return statement")
        
        return ReturnStatement(token.line, token.column, value)
    
    def parse_break_statement(self):
        """
        解析Break语句
        """
        token = self.consume(TokenType.BREAK, "Expect 'break' keyword")
        self.consume(TokenType.SEMICOLON, "Expect ';' after break statement")
        
        return BreakStatement(token.line, token.column)
    
    def parse_continue_statement(self):
        """
        解析Continue语句
        """
        token = self.consume(TokenType.CONTINUE, "Expect 'continue' keyword")
        self.consume(TokenType.SEMICOLON, "Expect ';' after continue statement")
        
        return ContinueStatement(token.line, token.column)
    
    def parse_delete_variable(self):
        """
        解析删除变量语句
        """
        token = self.consume(TokenType.DEL, "Expect 'del' keyword")
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        self.consume(TokenType.SEMICOLON, "Expect ';' after delete variable statement")
        
        return DeleteVariable(token.line, token.column, name.lexeme)
    
    def parse_struct_definition(self, token=None, is_template=False):
        """
        解析结构体定义
        """
        is_generic = is_template or self.match(TokenType.GENERIC)
        
        # 获取"struct"关键字（如果已经消费，使用传入的token）
        if token is None:
            token = self.consume(TokenType.STRUCT, "Expect 'struct' keyword")
        
        # 解析结构体名称（可选，支持匿名结构体）
        name = None
        if self.peek().type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER, "Expect struct name").lexeme
        
        # 检查是否有类型参数
        type_params = None
        if is_generic or self.peek().type == TokenType.LESS_THAN:
            type_params = self.parse_type_parameters()
        
        self.consume(TokenType.LBRACE, "Expect '{' after struct name")
        fields = []
        methods = []
        
        while self.peek().type != TokenType.RBRACE:
            # 检查是否是方法定义
            if self.peek().type == TokenType.FUNC or (self.peek().type == TokenType.GENERIC and self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == TokenType.FUNC):
                # 解析方法定义
                if self.peek().type == TokenType.GENERIC:
                    # 泛型方法
                    self.advance()  # 跳过GENERIC关键字
                    # 检查是否有类型参数
                    if self.peek().type in (TokenType.LT, TokenType.LESS_THAN):
                        # 有类型参数，解析类型参数
                        method_type_params = self.parse_type_parameters()
                        # 解析函数定义，传入类型参数
                        method = self.parse_function_definition_with_type_params(method_type_params)
                    else:
                        # 没有类型参数，但仍然是泛型方法
                        method = self.parse_function_definition(is_generic=True)
                else:
                    # 普通方法
                    method = self.parse_function_definition()
                methods.append(method)
            else:
                if self.peek().type in (TokenType.VAR, TokenType.LET, TokenType.CONST):
                    self.advance()
                
                field_name = self.consume(TokenType.IDENTIFIER, "Expect field name or method definition")
                self.consume(TokenType.COLON, "Expect ':' after field name")
                field_type = self.parse_type()
                fields.append((field_name.lexeme, field_type))
                
                # 检查分号或逗号
                if self.peek().type == TokenType.SEMICOLON:
                    self.advance()
                elif self.peek().type == TokenType.COMMA:
                    self.advance()
        
        self.consume(TokenType.RBRACE, "Expect '}' after struct fields and methods")
        
        # 如果是泛型结构体，返回GenericStructDefinition
        if type_params is not None:
            return GenericStructDefinition(
                token.line, token.column,
                name, type_params, fields, methods
            )
        
        return StructDefinition(token.line, token.column, name, fields, methods)
    
    def parse_class_definition(self, token=None):
        """
        解析类定义（支持访问修饰符、构造函数、抽象类和模板类）
        """
        # 检查是否是抽象类
        is_abstract = False
        if self.peek().type == TokenType.ABSTRACT:
            self.advance()
            is_abstract = True
        
        # 获取"class"关键字（如果已经消费，使用传入的token）
        if token is None:
            token = self.consume(TokenType.CLASS, "Expect 'class' keyword")
        
        # 解析类名称
        name = self.consume(TokenType.IDENTIFIER, "Expect class name").lexeme
        
        # 检查是否有类型参数（模板类）
        type_params = None
        if self.peek().type == TokenType.LESS_THAN:
            type_params = self.parse_type_parameters()
        
        # 检查是否有继承
        parent = None
        if self.peek().type == TokenType.EXTENDS:
            self.advance()  # 消费 'extends'
            parent = self.consume(TokenType.IDENTIFIER, "Expect parent class name").lexeme
        
        self.consume(TokenType.LBRACE, "Expect '{' after class name")
        fields = []
        methods = []
        static_fields = []  # 静态字段
        static_methods = []  # 静态方法
        init_method = None  # 构造函数
        
        while self.peek().type != TokenType.RBRACE:
            # 检查是否是构造函数
            if self.peek().type == TokenType.INIT:
                init_method = self.parse_init_method()
                continue
            
            # 检查访问修饰符和static关键字（顺序不限）
            access_modifier = 'public'  # 默认访问修饰符
            is_static = False
            is_abstract_method = False  # 是否是抽象方法
            
            # 循环处理修饰符，直到遇到非修饰符token
            while True:
                if self.peek().type == TokenType.STATIC:
                    self.advance()
                    is_static = True
                elif self.peek().type == TokenType.ABSTRACT:
                    self.advance()
                    is_abstract_method = True
                elif self.peek().type == TokenType.PRIVATE:
                    self.advance()
                    access_modifier = 'private'
                elif self.peek().type == TokenType.PROTECTED:
                    self.advance()
                    access_modifier = 'protected'
                elif self.peek().type == TokenType.PUBLIC:
                    self.advance()
                    access_modifier = 'public'
                else:
                    break
            
            # 检查是否是方法定义
            if self.peek().type == TokenType.FUNC:
                # 解析方法定义
                method = self.parse_function_definition(is_abstract=is_abstract_method)
                if is_static:
                    static_methods.append((method, access_modifier))
                else:
                    methods.append((method, access_modifier))
            else:
                # 解析字段定义
                # 检查是否有 var/let/const 关键字
                if self.peek().type in (TokenType.VAR, TokenType.LET, TokenType.CONST):
                    self.advance()  # 消费关键字
                
                field_name = self.consume(TokenType.IDENTIFIER, "Expect field name or method definition")
                self.consume(TokenType.COLON, "Expect ':' after field name")
                # 解析字段类型
                field_type = self.parse_type()
                
                # 检查是否有初始值
                initial_value = None
                if self.peek().type == TokenType.ASSIGN:
                    self.advance()
                    initial_value = self.parse_expression()
                
                if is_static:
                    static_fields.append((field_name.lexeme, field_type, access_modifier, initial_value))
                else:
                    fields.append((field_name.lexeme, field_type, access_modifier))
                
                # 检查分号或逗号
                if self.peek().type == TokenType.SEMICOLON:
                    self.advance()
                elif self.peek().type == TokenType.COMMA:
                    self.advance()
        
        self.consume(TokenType.RBRACE, "Expect '}' after class fields and methods")
        
        # 如果有类型参数，返回GenericClassDefinition
        if type_params is not None:
            return GenericClassDefinition(
                token.line, token.column, 
                name, type_params, fields, methods, parent, init_method, static_fields, static_methods, is_abstract
            )
        
        return ClassDefinition(token.line, token.column, name, fields, methods, parent, init_method, static_fields, static_methods, is_abstract)
    
    def parse_init_method(self):
        """
        解析构造函数（init 方法）
        """
        init_token = self.consume(TokenType.INIT, "Expect 'init' keyword")
        
        # 解析参数列表
        self.consume(TokenType.LPAREN, "Expect '(' after 'init'")
        params = []
        if self.peek().type != TokenType.RPAREN:
            while True:
                param_name = self.consume(TokenType.IDENTIFIER, "Expect parameter name")
                self.consume(TokenType.COLON, "Expect ':' after parameter name")
                param_type = self.parse_type()
                params.append((param_name.lexeme, param_type))
                
                if self.peek().type != TokenType.COMMA:
                    break
                self.advance()
        self.consume(TokenType.RPAREN, "Expect ')' after parameters")
        
        # 解析函数体
        self.consume(TokenType.LBRACE, "Expect '{' to start function body")
        body = []
        while self.peek().type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.consume(TokenType.RBRACE, "Expect '}' after function body")
        
        # 创建函数定义节点
        from nova.compiler.parser.ast import FunctionDefinition
        return FunctionDefinition(
            init_token.line, init_token.column,
            'init', params, None, body
        )
    
    def parse_union_definition(self, token=None):
        """
        解析联合体定义
        """
        # 获取"union"关键字（如果已经消费，使用传入的token）
        if token is None:
            token = self.consume(TokenType.UNION, "Expect 'union' keyword")
        
        # 解析联合体名称（可选，支持匿名联合体）
        name = None
        if self.peek().type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER, "Expect union name").lexeme
        
        self.consume(TokenType.LBRACE, "Expect '{' after union name")
        variants = []
        
        while self.peek().type != TokenType.RBRACE:
            # 解析变体类型
            variant_type = self.parse_type()
            variants.append(variant_type)
            
            # 检查分隔符：可以是逗号或分号
            if self.peek().type == TokenType.COMMA:
                self.advance()
            elif self.peek().type == TokenType.SEMICOLON:
                self.advance()
        
        self.consume(TokenType.RBRACE, "Expect '}' after union variants")
        
        return UnionDefinition(token.line, token.column, name, variants)
    
    def parse_enum_definition(self, token=None):
        """
        解析枚举定义
        """
        # 获取"enum"关键字（如果已经消费，使用传入的token）
        if token is None:
            token = self.consume(TokenType.ENUM, "Expect 'enum' keyword")
        
        # 解析枚举名称（可选，支持匿名枚举）
        name = None
        if self.peek().type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER, "Expect enum name").lexeme
        
        self.consume(TokenType.LBRACE, "Expect '{' after enum name")
        variants = []
        
        while self.peek().type != TokenType.RBRACE:
            variant_name = self.consume(TokenType.IDENTIFIER, "Expect variant name")
            variants.append(variant_name.lexeme)
            
            if self.peek().type == TokenType.COMMA:
                self.advance()
        
        self.consume(TokenType.RBRACE, "Expect '}' after enum variants")
        
        return EnumDefinition(token.line, token.column, name, variants)
    
    def parse_trait_definition(self):
        """
        解析Trait定义
        """
        token = self.consume(TokenType.TRAIT, "Expect 'trait' keyword")
        name = self.consume(TokenType.IDENTIFIER, "Expect trait name")
        
        # 检查是否有泛型类型参数
        type_params = None
        if self.peek().type == TokenType.LESS_THAN:
            type_params = self.parse_type_parameters()
        
        self.consume(TokenType.LBRACE, "Expect '{' after trait name")
        methods = []
        
        while self.peek().type != TokenType.RBRACE:
            method = self.parse_function_signature()
            methods.append(method)
        
        self.consume(TokenType.RBRACE, "Expect '}' after trait methods")
        
        return TraitDefinition(token.line, token.column, name.lexeme, methods, type_params)
    
    def parse_impl_block(self):
        """
        解析Impl块
        """
        token = self.consume(TokenType.IMPL, "Expect 'impl' keyword")
        
        # 检查是否有泛型类型参数
        type_params = None
        if self.peek().type == TokenType.LESS_THAN:
            type_params = self.parse_type_parameters()
        
        # 解析类型名称（可能是泛型类型）
        type_name_expr = self.parse_type()
        type_name = type_name_expr
        
        # 可选的for关键字
        trait_name = None
        if self.peek().type == TokenType.FOR:
            self.advance()
            # 解析 trait 名称（可能是泛型类型）
            trait_name = self.parse_type()
        
        self.consume(TokenType.LBRACE, "Expect '{' after type name")
        methods = []
        
        while self.peek().type != TokenType.RBRACE:
            method = self.parse_function_definition()
            methods.append(method)
        
        self.consume(TokenType.RBRACE, "Expect '}' after impl methods")
        
        # 提取类型名称字符串
        # 注意：如果有 for 关键字，则第一个类型是 trait，第二个类型是 type
        # 如果没有 for 关键字，则第一个类型是 type
        if trait_name is not None:
            # 有 for 关键字：impl Trait for Type
            # type_name_expr 是 trait，trait_name 是 type，需要交换
            # 保持 TypeExpression 对象，不要转换成字符串
            type_name_final = trait_name  # 保持 trait_name 作为 TypeExpression 对象
            trait_name_final = type_name_expr  # 保持 type_name_expr 作为 TypeExpression 对象
        else:
            # 没有 for 关键字：impl Type
            type_name_final = type_name_expr  # 保持 type_name_expr 作为 TypeExpression 对象
            trait_name_final = None
        
        return ImplBlock(token.line, token.column, type_name_final, methods, trait_name_final, type_params)
    
    def parse_expression_statement(self):
        """
        解析表达式语句
        """
        expression = self.parse_expression()
        if not self.repl_mode:
            self.consume(TokenType.SEMICOLON, "Expect ';' after expression")
        elif self.peek().type == TokenType.SEMICOLON:
            self.advance()
        return expression
    
    def parse_expression(self):
        """
        解析表达式
        """
        return self.parse_assignment()
    
    def parse_assignment(self):
        """
        解析赋值表达式
        """
        expression = self.parse_null_coalescing()
        
        if self.match(TokenType.ASSIGN):
            equals = self.previous()
            value = self.parse_assignment()
            expression = BinaryExpression(
                equals.line, equals.column,
                expression, "=", value
            )
        
        return expression
    
    def parse_logical_or(self):
        """
        解析逻辑OR表达式
        """
        expression = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.parse_logical_and()
            expression = BinaryExpression(
                operator.line, operator.column,
                expression, "||", right
            )
        
        return expression
    
    def parse_null_coalescing(self):
        """
        解析空值合并表达式
        """
        expression = self.parse_logical_or()
        
        while self.match(TokenType.NULL_COALESCING):
            operator = self.previous()
            right = self.parse_logical_or()
            expression = BinaryExpression(
                operator.line, operator.column,
                expression, "??", right
            )
        
        return expression
    
    def parse_logical_and(self):
        """
        解析逻辑AND表达式
        """
        expression = self.parse_equality()
        
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.parse_equality()
            expression = BinaryExpression(
                operator.line, operator.column,
                expression, "&&", right
            )
        
        return expression
    
    def parse_equality(self):
        """
        解析相等性表达式
        """
        expression = self.parse_comparison()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.previous()
            right = self.parse_comparison()
            expression = BinaryExpression(
                operator.line, operator.column,
                expression, operator.lexeme, right
            )
        
        return expression
    
    def _is_valid_generic_instantiation(self):
        """
        检查当前位置是否是有效的泛型类型实例化
        
        泛型类型实例化的模式：
        - Identifier < Type > (    -> 泛型类型构造函数调用
        - Identifier < Type > .    -> 泛型类型静态成员访问
        
        比较操作的模式：
        - Identifier < Identifier  -> 比较操作（如 a < b）
        
        返回 True 如果是有效的泛型类型实例化，False 否则
        """
        # 保存当前位置
        saved_current = self.current
        
        try:
            # 跳过 <
            self.advance()
            
            # 解析类型参数列表
            # 类型参数可以是：int, float, string, Vector<int>, Map<string, int> 等
            while not self.is_at_end():
                # 检查是否是类型名
                if not self.check(TokenType.IDENTIFIER):
                    return False
                
                # 消费类型名
                self.advance()
                
                # 检查是否有嵌套的泛型类型，如 Vector<int>
                if self.check(TokenType.LESS_THAN):
                    # 递归检查嵌套泛型类型
                    if not self._skip_nested_generic():
                        return False
                
                # 检查是否有更多类型参数（逗号分隔）
                if self.check(TokenType.COMMA):
                    self.advance()
                    continue
                
                # 检查是否以 > 结束
                if self.check(TokenType.GREATER_THAN):
                    self.advance()
                    # 检查后面是否是 ( 或 .
                    if self.check(TokenType.LPAREN) or self.check(TokenType.DOT):
                        return True
                    return False
                
                # 如果不是以上情况，可能是比较操作
                return False
            
            return False
            
        finally:
            # 恢复位置
            self.current = saved_current
    
    def _skip_nested_generic(self):
        """
        跳过嵌套的泛型类型，如 <int> 或 <string, int>
        
        返回 True 如果成功跳过，False 否则
        """
        if not self.check(TokenType.LESS_THAN):
            return False
        
        self.advance()  # 消费 <
        
        while not self.is_at_end():
            if self.check(TokenType.IDENTIFIER):
                self.advance()
                # 检查是否有更深层次的嵌套
                if self.check(TokenType.LESS_THAN):
                    if not self._skip_nested_generic():
                        return False
            elif self.check(TokenType.COMMA):
                self.advance()
            elif self.check(TokenType.GREATER_THAN):
                self.advance()
                return True
            else:
                return False
        
        return False
    
    def parse_comparison(self):
        """
        解析比较表达式
        """
        expression = self.parse_addition()
        
        while True:
            # 检查是否是比较操作符
            if self.match(
                TokenType.LESS_THAN, TokenType.LESS_THAN_OR_EQUAL,
                TokenType.GREATER_THAN, TokenType.GREATER_THAN_OR_EQUAL
            ):
                operator = self.previous()
                right = self.parse_addition()
                expression = BinaryExpression(
                    operator.line, operator.column,
                    expression, operator.lexeme, right
                )
            else:
                break
        
        return expression
    
    def parse_addition(self):
        """
        解析加法表达式
        """
        expression = self.parse_multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.parse_multiplication()
            expression = BinaryExpression(
                operator.line, operator.column,
                expression, operator.lexeme, right
            )
        
        return expression
    
    def parse_multiplication(self):
        """
        解析乘法表达式
        """
        expression = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.previous()
            right = self.parse_unary()
            expression = BinaryExpression(
                operator.line, operator.column,
                expression, operator.lexeme, right
            )
        
        return expression
    
    def parse_unary(self):
        """
        解析一元表达式
        """
        # 处理取地址表达式 &x 或 &mut x
        if self.match(TokenType.AMPERSAND):
            operator = self.previous()
            # 检查是否是可变引用 &mut
            is_mutable = False
            if self.peek().type == TokenType.MUT:
                self.advance()  # 消耗 mut
                is_mutable = True
            right = self.parse_unary()
            return AddressOfExpression(
                operator.line, operator.column,
                right, is_mutable
            )
        
        # 处理解引用表达式 *ptr
        if self.match(TokenType.MULTIPLY):
            operator = self.previous()
            right = self.parse_unary()
            return DereferenceExpression(
                operator.line, operator.column,
                right
            )
        
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous()
            right = self.parse_unary()
            return UnaryExpression(
                operator.line, operator.column,
                operator.lexeme, right
            )
        
        primary = self.parse_primary()
        
        # 优化链式调用处理，使用循环而不是递归检查
        while True:
            # 检查是否是可选链成员访问
            if self.peek().type == TokenType.OPTIONAL_CHAIN:
                # 消耗可选链操作符 ?.
                self.advance()
                # 解析成员名
                member_name = self.consume(TokenType.IDENTIFIER, "Expect member name after optional chain operator")
                # 创建可选链表达式
                primary = OptionalChainExpression(
                    primary.line, primary.column,
                    primary, member_name.lexeme
                )
            # 检查是否是成员访问
            elif self.peek().type == TokenType.DOT:
                primary = self.parse_member_access(primary)
            # 检查是否是函数调用
            elif self.peek().type == TokenType.LPAREN:
                primary = self.parse_call(primary, consume_lparen=True)
            else:
                break
        
        return primary
    
    def parse_primary(self):
        """
        解析 primary 表达式
        """
        # 解析await表达式
        if self.match(TokenType.AWAIT):
            await_token = self.previous()
            expression = self.parse_primary()
            return AwaitExpression(
                await_token.line, await_token.column,
                expression
            )
        
        if self.match(TokenType.FALSE):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                False, "boolean"
            )
        elif self.match(TokenType.TRUE):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                True, "boolean"
            )
        elif self.match(TokenType.INTEGER):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                self.previous().literal, "integer"
            )
        elif self.match(TokenType.FLOAT):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                self.previous().literal, "float"
            )
        elif self.match(TokenType.STRING):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                self.previous().literal, "string"
            )
        elif self.match(TokenType.BOOLEAN):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                self.previous().literal, "boolean"
            )
        elif self.match(TokenType.F_STRING_START):
            # 解析f-string
            parts = []
            while not self.is_at_end():
                # 这里简化处理，实际应该解析f-string的各个部分
                # 包括普通字符串部分和表达式部分
                if self.peek().type == TokenType.F_STRING_EXPRESSION_START:
                    self.advance()
                    # 解析表达式
                    expr = self.parse_expression()
                    parts.append(("expression", expr))
                    # 消耗F_STRING_EXPRESSION_END
                    if self.peek().type == TokenType.F_STRING_EXPRESSION_END:
                        self.advance()
                elif self.peek().type == TokenType.STRING:
                    # 处理普通字符串部分
                    string_token = self.advance()
                    parts.append(("string", string_token.literal))
                else:
                    break
            return StringInterpolationExpression(
                self.previous().line, self.previous().column,
                parts
            )
        elif self.match(TokenType.CHARACTER):
            return LiteralExpression(
                self.previous().line, self.previous().column,
                self.previous().literal, "character"
            )
        elif self.match(TokenType.SELF):
            name = "self"
            line = self.previous().line
            column = self.previous().column
            
            # 检查是否是成员访问
            if self.peek().type == TokenType.DOT:
                return self.parse_member_access(IdentifierExpression(
                    line, column, name
                ))
            else:
                return IdentifierExpression(
                    line, column, name
                )
        elif self.match(TokenType.THIS):
            name = "this"
            line = self.previous().line
            column = self.previous().column
            
            # 检查是否是成员访问
            if self.peek().type == TokenType.DOT:
                return self.parse_member_access(IdentifierExpression(
                    line, column, name
                ))
            else:
                return IdentifierExpression(
                    line, column, name
                )
        elif self.match(TokenType.SUPER):
            name = "super"
            line = self.previous().line
            column = self.previous().column
            
            # 检查是否是成员访问
            if self.peek().type == TokenType.DOT:
                return self.parse_member_access(IdentifierExpression(
                    line, column, name
                ))
            else:
                return IdentifierExpression(
                    line, column, name
                )
        elif self.match(TokenType.STRUCT):
            return self.parse_struct_definition(self.previous())
        elif self.match(TokenType.UNION):
            return self.parse_union_definition(self.previous())
        elif self.match(TokenType.ENUM):
            return self.parse_enum_definition(self.previous())
        elif self.match(TokenType.TYPE):
            # 解析type表达式 type: T
            type_token = self.previous()
            if self.match(TokenType.COLON):
                # 解析类型
                wrapped_type = self.parse_type()
                return TypeTypeExpression(
                    type_token.line, type_token.column,
                    wrapped_type
                )
            else:
                # 没有指定类型，返回通用的type
                return TypeTypeExpression(
                    type_token.line, type_token.column,
                    None
                )
        elif self.match(TokenType.FUNC):
            # 解析匿名函数/lambda表达式
            line = self.previous().line
            column = self.previous().column
            
            # 解析参数
            self.consume(TokenType.LPAREN, "Expect '(' after 'func'")
            params = []
            if self.peek().type != TokenType.RPAREN:
                while True:
                    param_name = self.consume(TokenType.IDENTIFIER, "Expect parameter name")
                    self.consume(TokenType.COLON, "Expect ':' after parameter name")
                    param_type = self.parse_type()
                    params.append((param_name.lexeme, param_type))
                    
                    if self.peek().type != TokenType.COMMA:
                        break
                    self.advance()
            self.consume(TokenType.RPAREN, "Expect ')' after parameters")
            
            # 解析返回类型
            return_type = None
            if self.peek().type == TokenType.ARROW:
                self.advance()
                return_type = self.parse_type()
            
            # 解析函数体
            body = self.parse_block()
            
            return LambdaExpression(
                line, column, params, body
            )
        elif self.match(TokenType.IDENTIFIER):
            name = self.previous().lexeme
            line = self.previous().line
            column = self.previous().column
            
            # 检查是否是泛型类型实例化
            # 只有当 < 后面跟着有效的类型参数列表，并且后面跟着 ( 或 . 时才认为是泛型类型
            if self.peek().type == TokenType.LESS_THAN and self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == TokenType.IDENTIFIER:
                # 尝试解析类型参数列表，看看是否是有效的泛型类型实例化
                if self._is_valid_generic_instantiation():
                    # 消费左括号
                    self.consume(TokenType.LESS_THAN, "Expect '<' after type name")
                    type_args = []
                    
                    if self.peek().type != TokenType.GREATER_THAN:
                        while True:
                            type_arg = self.parse_type()
                            type_args.append(type_arg)
                            
                            if self.peek().type != TokenType.COMMA:
                                break
                            self.advance()
                    
                    self.consume(TokenType.GREATER_THAN, "Expect '>' after type arguments")
                    
                    # 创建泛型类型表达式
                    callee = GenericTypeExpression(line, column, name, type_args)
                    
                    # 检查是否是调用
                    if self.peek().type == TokenType.LPAREN:
                        return self.parse_call(callee, consume_lparen=True)
                    # 检查是否是成员访问
                    elif self.peek().type == TokenType.DOT:
                        return self.parse_member_access(callee)
                    else:
                        return callee
            
            # 检查是否是调用（可能是泛型类型调用，需要类型推断）
            if self.peek().type == TokenType.LPAREN:
                # 创建标识符表达式
                callee = IdentifierExpression(line, column, name)
                return self.parse_call(callee, consume_lparen=True)
            # 检查是否是成员访问
            elif self.peek().type == TokenType.DOT:
                return self.parse_member_access(IdentifierExpression(
                    self.previous().line, self.previous().column, name
                ))
            else:
                return IdentifierExpression(
                    self.previous().line, self.previous().column, name
                )
        elif self.match(TokenType.LPAREN):
            # 检查是否是元组字面量
            if self.peek().type == TokenType.RPAREN:
                # 空元组
                self.consume(TokenType.RPAREN, "Expect ')' after '('")
                return TupleLiteralExpression(
                    self.previous().line, self.previous().column,
                    []
                )
            
            # 解析第一个表达式
            first_expr = self.parse_expression()
            
            # 检查是否是元组
            if self.peek().type == TokenType.COMMA:
                # 元组字面量
                elements = [first_expr]
                while self.match(TokenType.COMMA):
                    elements.append(self.parse_expression())
                self.consume(TokenType.RPAREN, "Expect ')' after tuple elements")
                return TupleLiteralExpression(
                    self.previous().line, self.previous().column,
                    elements
                )
            else:
                # 括号表达式
                self.consume(TokenType.RPAREN, "Expect ')' after expression")
                return first_expr
        elif self.match(TokenType.LBRACKET):
            # 解析数组字面量
            elements = []
            
            if self.peek().type != TokenType.RBRACKET:
                while True:
                    elements.append(self.parse_expression())
                    
                    if self.peek().type != TokenType.COMMA:
                        break
                    self.advance()
            
            self.consume(TokenType.RBRACKET, "Expect ']' after array elements")
            
            return ArrayLiteralExpression(
                self.previous().line, self.previous().column,
                elements
            )
        else:
            self.error("Expect expression")
    
    def parse_call(self, callee, consume_lparen=True):
        """
        解析函数调用
        
        Args:
            callee: 被调用的表达式
            consume_lparen: 是否消费左括号
        """
        arguments = []
        
        if consume_lparen:
            self.consume(TokenType.LPAREN, "Expect '(' after function name")
        
        if self.peek().type != TokenType.RPAREN:
            while True:
                # 检查是否是命名参数
                if self.peek().type == TokenType.IDENTIFIER and self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == TokenType.COLON:
                    # 命名参数: name: value
                    param_name = self.consume(TokenType.IDENTIFIER, "Expect parameter name").lexeme
                    self.consume(TokenType.COLON, "Expect ':' after parameter name")
                    param_value = self.parse_expression()
                    arguments.append(NamedArgumentExpression(
                        self.previous().line, self.previous().column,
                        param_name, param_value
                    ))
                else:
                    # 位置参数
                    arguments.append(self.parse_expression())
                
                # 遇到逗号或右括号时停止
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                elif self.peek().type == TokenType.RPAREN:
                    break
                else:
                    # 如果不是逗号或右括号，报错
                    self.error("Expect ',' or ')' after argument")
        self.consume(TokenType.RPAREN, "Expect ')' after arguments")
        
        call_expr = CallExpression(
            callee.line, callee.column,
            callee, arguments
        )
        
        # 检查是否有更多的成员访问
        if self.peek().type == TokenType.DOT:
            return self.parse_member_access(call_expr)
        
        return call_expr
    
    def parse_member_access(self, object):
        """
        解析成员访问
        """
        while self.match(TokenType.DOT):
            member = self.consume(TokenType.IDENTIFIER, "Expect member name")
            object = MemberExpression(
                self.previous().line, self.previous().column,
                object, member.lexeme
            )
        
        # 检查是否是函数调用
        if self.peek().type == TokenType.LPAREN:
            object = self.parse_call(object, consume_lparen=True)
        
        return object
    
    def parse_pattern(self):
        """
        解析模式
        """
        # 简化实现，仅支持标识符和字面量
        if self.peek().type == TokenType.IDENTIFIER:
            return self.consume(TokenType.IDENTIFIER, "Expect pattern").lexeme
        elif self.peek().type in [TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.CHARACTER, TokenType.TRUE, TokenType.FALSE]:
            return self.advance().literal
        else:
            self.error("Expect pattern")
    
    def parse_function_signature(self):
        """
        解析函数签名
        """
        # 可选的func关键字
        if self.peek().type == TokenType.FUNC:
            self.advance()
        
        name = self.consume(TokenType.IDENTIFIER, "Expect function name")
        
        # 解析参数
        self.consume(TokenType.LPAREN, "Expect '(' after function name")
        params = []
        if self.peek().type != TokenType.RPAREN:
            while True:
                # 参数名可以是IDENTIFIER或SELF关键字
                if self.peek().type == TokenType.SELF:
                    param_name = self.advance()
                else:
                    param_name = self.consume(TokenType.IDENTIFIER, "Expect parameter name")
                self.consume(TokenType.COLON, "Expect ':' after parameter name")
                param_type = self.parse_type()
                params.append((param_name.lexeme, param_type))
                
                if self.peek().type != TokenType.COMMA:
                    break
                self.advance()
        self.consume(TokenType.RPAREN, "Expect ')' after parameters")
        
        # 解析返回类型
        return_type = None
        if self.peek().type == TokenType.ARROW:
            self.advance()
            return_type = self.parse_type()
        elif self.peek().type == TokenType.COLON:
            self.advance()
            return_type = self.parse_type()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after function signature")
        
        return (name.lexeme, params, return_type)
    
    def parse_block(self):
        """
        解析代码块
        """
        statements = []
        self.consume(TokenType.LBRACE, "Expect '{' to start block")
        
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        
        self.consume(TokenType.RBRACE, "Expect '}' to end block")
        return statements
    
    def match(self, *types):
        """
        匹配Token类型
        
        Args:
            *types: Token类型列表
        
        Returns:
            bool: 是否匹配
        """
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type):
        """
        检查当前Token类型
        
        Args:
            type: Token类型
        
        Returns:
            bool: 是否匹配
        """
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def advance(self):
        """
        前进到下一个Token
        
        Returns:
            Token: 当前Token
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        """
        是否到达Token列表末尾
        
        Returns:
            bool: 是否到达末尾
        """
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        """
        查看当前Token
        
        Returns:
            Token: 当前Token
        """
        return self.tokens[self.current]
    
    def previous(self):
        """
        查看前一个Token
        
        Returns:
            Token: 前一个Token
        """
        return self.tokens[self.current - 1]
    
    def error(self, message):
        """
        生成错误信息，提供更详细的上下文
        
        Args:
            message: 错误信息
        
        Raises:
            ParserError: 语法分析错误
        """
        token = self.peek()
        # 提供更详细的错误信息，包括当前位置和期望的内容
        raise ParserError(token.line, token.column, message)
    
    def consume(self, type, message):
        """
        消耗指定类型的Token
        
        Args:
            type: Token类型
            message: 错误信息
        
        Returns:
            Token: 消耗的Token
        
        Raises:
            ParserError: 语法分析错误
        """
        if self.check(type):
            return self.advance()
        self.error(message)
    
    def parse_type_parameters(self):
        """
        解析泛型类型参数
        
        Returns:
            list: 类型参数列表
        """
        self.consume(TokenType.LESS_THAN, "Expect '<' after generic keyword")
        type_params = []
        
        if self.peek().type != TokenType.GREATER_THAN:
            while True:
                param_name = self.consume(TokenType.IDENTIFIER, "Expect type parameter name")
                type_params.append(GenericTypeParameter(
                    param_name.line, param_name.column,
                    param_name.lexeme
                ))
                
                if self.peek().type != TokenType.COMMA:
                    break
                self.advance()
        
        self.consume(TokenType.GREATER_THAN, "Expect '>' after type parameters")
        return type_params
    
    def parse_where_clause(self):
        """
        解析where子句
        
        Returns:
            WhereClause: where子句节点
        """
        # where关键字已经在调用前被match了，所以不需要再次消费
        constraints = []
        
        while True:
            type_param = self.consume(TokenType.IDENTIFIER, "Expect type parameter name")
            self.consume(TokenType.COLON, "Expect ':' after type parameter")
            
            # 解析第一个 trait 名称（可能是泛型类型）
            trait_name = self.parse_type()
            trait_names = [trait_name]
            
            # 检查是否有多个 trait 约束（使用 + 连接）
            while self.peek().type == TokenType.PLUS:
                self.advance()
                trait_name = self.parse_type()
                trait_names.append(trait_name)
            
            constraints.append(TypeConstraint(
                type_param.line, type_param.column,
                type_param.lexeme, trait_names
            ))
            
            if self.peek().type != TokenType.COMMA:
                break
            self.advance()
        
        return WhereClause(
            self.peek().line, self.peek().column,
            constraints
        )
    
    def parse_type(self):
        """
        解析类型
        
        Returns:
            TypeExpression: 类型表达式对象
        """
        # 检查是否是指针类型 *T 或 *mut T
        if self.peek().type == TokenType.MULTIPLY:
            self.advance()  # 消费 *
            # 检查是否是可变指针 *mut T
            is_mutable = False
            if self.peek().type == TokenType.MUT:
                self.advance()  # 消费 mut
                is_mutable = True
            pointee_type = self.parse_type()
            return PointerTypeExpression(
                self.previous().line, self.previous().column,
                pointee_type, is_mutable
            )
        
        # 检查是否是元组类型 (T, U, ...)
        if self.peek().type == TokenType.LPAREN:
            self.advance()
            element_types = []
            
            if self.peek().type != TokenType.RPAREN:
                while True:
                    element_types.append(self.parse_type())
                    
                    if self.peek().type != TokenType.COMMA:
                        break
                    self.advance()
            
            self.consume(TokenType.RPAREN, "Expect ')' after tuple element types")
            
            # 如果只有一个元素，不是元组，而是括号分组
            if len(element_types) == 1:
                return element_types[0]
            
            return TupleTypeExpression(
                self.previous().line, self.previous().column,
                element_types
            )
        
        # 检查是否是数组类型
        if self.peek().type == TokenType.LBRACKET:
            self.advance()
            element_type = self.parse_type()
            self.consume(TokenType.RBRACKET, "Expect ']' after array element type")
            return ArrayTypeExpression(
                self.previous().line, self.previous().column,
                element_type
            )
        
        # 检查是否是函数类型 func(T): U 或 func(T) -> U
        if self.peek().type == TokenType.FUNC:
            self.advance()
            self.consume(TokenType.LPAREN, "Expect '(' after 'func'")
            param_types = []
            
            if self.peek().type != TokenType.RPAREN:
                while True:
                    param_types.append(self.parse_type())
                    
                    if self.peek().type != TokenType.COMMA:
                        break
                    self.advance()
            
            self.consume(TokenType.RPAREN, "Expect ')' after parameter types")
            
            # 支持两种语法：func(T): U 和 func(T) -> U
            if self.peek().type == TokenType.ARROW:
                self.advance()  # 消费 ->
            elif self.peek().type == TokenType.COLON:
                self.advance()  # 消费 :
            else:
                self.error("Expect ':' or '->' after parameter types")
            
            return_type = self.parse_type()
            
            return FunctionTypeExpression(
                self.previous().line, self.previous().column,
                param_types, return_type
            )
        
        # 检查是否是type类型（类型类型）
        if self.peek().type == TokenType.TYPE:
            self.advance()  # 消费 type
            # 检查是否有冒号和具体类型 type: T
            if self.peek().type == TokenType.COLON:
                self.advance()  # 消费 :
                wrapped_type = self.parse_type()
                return TypeTypeExpression(
                    self.previous().line, self.previous().column,
                    wrapped_type
                )
            else:
                # 没有指定具体类型，返回通用的type类型
                return TypeTypeExpression(
                    self.previous().line, self.previous().column,
                    None
                )
        
        # 检查是否是泛型类型或简单类型
        if self.peek().type == TokenType.IDENTIFIER:
            token = self.consume(TokenType.IDENTIFIER, "Expect type name")
            base_type = token.lexeme
            
            # 检查是否有类型参数
            if self.peek().type == TokenType.LESS_THAN:
                # 消费左括号
                self.consume(TokenType.LESS_THAN, "Expect '<' after type name")
                type_args = []
                
                if self.peek().type != TokenType.GREATER_THAN:
                    while True:
                        type_arg = self.parse_type()
                        type_args.append(type_arg)
                        
                        if self.peek().type != TokenType.COMMA:
                            break
                        self.advance()
                
                self.consume(TokenType.GREATER_THAN, "Expect '>' after type arguments")
                return GenericTypeExpression(
                    token.line, token.column,
                    base_type, type_args
                )
            
            # 对于简单类型，返回TypeExpression对象
            return TypeExpression(
                token.line, token.column,
                base_type
            )
        
        # 如果不是标识符，尝试消费一个标识符作为类型名
        token = self.consume(TokenType.IDENTIFIER, "Expect type name")
        return TypeExpression(
            token.line, token.column,
            token.lexeme
        )
