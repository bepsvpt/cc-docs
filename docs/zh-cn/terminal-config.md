> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 为 Claude Code 配置您的终端

> 修复 Shift+Enter 以实现换行、在 Claude 完成时获得终端铃声、配置 tmux、匹配颜色主题，以及在 Claude Code CLI 中启用 Vim 模式。

Claude Code 在任何终端中都可以无需配置而工作。此页面适用于当某些特定功能的行为不符合您的预期时。在下面找到您的症状。如果一切都已经感觉正确，您不需要此页面。

* [Shift+Enter 提交而不是插入换行](#enter-multiline-prompts)
* [Option 键快捷键在 macOS 上无效](#enable-option-key-shortcuts-on-macos)
* [Claude 完成时没有声音或警报](#get-a-terminal-bell-or-notification)
* [您在 tmux 内运行 Claude Code](#configure-tmux)
* [显示闪烁或滚动条跳跃](#switch-to-fullscreen-rendering)
* [您想在提示符中使用 Vim 快捷键](#edit-prompts-with-vim-keybindings)

此页面是关于让您的终端向 Claude Code 发送正确的信号。要更改 Claude Code 本身响应的快捷键，请改为参阅[快捷键](/zh-CN/keybindings)。

## 输入多行提示符

按 Enter 提交您的消息。要添加换行符而不提交，请按 Ctrl+J，或输入 `\` 然后按 Enter。两者都在每个终端中工作，无需设置。

在大多数终端中，您也可以按 Shift+Enter，但支持因终端模拟器而异：

| 终端                                                                        | Shift+Enter 换行               |
| :------------------------------------------------------------------------ | :--------------------------- |
| Ghostty、Kitty、iTerm2、WezTerm、Warp、Apple Terminal                          | 无需设置即可工作                     |
| VS Code、Cursor、Windsurf、Alacritty、Zed                                     | 运行一次 `/terminal-setup`       |
| Windows Terminal、gnome-terminal、JetBrains IDE（如 PyCharm 和 Android Studio） | 不可用；使用 Ctrl+J 或 `\` 然后 Enter |

对于 VS Code、Cursor、Windsurf、Alacritty 和 Zed，`/terminal-setup` 将 Shift+Enter 和其他快捷键写入终端的配置文件。如果它报告冲突，例如 `Found existing VSCode terminal Shift+Enter key binding`，请从终端自己的快捷键文件（例如 VS Code 的 `keybindings.json`）中删除该条目，然后再次运行该命令。在主机终端中直接运行 `/terminal-setup` 而不是在 tmux 或 screen 内运行，因为它需要写入主机终端的配置。

如果您在 tmux 内运行，即使外部终端支持，Shift+Enter 也需要下面的 [tmux 配置](#configure-tmux)。

要将换行绑定到不同的快捷键，或交换行为使 Enter 插入换行而 Shift+Enter 提交，请在您的[快捷键文件](/zh-CN/keybindings)中映射 `chat:newline` 和 `chat:submit` 操作。

## 在 macOS 上启用 Option 快捷键

某些 Claude Code 快捷键使用 Option 键，例如 Option+Enter 换行或 Option+P 切换模型。在 macOS 上，大多数终端默认不将 Option 作为修饰符发送，因此这些快捷键在您启用它之前无效。此终端设置通常标记为"使用 Option 作为 Meta 键"；Meta 是现在标记为 Option 或 Alt 的快捷键的历史 Unix 名称。

<Tabs>
  <Tab title="Apple Terminal">
    打开设置 → 配置文件 → 键盘并勾选"使用 Option 作为 Meta 键"。

    如果您接受了 Claude Code 的首次运行提示，该提示提供了"Option+Enter 换行和视觉铃声"，这已经完成。该提示为您运行 `/terminal-setup`，它在您的 Apple Terminal 配置文件中启用 Option 作为 Meta 并将音频铃声切换为视觉屏幕闪烁。
  </Tab>

  <Tab title="iTerm2">
    打开设置 → 配置文件 → 快捷键 → 常规并将左 Option 快捷键和右 Option 快捷键设置为"Esc+"。
  </Tab>

  <Tab title="VS Code">
    将 `"terminal.integrated.macOptionIsMeta": true` 添加到您的 VS Code 设置。
  </Tab>
</Tabs>

对于 Ghostty、Kitty 和其他终端，请在终端的配置文件中查找 Option-as-Alt 或 Option-as-Meta 设置。

## 获取终端铃声或通知

当 Claude 完成任务或暂停以获得权限提示时，它会触发通知事件。将其显示为终端铃声或桌面通知可让您在长任务运行时切换到其他工作。

Claude Code 仅在 Ghostty、Kitty 和 iTerm2 中发送桌面通知；所有其他终端需要[通知钩子](#play-a-sound-with-a-notification-hook)。通知也通过 SSH 到达您的本地机器，因此远程会话仍然可以提醒您。Ghostty 和 Kitty 无需进一步设置即可将其转发到您的 OS 通知中心。iTerm2 要求您启用转发：

<Steps>
  <Step title="打开 iTerm2 通知设置">
    转到设置 → 配置文件 → 终端。
  </Step>

  <Step title="启用警报">
    勾选"通知中心警报"，然后单击"过滤警报"并启用"发送转义序列生成的警报"。
  </Step>
</Steps>

如果通知仍未出现，请确认您的终端应用程序在您的 OS 设置中具有通知权限，如果您在 tmux 内运行，请[启用直通](#configure-tmux)。

### 使用通知钩子播放声音

在任何终端中，您可以配置[通知钩子](/zh-CN/hooks-guide#get-notified-when-claude-needs-input)以在 Claude 需要您的注意时播放声音或运行自定义命令。钩子与桌面通知一起运行，而不是替代它。Warp 或 Apple Terminal 等终端仅依赖钩子，因为 Claude Code 不向它们发送桌面通知。

下面的示例在 macOS 上播放系统声音。链接的指南包含 macOS、Linux 和 Windows 的桌面通知命令。

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## 配置 tmux

当 Claude Code 在 tmux 内运行时，默认情况下两件事会中断：Shift+Enter 提交而不是插入换行，桌面通知和[进度条](/zh-CN/settings#global-config-settings)永远无法到达外部终端。将这些行添加到 `~/.tmux.conf`，然后运行 `tmux source-file ~/.tmux.conf` 将它们应用到运行的服务器：

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

`allow-passthrough` 行让通知和进度更新到达 iTerm2、Ghostty 或 Kitty，而不是被 tmux 吞没。`extended-keys` 行让 tmux 区分 Shift+Enter 和纯 Enter，以便换行快捷键工作。

## 匹配颜色主题

使用 `/theme` 命令或 `/config` 中的主题选择器来选择与您的终端匹配的 Claude Code 主题。选择自动选项会检测您的终端的浅色或深色背景，因此主题会在您的终端执行时跟随 OS 外观更改。可用的主题是内置的；没有自定义主题文件。Claude Code 不控制终端自己的颜色方案，该方案由终端应用程序设置。

要自定义界面底部显示的内容，请配置[自定义状态行](/zh-CN/statusline)，显示当前模型、工作目录、git 分支或其他上下文。

## 切换到全屏渲染

如果显示闪烁或在 Claude 工作时滚动位置跳跃，请切换到[全屏渲染模式](/zh-CN/fullscreen)。它绘制到终端为全屏应用程序保留的单独屏幕，而不是附加到您的正常滚动条，这保持内存使用平稳并为滚动和选择添加鼠标支持。在此模式下，您使用鼠标或 PageUp 在 Claude Code 内滚动，而不是使用您的终端的本机滚动条；请参阅[全屏页面](/zh-CN/fullscreen#search-and-review-the-conversation)了解如何搜索和复制。

运行 `/tui fullscreen` 在当前会话中切换，您的对话保持不变。要使其成为默认值，请在启动 Claude Code 之前设置 `CLAUDE_CODE_NO_FLICKER` 环境变量：

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## 粘贴大型内容

当您将超过 10,000 个字符粘贴到提示符中时，Claude Code 将输入折叠为 `[Pasted text]` 占位符，以便输入框保持可用。当您提交时，完整内容仍会发送给 Claude。

VS Code 集成终端可能会在非常大的粘贴中丢弃字符，然后才能到达 Claude Code，因此在那里更喜欢基于文件的工作流。对于非常大的输入，例如整个文件或长日志，请将内容写入文件并要求 Claude 读取它，而不是粘贴。这保持对话记录可读，并让 Claude 在后续轮次中按路径引用文件。

## 使用 Vim 快捷键编辑提示符

Claude Code 包括提示符输入的 Vim 风格编辑模式。通过 `/config` → 编辑器模式启用它，或通过在 `~/.claude.json` 中将 [`editorMode`](/zh-CN/settings#global-config-settings) 全局配置键设置为 `"vim"` 来启用。将编辑器模式设置回 `normal` 以关闭它。

Vim 模式支持 NORMAL 模式动作和运算符的子集，例如 `hjkl` 导航和 `d`/`c`/`y` 与文本对象。请参阅 [Vim 编辑器模式参考](/zh-CN/interactive-mode#vim-editor-mode)了解完整的快捷键表。Vim 动作不可通过快捷键文件重新映射。

在 INSERT 模式下按 Enter 仍会提交您的提示符，与标准 Vim 不同。在 NORMAL 模式下使用 `o` 或 `O`，或 Ctrl+J，来插入换行。

## 相关资源

* [交互模式](/zh-CN/interactive-mode)：完整的键盘快捷键参考和 Vim 快捷键表
* [快捷键](/zh-CN/keybindings)：重新映射任何 Claude Code 快捷键，包括 Enter 和 Shift+Enter
* [全屏渲染](/zh-CN/fullscreen)：全屏模式下滚动、搜索和复制的详细信息
* [钩子指南](/zh-CN/hooks-guide)：Linux 和 Windows 的更多通知钩子示例
* [故障排除](/zh-CN/troubleshooting)：修复终端配置之外的问题
