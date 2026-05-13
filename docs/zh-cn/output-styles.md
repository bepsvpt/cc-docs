> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 输出样式

> 将 Claude Code 适配用于软件工程之外的用途

输出样式改变 Claude 的响应方式，而不是 Claude 知道什么。它们修改系统提示以设置角色、语气和输出格式，同时保留核心功能，如运行脚本、读取和写入文件以及跟踪 TODO。当你在每个回合中不断重新提示相同的语音或格式时，或者当你希望 Claude 充当软件工程师以外的角色时，请使用一个。

有关你的项目、约定或代码库的说明，请改用 [CLAUDE.md](/zh-CN/memory)。

## 内置输出样式

Claude Code 的**默认**输出样式是现有的系统提示，旨在帮助你高效地完成软件工程任务。

还有三种额外的内置输出样式：

* **Proactive**：Claude 立即执行，做出合理的假设而不是暂停进行常规决策，并倾向于行动而非规划。这应用了与[自动模式](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)相同的指导，而不改变你的权限模式，因此你仍然会在工具运行前看到权限提示。

* **Explanatory**：在帮助你完成软件工程任务的同时提供教育性的"Insights"。帮助你理解实现选择和代码库模式。

* **Learning**：协作式的边学边做模式，Claude 不仅会在编码时分享"Insights"，还会要求你自己贡献小的、战略性的代码片段。Claude Code 将在你的代码中添加 `TODO(human)` 标记供你实现。

## 输出样式如何工作

输出样式直接修改 Claude Code 的系统提示。

* 自定义输出样式排除了编码说明（例如用测试验证代码），除非 `keep-coding-instructions` 为 true。
* 所有输出样式都在系统提示的末尾添加了自己的自定义说明。
* 所有输出样式都会在对话期间触发提醒，让 Claude 遵守输出样式说明。

令牌使用情况取决于样式。向系统提示添加说明会增加输入令牌，尽管 prompt caching 在会话中的第一个请求之后会降低这个成本。内置的 Explanatory 和 Learning 样式在设计上比 Default 产生更长的响应，这会增加输出令牌。对于自定义样式，输出令牌使用情况取决于你的说明告诉 Claude 生成什么。

## 更改你的输出样式

运行 `/config` 并选择**输出样式**从菜单中选择一种样式。你的选择会保存到[本地项目级别](/zh-CN/settings)的 `.claude/settings.local.json`。

要在不使用菜单的情况下设置样式，直接编辑设置文件中的 `outputStyle` 字段：

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

由于输出样式是在会话开始时在系统提示中设置的，更改将在你下次启动新会话时生效。这使系统提示在整个对话中保持稳定，以便 prompt caching 可以降低延迟和成本。

## 创建自定义输出样式

自定义输出样式是包含 frontmatter 和将添加到系统提示的文本的 Markdown 文件：

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

你可以在三个级别保存这些文件：

* 用户：`~/.claude/output-styles`
* 项目：`.claude/output-styles`
* 托管策略：[托管设置目录](/zh-CN/settings#settings-files)内的 `.claude/output-styles`

[Plugins](/zh-CN/plugins-reference) 也可以在 `output-styles/` 目录中提供输出样式。

### Frontmatter

输出样式文件支持 frontmatter 来指定元数据：

| Frontmatter                | 目的                                                                                                  | 默认值    |
| :------------------------- | :-------------------------------------------------------------------------------------------------- | :----- |
| `name`                     | 输出样式的名称，如果不是文件名                                                                                     | 从文件名继承 |
| `description`              | 输出样式的描述，在 `/config` 选择器中显示                                                                          | 无      |
| `keep-coding-instructions` | 是否保留 Claude Code 系统提示中与编码相关的部分。                                                                     | false  |
| `force-for-plugin`         | 仅限 Plugin 输出样式：在启用 plugin 时自动应用此样式，无需要求用户选择它。覆盖用户的 `outputStyle` 设置。如果多个启用的 plugin 设置了此项，则第一个加载的获胜。 | false  |

## 与相关功能的比较

### 输出样式 vs. CLAUDE.md vs. --append-system-prompt

根据 Claude 是否应该停止充当编码助手或保持其默认角色并学习更多内容来选择。输出样式用你自己的角色和声音替换 Claude Code 系统提示中的软件工程部分，因此当 Claude 应该采用不同的身份（如写作编辑或数据分析助手）时，请使用一种。CLAUDE.md 和 `--append-system-prompt` 都保持 Claude Code 的默认身份并添加到它，因此当 Claude 应该保持编码助手身份同时遵循你的项目约定或额外说明时，请使用它们。

机制也不同。输出样式直接编辑系统提示。CLAUDE.md 在系统提示之后将其内容作为用户消息添加。`--append-system-prompt` 将内容附加到系统提示的末尾，而不删除任何内容。

### 输出样式 vs. [Agents](/zh-CN/sub-agents)

使用输出样式来改变主对话在每个会话中的响应方式。当你想要一个单独作用域的辅助工具，由主对话委派给它时，使用 [subagent](/zh-CN/sub-agents)。输出样式仅影响主代理循环的系统提示。Agents 处理特定任务，可以携带自己的模型、工具和关于何时调用它们的上下文。

### 输出样式 vs. [Skills](/zh-CN/skills)

输出样式修改 Claude 的响应方式（格式、语气、结构），一旦选择就始终处于活动状态。Skills 是特定于任务的提示，你可以使用 `/skill-name` 调用或 Claude 在相关时自动加载。使用输出样式来实现一致的格式化偏好；使用 skills 来实现可重用的工作流和任务。
