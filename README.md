# Delicious-Study

帮助“不知道自己哪里不懂”的学习者，先通过多轮询问找到理解断点，再开展专业、直接的针对性讲解，最后用一道关联小题验证理解。

**先了解知识储备，再定位问题；不直接灌输整套知识，不用比喻替代专业解释。**

当前版本 **1.0.0** · [下载正式版](https://github.com/Delicious-Cao/Delicious-Study/releases/tag/v1.0.0) · [快速开始](docs/QUICKSTART.md) · [运行环境](docs/RUNTIME.md) · [更新记录](CHANGELOG.md)

## 它解决什么问题

用户说“帮我讲解溶液的依数性”，可能既不理解这个概念，也不知道应该补充什么背景、如何描述困惑。Delicious-Study 将寻找起点的责任交给 AI：根据用户的实际回答判断下一问，逐渐找到具体卡点。

| 环节 | 具体行为 |
| --- | --- |
| 了解目标与基础 | 围绕本次学习需要提问，不用年级或“学过”代替理解证据 |
| 多轮诊断 | 每轮聚焦一个目标，收到真实回答后再选择下一问 |
| 确认断点 | 整理已具备的基础、可能卡点与讲解顺序，允许用户纠正 |
| 针对性讲解 | 保留术语、公式与条件，用学科内实例建立理解 |
| 小题验证 | 连接本次涉及的相关知识，先作答再反馈，避免只会复述 |

提问工具可用时优先使用；工具不可用时，在普通对话中逐轮询问。一个通用版本即可使用，没有绑定某一家模型的专有教学策略。Skill 本身不会新增宿主工具。

## 安装与使用

从 [Release](https://github.com/Delicious-Cao/Delicious-Study/releases/tag/v1.0.0) 下载 `Delicious-Study-skill-v1.0.0.zip`，解压后保留完整的 `delicious-study/` 文件夹，放入宿主支持的技能目录。支持个人技能目录的 Codex 环境通常使用 `~/.codex/skills/`；宿主的具体加载方式见 [快速开始](docs/QUICKSTART.md)。

在支持按名称调用的宿主中：

```text
请使用 $delicious-study 帮我学习溶液的依数性。
先通过多轮询问了解我的基础，不要直接讲解，也不要使用比喻。
找到卡点后针对性说明，最后给我一道关联小题。
```

普通聊天界面可提供 [SKILL.md](skills/delicious-study/SKILL.md) 全文，并补充要学习的主题。普通对话不会因粘贴指令而自动获得 ask 工具。

## 示例与验证范围

- [溶液的依数性](examples/colligative-properties.md)：从浓度定义混淆与粒子数关系，过渡到沸点升高的关联小题。
- [导数与函数单调性](examples/derivatives.md)：区分“导数为零”和“区间单调性”，展示答对但理由不足时的追问。
- [示例说明](examples/README.md)：阅读方式及示例的证据边界。

示例是人工编写、逐轮审阅的流程说明，**不是真实学习者实验或模型端到端测试记录**。本版本检查 Skill 结构、元数据、文档链接、版本一致性与发布包完整性；尚未验证各客户端导入、实际 ask 交互或学习效果。详见 [运行环境与兼容性](docs/RUNTIME.md)。

## 下载包

| 附件 | 内容 |
| --- | --- |
| `Delicious-Study-skill-v1.0.0.zip` | 独立技能目录，含 `SKILL.md`、界面元数据与许可 |
| `Delicious-Study-v1.0.0.zip` | 完整仓库，含文档、示例和发布脚本 |
| `Delicious-Study-examples-v1.0.0.zip` | 两个完整对话示例与许可 |
| `SHA256SUMS.txt` | 三个 ZIP 的 SHA-256 校验值 |

## 仓库结构

```text
skills/delicious-study/
  SKILL.md
  agents/openai.yaml
docs/
  QUICKSTART.md
  RUNTIME.md
  RELEASING.md
  RELEASE-v1.0.0.md
examples/
  README.md
  colligative-properties.md
  derivatives.md
maintenance/
  check.py
  build_release.py
```

参与方式见 [贡献指南](CONTRIBUTING.md)，问题可通过仓库的 Issue 模板反馈。Skill、脚本和原创示例采用 [MIT License](LICENSE)。
