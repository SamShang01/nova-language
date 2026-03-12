# 修改语义分析器以增强类型检查

$file_path = "e:\nova\src\nova\compiler\semantic\analyzer.py"

# 读取文件内容
$content = Get-Content -Path $file_path -Raw -Encoding UTF8

# 1. 修改 _types_compatible 函数，使其更严格
$old_code = "        # 允许int和float之间的隐式转换
        if (type1 == INT_TYPE and type2 == FLOAT_TYPE) or (type1 == FLOAT_TYPE and type2 == INT_TYPE):
            return True"

$new_code = "        # 严格类型检查：不允许隐式类型转换"

if ($content -match [regex]::Escape($old_code)) {
    $content = $content -replace [regex]::Escape($old_code), $new_code
    Write-Host "已修改 _types_compatible 函数" -ForegroundColor Green
} else {
    Write-Host "未找到 _types_compatible 函数中的旧代码" -ForegroundColor Yellow
}

# 写回文件
Set-Content -Path $file_path -Value $content -Encoding UTF8 -NoNewline

Write-Host "语义分析器修改完成！" -ForegroundColor Green
