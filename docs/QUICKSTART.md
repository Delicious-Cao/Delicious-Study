# 快速开始

## 选择安装方式

### 支持 Skill 文件夹的宿主

1. 在 [v1.0.0 Release](https://github.com/Delicious-Cao/Delicious-Study/releases/tag/v1.0.0) 下载 `Delicious-Study-skill-v1.0.0.zip`。
2. 解压后得到 `delicious-study/`，其中直接包含 `SKILL.md` 与 `agents/openai.yaml`。不要只复制界面元数据文件。
3. 将整个目录放入宿主支持的技能目录。例如，使用 `~/.codex/skills/` 的环境中，最终入口是 `~/.codex/skills/delicious-study/SKILL.md`。
4. 按宿主方式刷新技能或重启会话。支持显式名称调用时输入 `$delicious-study`，并说明要学习的主题。

也可下载完整仓库包，将其中的 `skills/delicious-study/` 复制到同一位置。`agents/openai.yaml` 是可选的宿主界面元数据；Skill 的实际指令在 `SKILL.md`，并不依赖该 YAML 才能阅读。

### 普通聊天界面

打开 [SKILL.md](../skills/delicious-study/SKILL.md)，上传该文件或粘贴其全文，再写明学习主题。文件上传、技能识别和提问工具由客户端决定；粘贴指令不等于已经安装插件，也不会新增工具。

## 开始一轮学习

```text
请使用 Delicious-Study 帮我学习“溶液的依数性”。
我暂时说不清哪里不懂，请先多轮询问我的知识储备，
找到断点后再针对性讲解，不用比喻，最后用一道关联小题检查。
```

有材料时可以补充课本定义、公式、题目或自己的解题步骤。无需事先写出专业问题，也无需把个人背景全部交代清楚。

正常流程是：回答一小轮具体问题 → 必要时继续调查 → 确认 AI 对卡点的判断 → 接受针对性讲解 → 独立回答小题并说明理由。用户可以纠正诊断、要求加快节奏、只做诊断或跳过练习。

## 提问工具与等待

宿主提供可用的 ask／用户输入工具时，Skill 优先使用它。接口受限或不存在时，会在普通对话中逐轮提问。使用异步工具时，需要用户实际提交回复后才能继续依赖该回复的步骤；预选项与等待时长都不是回答。

如果 AI 一开始就大段讲解，可以提醒：“请先按 Skill 诊断我的基础，等我回答这一轮后再继续。”如果小题同时显示了答案，可以要求它改出一道新的等价小题，先不要给答案。

## 校验下载文件

将 ZIP 与 Release 中的 `SHA256SUMS.txt` 放在一起，比较文件名对应的散列值。

PowerShell：

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath '.\Delicious-Study-skill-v1.0.0.zip'
```

macOS／Linux 可使用系统的 SHA-256 工具。仓库打包脚本也会检查 ZIP 成员完整性并生成校验文件，见 [发布说明](RELEASING.md)。

## 示例与限制

阅读 [完整对话示例](../examples/README.md) 了解期望行为。示例是人工编写的说明，不保证每个模型和客户端都能同样执行；目前实际检查范围见 [运行环境](RUNTIME.md)。
