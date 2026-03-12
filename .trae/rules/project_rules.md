## 📋 版本管理规则

### 编译器版本管理
1. 每个版本的更新都需要在项目的`CHANGELOG.md`文件中进行记录。
2. `CHANGELOG.md`只包含最新版本的更新内容，并在末尾添加链接指向`CHANGELOG_ALL.md`。
3. `CHANGELOG_ALL.md`包含所有版本的完整更新记录，按版本号从新到旧排列。
4. 每个版本存档目录（`versions/x.y.z/`）中的`CHANGELOG.md`只包含该版本的更新内容，不包含其他版本的内容。
5. 每个小版本（bugfix）都需要有__version__字段，格式为`__version__ = (x,y,z)`，其中x、y、z分别为版本号的主、次、修订号。
6. 每个版本都要有if __version__>=(x,y,z)，用于判断当前版本是否大于等于该版本，其中(x,y,z)可以大于等于当前版本的任意一个数字。
7. 每个版本都要有完整的编译器系统存档，存档到`versions/x.y.z/`目录，包括：
   - 完整的src目录（包含所有编译器代码）
   - version.py文件（记录版本号）
   - CHANGELOG.md文件（记录该版本的变更，只包含该版本的内容）
   - README.md文件（版本说明）
8. 要有一个script.py文件，支持cli版本和gui版本，还有install --version==x.y.z的命令，用于安装指定版本的nova语言。
9. 要有一个setup.py文件，用于安装nova语言。
10. 每次更新版本时，必须先将当前版本的完整编译器系统存档到versions目录，然后再更新版本号。
11. 版本存档必须包含所有源代码文件，确保可以独立运行。

### 📚 库版本管理（独立版本系统）
12. **独立版本号系统**：每个库（包括 STL、内置库等）都有独立的版本号，从 0.1.0 开始算起，与编译器版本号系统完全独立。
13. **库版本存档目录**：库版本存档到 `src/nova/stdlib/<library_name>/versions/x.y.z/` 目录，例如：
    - STL 库：`src/nova/stdlib/stl/versions/0.1.0/`
    - 内置库：`src/nova/stdlib/<library_name>/versions/x.y.z/`
14. **库版本存档内容**：每个库版本存档必须包含：
    - 完整的库源代码文件（.nova 文件）
    - version.py 文件（记录库版本号）
    - CHANGELOG.md 文件（记录该库版本的变更）
    - README.md 文件（库版本说明）
15. **库版本更新规则**：
    - 仅当库本身发生更改时才更新库版本号
    - 编译器版本更新不强制要求库版本更新
    - 库版本更新不影响编译器版本号
16. **库版本 Changelog**：
    - 每个库的 CHANGELOG.md 只记录该库的最新版本内容
    - 每个库有独立的 CHANGELOG_ALL.md 记录所有历史版本
    - 格式与编译器版本 Changelog 保持一致

## 📝 通信规则
17. 如果你发现命令行前缀是 nova> ，那么你就直接执行 nova 代码，除非你是要执行命令行代码（除 Nova 代码以外的代码）。
18. 与另一个程序员讲话，写在talkToTheOtherProgrammer.md里，写xx程序员（/负责xxx的程序员）：xxx
19. 你要实时看talkToTheOtherProgrammer.md，确保及时沟通，写xx程序员（/负责xxx的程序员）：xxx
20. 以后每次都要清空talkToTheOtherProgrammer.md，在写入，要不然会有bug，但是要记得备份（talkToTheOtherProgrammer.md_YYMMDD_HHMMSS_MSS.bak）
21. 如果在特定情况下，你可以不按本规则，不过可以且尽可以在用户明说了才可以。