# 维护与发布

## 发布前检查

1. 更新根目录 `VERSION`、Skill 的 `metadata.version`、CHANGELOG 及对应发布正文。
2. 运行 `python maintenance/check.py`，检查版本、元数据、相对链接与必需文件。
3. 如本机有 skill-creator，另运行其 `scripts/quick_validate.py skills/delicious-study`。该工具不作为学习者运行依赖。
4. 人工审阅多轮提问、等待真实回答、诊断确认、专业讲解与关联小题的流程；修改示例时复核学科条件与答案。
5. 提交所有待发布文件，在该提交上创建标注 tag，例如 `git tag -a v1.0.0 -m "Delicious-Study v1.0.0"`。

## 构建附件

需要 Python 3.9+ 与 Git；不依赖第三方 Python 包。

```text
python maintenance/build_release.py --ref v1.0.0
```

脚本从指定 Git 引用读取文件，只允许版本与 tag 名一致的语义版本号。默认输出到仓库根目录的 `dist/v1.0.0/`：

- `Delicious-Study-skill-v1.0.0.zip`：整个技能目录及许可。
- `Delicious-Study-v1.0.0.zip`：完整已提交仓库，不含 `.git/`、工作目录和 `dist/`。
- `Delicious-Study-examples-v1.0.0.zip`：两个完整示例、入口说明与许可。
- `SHA256SUMS.txt`：三个 ZIP 的校验值。

脚本会检查 ZIP 可读、成员路径安全、内容与指定提交一致、必需入口及许可存在。工作区中未提交的修改不会混入版本包。脚本会覆盖本地同目录生成物；这不授权覆盖 GitHub 已公开附件。

## GitHub Release

推送预期提交与 tag 后，以对应的 `docs/RELEASE-v版本号.md` 为正文创建正式 Release，上传全部四个附件。发布完成前可保持 Release 为草稿；核对全部附件后再公开。

发布正文应说明本次功能、下载包用途、已检查范围与未验证项。不要将人工编写示例描述为真实模型或用户实验。

发布后检查：

1. Release 是正式公开版本，tag 指向预期提交，默认分支一致。
2. 四个附件名称和大小正确，远端 ZIP 的散列与本地 `SHA256SUMS.txt` 相符。
3. 独立技能 ZIP 解压后的目录结构、许可和完整包的文档链接正确。

不移动已公开 tag，不覆盖同名公开附件隐藏内容变化；需要修正时发布新版本并解释修正范围。
