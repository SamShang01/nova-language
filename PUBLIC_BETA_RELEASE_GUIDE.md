# Nova 语言公测发布指南

本指南将帮助你完成Nova语言的公测发布工作。请按照以下步骤逐步执行。

## 第一步：创建GitHub仓库（如果还没有）

### 1.1 在GitHub上创建仓库
1. 访问 https://github.com
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `nova-language`
   - Description: `Nova Programming Language - A modern, type-safe language with powerful features`
   - 选择 Public（公开）
   - 勾选 "Add a README file"
   - 选择 MIT License
4. 点击 "Create repository"

### 1.2 初始化本地Git仓库
在项目根目录打开PowerShell，执行以下命令：

```powershell
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 创建第一次提交
git commit -m "Initial commit: Nova Language v0.16.0"

# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/nova-language.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 第二步：创建发布版本

### 2.1 创建版本标签
```powershell
# 创建v0.16.0标签
git tag -a v0.16.0 -m "Nova Language v0.16.0 - Public Beta Release"

# 推送标签到GitHub
git push origin v0.16.0
```

### 2.2 在GitHub上创建Release
1. 访问你的GitHub仓库页面
2. 点击右侧的 "Releases"
3. 点击 "Draft a new release"
4. 填写发布信息：
   - Tag: v0.16.0
   - Title: Nova Language v0.16.0 - Public Beta
   - Description: 复制下面的内容

```markdown
# Nova Language v0.16.0 - Public Beta Release

## 🎉 欢迎参加Nova语言公测！

Nova是一个现代化的编程语言，具有强大的类型系统、泛型支持、Trait系统和丰富的标准库。

## ✨ 主要特性

- **类型系统**: 支持基本类型、复合类型、泛型和类型推断
- **Trait系统**: 支持接口定义和约束
- **函数式编程**: 支持Lambda表达式和高阶函数
- **异步编程**: 支持async/await
- **标准库**: 丰富的STL、数学、字符串、集合等库

## 📦 安装方式

### 方式一：通过pip安装
```bash
pip install nova-language
```

### 方式二：从源码安装
```bash
git clone https://github.com/YOUR_USERNAME/nova-language.git
cd nova-language
pip install -e .
```

## 🚀 快速开始

### 运行REPL
```bash
nova repl
```

### 运行Nova程序
```bash
nova run your_program.nova
```

### 编译Nova程序
```bash
nova compile your_program.nova
```

## 📚 文档

- [语言说明书](NOVA_LANGUAGE_MANUAL.md)
- [开发工具指南](DEVELOPMENT_TOOLS.md)
- [STL用户指南](STL_USER_GUIDE.md)

## 🛠️ 开发工具

### VS Code插件
- 语法高亮
- 代码片段
- 代码运行
- 代码格式化

### Nova IDE
- 图形界面IDE
- 文件管理
- 代码编辑

## 🧪 测试状态

- 总测试数: 114
- 通过率: 100%
- 测试覆盖: 词法、语法、语义、虚拟机、标准库

## 📝 示例代码

```nova
// Hello World
func main() -> void {
    print("Hello, Nova!");
}

// 泛型函数
func max<T: Comparable>(a: T, b: T) -> T {
    if a > b {
        return a;
    } else {
        return b;
    }
}

// 异步编程
async func fetchData() -> string {
    await delay(1000);
    return "Data loaded";
}
```

## 🐛 反馈问题

如果你在使用过程中遇到问题，请：
1. 在GitHub上创建Issue
2. 描述问题的详细情况
3. 提供复现步骤
4. 附上相关的代码和错误信息

## 📄 许可证

MIT License

---

**感谢你参与Nova语言的公测！**
```

5. 点击 "Publish release"

## 第三步：发布到PyPI（Python包索引）

### 3.1 安装发布工具
```powershell
pip install build twine
```

### 3.2 构建发布包
```powershell
# 在项目根目录执行
python -m build
```

### 3.3 上传到PyPI
```powershell
# 先上传到TestPyPI测试
twine upload --repository testpypi dist/*

# 测试通过后，上传到正式PyPI
twine upload dist/*
```

**注意**: 你需要先在 https://pypi.org 和 https://test.pypi.org 注册账号。

## 第四步：发布VS Code插件

### 4.1 安装vsce工具
```powershell
npm install -g @vscode/vsce
```

### 4.2 打包插件
```powershell
cd vscode-extension/nova-language
vsce package
```

### 4.3 发布到VS Code Marketplace
1. 访问 https://marketplace.visualstudio.com
2. 点击 "Publish extensions"
3. 登录你的Microsoft账号
4. 上传生成的 `.vsix` 文件

## 第五步：宣传和推广

### 5.1 社交媒体宣传
在以下平台发布消息：
- Twitter/X
- Reddit (r/programming, r/python, r/ProgrammingLanguages)
- Hacker News
- V2EX
- 掘金
- 思否

### 5.2 发布模板
```
🚀 Nova语言公测开始！

Nova是一个现代化的编程语言，具有：
✅ 强大的类型系统
✅ 泛型和Trait支持
✅ 异步编程
✅ 丰富的标准库

安装：pip install nova-language
文档：https://github.com/YOUR_USERNAME/nova-language

欢迎试用和反馈！
#NovaLanguage #ProgrammingLanguage #OpenSource
```

## 第六步：收集反馈

### 6.1 创建Issue模板
在GitHub仓库中创建 `.github/ISSUE_TEMPLATE/bug_report.md`：

```markdown
---
name: Bug report
about: 报告一个bug
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug描述
请清楚地描述这个bug。

## 复现步骤
1. 执行 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

## 期望行为
描述你期望发生什么。

## 实际行为
描述实际发生了什么。

## 截图
如果适用，添加截图来帮助解释问题。

## 环境信息
- OS: [例如 Windows 10]
- Python版本: [例如 3.9.0]
- Nova版本: [例如 0.16.0]

## 附加信息
添加任何其他关于问题的信息。
```

### 6.2 创建功能请求模板
创建 `.github/ISSUE_TEMPLATE/feature_request.md`：

```markdown
---
name: Feature request
about: 提出一个新功能建议
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## 功能描述
清楚地描述你想要的功能。

## 为什么需要这个功能？
解释为什么这个功能对项目有用。

## 建议的实现方式
如果你有实现想法，请描述。

## 附加信息
添加任何其他相关信息或截图。
```

## 第七步：持续维护

### 7.1 定期检查
- 每天查看GitHub Issues
- 回复用户问题
- 记录反馈和建议

### 7.2 发布更新
- 修复关键bug
- 添加常用功能
- 更新文档

### 7.3 版本管理
- 遵循语义化版本号
- 更新CHANGELOG.md
- 创建新的Release

## 常见问题

### Q: 我没有GitHub账号怎么办？
A: 访问 https://github.com/signup 注册一个免费账号。

### Q: 我没有PyPI账号怎么办？
A: 访问 https://pypi.org/account/register/ 注册账号。

### Q: 我不会使用Git怎么办？
A: 可以使用GitHub Desktop图形界面工具，或者参考Git教程。

### Q: 我没有Microsoft账号怎么办？
A: 访问 https://account.microsoft.com 注册账号。

### Q: 我可以跳过某些步骤吗？
A: 可以。最简单的方式是只创建GitHub Release，让用户从源码安装。

## 最简发布流程（推荐新手）

如果你觉得上面的步骤太复杂，可以只执行以下最简步骤：

1. **创建GitHub仓库并上传代码**
   ```powershell
   git init
   git add .
   git commit -m "Nova Language v0.16.0"
   git remote add origin https://github.com/YOUR_USERNAME/nova-language.git
   git push -u origin main
   ```

2. **创建Release**
   - 在GitHub上创建v0.16.0 Release
   - 添加发布说明

3. **告知用户安装方式**
   ```bash
   git clone https://github.com/YOUR_USERNAME/nova-language.git
   cd nova-language
   pip install -e .
   ```

这样就完成了最基本的发布！

## 需要帮助？

如果你在执行过程中遇到任何问题，可以：
1. 查看GitHub文档：https://docs.github.com
2. 查看PyPI文档：https://packaging.python.org
3. 查看VS Code扩展文档：https://code.visualstudio.com/api

---

**祝发布顺利！** 🎉