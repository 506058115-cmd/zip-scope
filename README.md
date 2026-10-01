# zip-scope

解压前离线查看 ZIP 条目名称、声明体积和可能越界的路径。工具只读取压缩包目录，不提取或改写文件。

## 使用

需要 Python 3.8+，不安装依赖。

~~~sh
python zip_scope.py ./download.zip
python zip_scope.py ./download.zip --list
~~~

默认只显示摘要和包含根路径或盘符、.. 路径段或符号链接等需要留意的条目；--list 会列出所有名称和声明大小。名称以转义形式输出，避免压缩包里的控制字符直接影响终端显示。

这些检查只能提示部分风险，不能证明压缩包安全。工具不会解压文件，也不会判断文件内容是否可信。

## 许可

MIT，见 [LICENSE](LICENSE)。
## Linux x86_64 下载

- [单文件版](https://github.com/506058115-cmd/zip-scope/releases/download/v1.0.0/zip-scope-linux-x86_64-onefile.tar.gz)
- [目录版](https://github.com/506058115-cmd/zip-scope/releases/download/v1.0.0/zip-scope-linux-x86_64-onedir.tar.gz)
- [v1.0.0 Release 页面](https://github.com/506058115-cmd/zip-scope/releases/tag/v1.0.0)

压缩包附带构建信息和依赖许可证；Release 另附 SHA-256 校验文件。产物在 WSL Ubuntu 24.04（Python 3.12.3、PyInstaller 6.22.2）中构建，目标为 GNU/Linux x86_64。较旧的发行版可能需要兼容的 glibc。
