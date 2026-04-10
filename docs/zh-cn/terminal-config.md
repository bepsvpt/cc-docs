> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# 优化您的终端设置

> Claude Code 在终端配置正确时效果最佳。请按照这些指南来优化您的体验。

### 主题和外观

Claude 无法控制您的终端主题。这由您的终端应用程序处理。您可以随时通过 `/config` 命令将 Claude Code 的主题与您的终端相匹配。

为了进一步自定义 Claude Code 界面本身，您可以配置一个[自定义状态行](/zh-CN/statusline)来显示上下文信息，如当前模型、工作目录或 git 分支在您的终端底部。

### 换行符

您有多个选项可以在 Claude Code 中输入换行符：

* **快速转义**：输入 `\` 后按 Enter 键创建新行
* **Shift+Enter**：在 iTerm2、WezTerm、Ghostty 和 Kitty 中开箱即用
* **键盘快捷键**：在其他终端中设置快捷键以插入新行

**为其他终端设置 Shift+Enter**

在 Claude Code 中运行 `/terminal-setup` 以自动为 VS Code、Alacritty、Zed 和 Warp 配置 Shift+Enter。

<Note>
  `/terminal-setup` 命令仅在需要手动配置的终端中可见。如果您使用的是 iTerm2、WezTerm、Ghostty 或 Kitty，您将看不到此命令，因为 Shift+Enter 已经原生工作。
</Note>

**设置 Option+Enter（VS Code、iTerm2 或 macOS Terminal.app）**

**对于 Mac Terminal.app：**

1. 打开设置 → 配置文件 → 键盘
2. 勾选"使用 Option 作为 Meta 键"

**对于 iTerm2：**

1. 打开设置 → 配置文件 → 键
2. 在常规下，将左/右 Option 键设置为"Esc+"

**对于 VS Code 终端：**

在 VS Code 设置中设置 `"terminal.integrated.macOptionIsMeta": true`。

### 通知设置

当 Claude 完成工作并等待您的输入时，它会触发一个通知事件。您可以通过您的终端将此事件显示为桌面通知，或使用[通知钩子](/zh-CN/hooks#notification)运行自定义逻辑。

#### 终端通知

Kitty 和 Ghostty 支持桌面通知，无需额外配置。iTerm 2 需要设置：

1. 打开 iTerm 2 设置 → 配置文件 → 终端
2. 启用"通知中心警报"
3. 点击"过滤警报"并勾选"发送转义序列生成的警报"

如果通知未出现，请验证您的终端应用程序在操作系统设置中具有通知权限。

在 tmux 中运行 Claude Code 时，通知和[终端进度条](/zh-CN/settings#global-config-settings)仅在您在 tmux 配置中启用直通时才能到达外部终端，例如 iTerm2、Kitty 或 Ghostty：

```
set -g allow-passthrough on
```

没有此设置，tmux 会拦截转义序列，它们不会到达终端应用程序。

其他终端，包括默认的 macOS 终端，不支持原生通知。请改用[通知钩子](/zh-CN/hooks#notification)。

#### 通知钩子

要在通知触发时添加自定义行为，例如播放声音或发送消息，请配置一个[通知钩子](/zh-CN/hooks#notification)。钩子与终端通知一起运行，而不是作为替代品。

### 减少闪烁和内存使用

如果您在长时间会话中看到闪烁，或者当 Claude 工作时您的终端滚动位置跳到顶部，请尝试[全屏渲染](/zh-CN/fullscreen)。它使用一个替代渲染路径，保持内存平稳并添加鼠标支持。使用 `CLAUDE_CODE_NO_FLICKER=1` 启用它。

### 处理大型输入

处理大量代码或长指令时：

* **避免直接粘贴**：Claude Code 可能难以处理非常长的粘贴内容
* **使用基于文件的工作流**：将内容写入文件并要求 Claude 读取它
* **注意 VS Code 的限制**：VS Code 终端特别容易截断长粘贴

### Vim 模式

Claude Code 支持可以通过 `/vim` 启用或通过 `/config` 配置的 Vim 快捷键子集。要直接在配置文件中设置模式，请在 `~/.claude.json` 中将 [`editorMode`](/zh-CN/settings#global-config-settings) 全局配置键设置为 `"vim"`。

支持的子集包括：

* 模式切换：`Esc`（到 NORMAL）、`i`/`I`、`a`/`A`、`o`/`O`（到 INSERT）
* 导航：`h`/`j`/`k`/`l`、`w`/`e`/`b`、`0`/`$`/`^`、`gg`/`G`、`f`/`F`/`t`/`T` 带 `;`/`,` 重复
* 编辑：`x`、`dw`/`de`/`db`/`dd`/`D`、`cw`/`ce`/`cb`/`cc`/`C`、`.`（重复）
* 复制/粘贴：`yy`/`Y`、`yw`/`ye`/`yb`、`p`/`P`
* 文本对象：`iw`/`aw`、`iW`/`aW`、`i"`/`a"`、`i'`/`a'`、`i(`/`a(`、`i[`/`a[`、`i{`/`a{`
* 缩进：`>>`/`<<`
* 行操作：`J`（连接行）

请参阅[交互模式](/zh-CN/interactive-mode#vim-editor-mode)获取完整参考。
