# ============================================================
# Nova 语言公测准备 - 自动化测试脚本
# ============================================================
# 使用方法：在 PowerShell 中运行 .\public_beta_commands.ps1
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Nova 语言公测准备 - 自动化测试脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# 阶段一：核心功能修复
# ============================================================
Write-Host "阶段一：核心功能修复" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

# 任务 1.1：修复词法分析器测试失败
Write-Host "`n[任务 1.1] 检查词法分析器运算符定义..." -ForegroundColor Green
python -c "from nova.compiler.lexer.tokens import TokenType; print([t for t in dir(TokenType) if 'AND' in t or 'OR' in t or 'AMPERSAND' in t or 'PIPE' in t])"

Write-Host "`n[任务 1.1] 运行词法分析器测试..." -ForegroundColor Green
python -m unittest tests.test_lexer.TestLexer.test_scan_operators -v

# 任务 1.2：修复语义分析器返回类型检查
Write-Host "`n[任务 1.2] 运行语义分析器测试..." -ForegroundColor Green
python -m unittest tests.test_semantic.TestSemanticAnalyzer.test_analyze_simple_program -v

# 任务 1.3：修复Trait系统未定义标识符错误
Write-Host "`n[任务 1.3] 运行Trait测试..." -ForegroundColor Green
python -m unittest tests.test_traits.TestTraits.test_multiple_trait_constraints -v

# ============================================================
# 阶段二：功能完善
# ============================================================
Write-Host "`n阶段二：功能完善" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

# 任务 2.1：完善标准库函数
Write-Host "`n[任务 2.1] 运行标准库测试..." -ForegroundColor Green
python -m unittest tests.test_stdlib -v

Write-Host "`n[任务 2.1] 测试字符串模块..." -ForegroundColor Green
python -m unittest tests.test_string_module -v

Write-Host "`n[任务 2.1] 测试数学模块..." -ForegroundColor Green
python -m unittest tests.test_math_module -v

# 任务 2.2：完善泛型系统
Write-Host "`n[任务 2.2] 运行泛型结构体测试..." -ForegroundColor Green
python -m unittest tests.test_generic_structs -v

Write-Host "`n[任务 2.2] 运行泛型函数测试..." -ForegroundColor Green
python -m unittest tests.test_generic_functions -v

# 任务 2.3：完善虚拟机
Write-Host "`n[任务 2.3] 运行虚拟机测试..." -ForegroundColor Green
python -m unittest tests.test_vm -v

# ============================================================
# 阶段三：性能优化
# ============================================================
Write-Host "`n阶段三：性能优化" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

# 任务 3.1：启用LLVM JIT编译器
Write-Host "`n[任务 3.1] 测试LLVM编译器..." -ForegroundColor Green
python -c "from nova.compiler.llvm_compiler import LLVMCompiler; print('LLVM OK')"

Write-Host "`n[任务 3.1] 检查llvmlite是否安装..." -ForegroundColor Green
python -c "import llvmlite; print('llvmlite version:', llvmlite.__version__)"

# 任务 3.2：启用并行编译
Write-Host "`n[任务 3.2] 测试并行编译..." -ForegroundColor Green
python -c "from nova.compiler.parallel import ParallelCompiler; print('Parallel OK')"

# ============================================================
# 阶段四：文档和测试
# ============================================================
Write-Host "`n阶段四：文档和测试" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

# 任务 4.1：完善测试覆盖率
Write-Host "`n[任务 4.1] 检查pytest是否安装..." -ForegroundColor Green
python -c "import pytest; print('pytest version:', pytest.__version__)" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "pytest 未安装，正在安装..." -ForegroundColor Yellow
    pip install pytest pytest-cov
}

# 任务 4.2：更新文档
Write-Host "`n[任务 4.2] 检查文档是否存在..." -ForegroundColor Green
python -c "import os; print('Manual exists:', os.path.exists('NOVA_LANGUAGE_MANUAL.md'))"
python -c "import os; print('Changelog exists:', os.path.exists('CHANGELOG.md'))"

# ============================================================
# 阶段五：发布准备
# ============================================================
Write-Host "`n阶段五：发布准备" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

# 任务 5.1：版本存档
Write-Host "`n[任务 5.1] 检查版本存档..." -ForegroundColor Green
python -c "import os; print('Version archive exists:', os.path.exists('versions/0.16.0'))"

# 任务 5.2：构建和安装
Write-Host "`n[任务 5.2] 测试版本命令..." -ForegroundColor Green
python -m nova --version

Write-Host "`n[任务 5.2] 测试REPL..." -ForegroundColor Green
echo "print('Hello, Nova!');" | python -m nova.repl

# 任务 5.3：最终测试
Write-Host "`n[任务 5.3] 运行所有测试..." -ForegroundColor Green
python -m unittest discover -s tests -v

# ============================================================
# 总结
# ============================================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "测试完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "请检查以上输出，修复所有错误和失败。" -ForegroundColor Yellow
Write-Host "详细计划请查看: PUBLIC_BETA_PLAN.md" -ForegroundColor Yellow
