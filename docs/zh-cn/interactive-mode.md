> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 交互模式

> Claude Code 会话中键盘快捷键、输入模式和交互功能的完整参考。

## 快捷键

<Note>
  快捷键可能因平台和终端而异。按 `?` 查看您的环境中可用的快捷键。

  **macOS 用户**：Option/Alt 键快捷键（`Alt+B`、`Alt+F`、`Alt+Y`、`Alt+M`、`Alt+P`）需要在终端中将 Option 配置为 Meta：

  * **iTerm2**：设置 → 配置文件 → 键 → 将左/右 Option 键设置为"Esc+"
  * **Terminal.app**：设置 → 配置文件 → 键盘 → 勾选"使用 Option 作为 Meta 键"
  * **VS Code**：设置 → 配置文件 → 键 → 将左/右 Option 键设置为"Esc+"

  有关详细信息，请参阅[终端配置](/zh-CN/terminal-config)。
</Note>

### 常规控制

| 快捷键                                          | 描述                    | 上下文                                        |
| :------------------------------------------- | :-------------------- | :----------------------------------------- |
| `Ctrl+C`                                     | 取消当前输入或生成             | 标准中断                                       |
| `Ctrl+F`                                     | 终止所有后台代理。在 3 秒内按两次以确认 | 后台代理控制                                     |
| `Ctrl+D`                                     | 退出 Claude Code 会话     | EOF 信号                                     |
| `Ctrl+G`                                     | 在默认文本编辑器中打开           | 在默认文本编辑器中编辑您的提示或自定义响应                      |
| `Ctrl+L`                                     | 清除终端屏幕                | 保留对话历史                                     |
| `Ctrl+O`                                     | 切换详细输出                | 显示详细的工具使用和执行情况                             |
| `Ctrl+R`                                     | 反向搜索命令历史              | 交互式搜索以前的命令                                 |
| `Ctrl+V` 或 `Cmd+V`（iTerm2）或 `Alt+V`（Windows） | 从剪贴板粘贴图像              | 粘贴图像或图像文件的路径                               |
| `Ctrl+B`                                     | 后台运行任务                | 后台运行 bash 命令和代理。Tmux 用户按两次                 |
| `Ctrl+T`                                     | 切换任务列表                | 在终端状态区域中显示或隐藏[任务列表](#task-list)            |
| `Left/Right arrows`                          | 在对话框选项卡之间循环           | 在权限对话框和菜单中的选项卡之间导航                         |
| `Up/Down arrows`                             | 导航命令历史                | 回忆以前的输入                                    |
| `Esc` + `Esc`                                | 回退或总结                 | 将代码和/或对话恢复到上一个点，或从选定的消息进行总结                |
| `Shift+Tab` 或 `Alt+M`（某些配置）                  | 切换权限模式                | 在自动接受模式、Plan Mode 和正常模式之间切换。               |
| `Option+P`（macOS）或 `Alt+P`（Windows/Linux）    | 切换模型                  | 在不清除提示的情况下切换模型                             |
| `Option+T`（macOS）或 `Alt+T`（Windows/Linux）    | 切换扩展思考                | 启用或禁用扩展思考模式。首先运行 `/terminal-setup` 以启用此快捷键 |

### 文本编辑

| 快捷键                    | 描述          | 上下文                                                                |
| :--------------------- | :---------- | :----------------------------------------------------------------- |
| `Ctrl+K`               | 删除到行尾       | 存储已删除的文本以供粘贴                                                       |
| `Ctrl+U`               | 删除整行        | 存储已删除的文本以供粘贴                                                       |
| `Ctrl+Y`               | 粘贴已删除的文本    | 粘贴用 `Ctrl+K` 或 `Ctrl+U` 删除的文本                                      |
| `Alt+Y`（在 `Ctrl+Y` 之后） | 循环粘贴历史      | 粘贴后，循环浏览以前删除的文本。在 macOS 上需要[将 Option 作为 Meta](#keyboard-shortcuts) |
| `Alt+B`                | 将光标向后移动一个单词 | 单词导航。在 macOS 上需要[将 Option 作为 Meta](#keyboard-shortcuts)            |
| `Alt+F`                | 将光标向前移动一个单词 | 单词导航。在 macOS 上需要[将 Option 作为 Meta](#keyboard-shortcuts)            |

### 主题和显示

| 快捷键      | 描述           | 上下文                                           |
| :------- | :----------- | :-------------------------------------------- |
| `Ctrl+T` | 切换代码块的语法突出显示 | 仅在 `/theme` 选择器菜单内有效。控制 Claude 响应中的代码是否使用语法着色 |

<Note>
  语法突出显示仅在 Claude Code 的原生构建中可用。
</Note>

### 多行输入

| 方法          | 快捷键            | 上下文                                  |
| :---------- | :------------- | :----------------------------------- |
| 快速转义        | `\` + `Enter`  | 在所有终端中有效                             |
| macOS 默认    | `Option+Enter` | macOS 上的默认值                          |
| Shift+Enter | `Shift+Enter`  | 在 iTerm2、WezTerm、Ghostty、Kitty 中开箱即用 |
| 控制序列        | `Ctrl+J`       | 多行的换行符                               |
| 粘贴模式        | 直接粘贴           | 对于代码块、日志                             |

<Tip>
  Shift+Enter 在 iTerm2、WezTerm、Ghostty 和 Kitty 中无需配置即可工作。对于其他终端（VS Code、Alacritty、Zed、Warp），运行 `/terminal-setup` 以安装绑定。
</Tip>

### 快速命令

| 快捷键     | 描述        | 注释                                                     |
| :------ | :-------- | :----------------------------------------------------- |
| `/` 在开始 | 命令或 skill | 请参阅[内置命令](#built-in-commands)和 [skills](/zh-CN/skills) |
| `!` 在开始 | Bash 模式   | 直接运行命令并将执行输出添加到会话                                      |
| `@`     | 文件路径提及    | 触发文件路径自动完成                                             |

## 内置命令

在 Claude Code 中输入 `/` 以查看所有可用命令，或输入 `/` 后跟任何字母以进行筛选。并非所有命令对每个用户都可见。有些取决于您的平台、计划或环境。例如，`/desktop` 仅在 macOS 和 Windows 上显示，`/upgrade` 和 `/privacy-settings` 仅在 Pro 和 Max 计划上可用，`/terminal-setup` 在您的终端本身支持其快捷键时隐藏。

Claude Code 还附带[捆绑的 skills](/zh-CN/skills#bundled-skills)，如 `/simplify`、`/batch` 和 `/debug`，当您输入 `/` 时会与内置命令一起显示。要创建您自己的命令，请参阅 [skills](/zh-CN/skills)。

在下表中，`<arg>` 表示必需的参数，`[arg]` 表示可选参数。

| 命令                        | 目的                                                                                                                                                                                 |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | 将新的工作目录添加到当前会话                                                                                                                                                                     |
| `/agents`                 | 管理 [agent](/zh-CN/sub-agents) 配置                                                                                                                                                   |
| `/btw <question>`         | 提出快速[侧问题](#side-questions-with-%2Fbtw)，无需添加到对话                                                                                                                                     |
| `/chrome`                 | 配置[Chrome 中的 Claude](/zh-CN/chrome) 设置                                                                                                                                             |
| `/clear`                  | 清除对话历史并释放上下文。别名：`/reset`、`/new`                                                                                                                                                    |
| `/compact [instructions]` | 压缩对话，可选的焦点说明                                                                                                                                                                       |
| `/config`                 | 打开[设置](/zh-CN/settings)界面以调整主题、模型、[输出样式](/zh-CN/output-styles)和其他首选项。别名：`/settings`                                                                                                |
| `/context`                | 将当前上下文使用情况可视化为彩色网格                                                                                                                                                                 |
| `/copy`                   | 将最后一个助手响应复制到剪贴板。当存在代码块时，显示交互式选择器以选择单个块或完整响应                                                                                                                                        |
| `/cost`                   | 显示令牌使用统计信息。有关特定于订阅的详细信息，请参阅[成本跟踪指南](/zh-CN/costs#using-the-cost-command)                                                                                                           |
| `/desktop`                | 在 Claude Code 桌面应用中继续当前会话。仅限 macOS 和 Windows。别名：`/app`                                                                                                                             |
| `/diff`                   | 打开交互式差异查看器，显示未提交的更改和每个回合的差异。使用左/右箭头在当前 git 差异和单个 Claude 回合之间切换，使用上/下浏览文件                                                                                                           |
| `/doctor`                 | 诊断并验证您的 Claude Code 安装和设置                                                                                                                                                          |
| `/exit`                   | 退出 CLI。别名：`/quit`                                                                                                                                                                  |
| `/export [filename]`      | 将当前对话导出为纯文本。使用文件名时，直接写入该文件。不使用时，打开对话框以复制到剪贴板或保存到文件                                                                                                                                 |
| `/extra-usage`            | 配置额外使用以在达到速率限制时继续工作                                                                                                                                                                |
| `/fast [on\|off]`         | 切换[快速模式](/zh-CN/fast-mode)开启或关闭                                                                                                                                                    |
| `/feedback [report]`      | 提交关于 Claude Code 的反馈。别名：`/bug`                                                                                                                                                     |
| `/fork [name]`            | 在此点创建当前对话的分支                                                                                                                                                                       |
| `/help`                   | 显示帮助和可用命令                                                                                                                                                                          |
| `/hooks`                  | 管理工具事件的 [hook](/zh-CN/hooks) 配置                                                                                                                                                    |
| `/ide`                    | 管理 IDE 集成并显示状态                                                                                                                                                                     |
| `/init`                   | 使用 `CLAUDE.md` 指南初始化项目                                                                                                                                                             |
| `/insights`               | 生成报告，分析您的 Claude Code 会话，包括项目区域、交互模式和摩擦点                                                                                                                                           |
| `/install-github-app`     | 为存储库设置 [Claude GitHub Actions](/zh-CN/github-actions) 应用。引导您选择存储库并配置集成                                                                                                             |
| `/install-slack-app`      | 安装 Claude Slack 应用。打开浏览器以完成 OAuth 流程                                                                                                                                               |
| `/keybindings`            | 打开或创建您的快捷键配置文件                                                                                                                                                                     |
| `/login`                  | 登录到您的 Anthropic 账户                                                                                                                                                                 |
| `/logout`                 | 从您的 Anthropic 账户登出                                                                                                                                                                 |
| `/mcp`                    | 管理 MCP server 连接和 OAuth 身份验证                                                                                                                                                       |
| `/memory`                 | 编辑 `CLAUDE.md` 内存文件，启用或禁用[自动内存](/zh-CN/memory#auto-memory)，并查看自动内存条目                                                                                                               |
| `/mobile`                 | 显示二维码以下载 Claude 移动应用。别名：`/ios`、`/android`                                                                                                                                          |
| `/model [model]`          | 选择或更改 AI 模型。对于支持的模型，使用左/右箭头[调整努力级别](/zh-CN/model-config#adjust-effort-level)。更改立即生效，无需等待当前响应完成                                                                                     |
| `/passes`                 | 与朋友分享一周免费的 Claude Code。仅在您的账户符合条件时可见                                                                                                                                               |
| `/permissions`            | 查看或更新[权限](/zh-CN/permissions#manage-permissions)。别名：`/allowed-tools`                                                                                                               |
| `/plan`                   | 直接从提示进入 plan mode                                                                                                                                                                  |
| `/plugin`                 | 管理 Claude Code [plugins](/zh-CN/plugins)                                                                                                                                           |
| `/pr-comments [PR]`       | 获取并显示来自 GitHub pull request 的评论。自动检测当前分支的 PR，或传递 PR URL 或编号。需要 `gh` CLI                                                                                                            |
| `/privacy-settings`       | 查看和更新您的隐私设置。仅对 Pro 和 Max 计划订阅者可用                                                                                                                                                   |
| `/release-notes`          | 查看完整的更改日志，最新版本最接近您的提示                                                                                                                                                              |
| `/reload-plugins`         | 重新加载所有活跃 [plugins](/zh-CN/plugins) 以应用待处理的更改，无需重启。报告已加载的内容并注明需要重启的更改                                                                                                               |
| `/remote-control`         | 使此会话可从 claude.ai 进行[远程控制](/zh-CN/remote-control)。别名：`/rc`                                                                                                                          |
| `/remote-env`             | 为[teleport 会话](/zh-CN/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)配置默认远程环境                                                                                      |
| `/rename [name]`          | 重命名当前会话。不使用名称时，从对话历史自动生成                                                                                                                                                           |
| `/resume [session]`       | 按 ID 或名称恢复对话，或打开会话选择器。别名：`/continue`                                                                                                                                               |
| `/review`                 | 已弃用。改为安装 [`code-review` plugin](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md)：`claude plugin install code-review@claude-code-marketplace` |
| `/rewind`                 | 将对话和/或代码回退到上一个点，或从选定的消息进行总结。请参阅[checkpointing](/zh-CN/checkpointing)。别名：`/checkpoint`                                                                                              |
| `/sandbox`                | 切换[sandbox 模式](/zh-CN/sandboxing)。仅在支持的平台上可用                                                                                                                                       |
| `/security-review`        | 分析当前分支上的待处理更改以查找安全漏洞。审查 git 差异并识别风险，如注入、身份验证问题和数据泄露                                                                                                                                |
| `/skills`                 | 列出可用的 [skills](/zh-CN/skills)                                                                                                                                                      |
| `/stats`                  | 可视化每日使用情况、会话历史、连胜和模型偏好                                                                                                                                                             |
| `/status`                 | 打开设置界面（状态选项卡），显示版本、模型、账户和连接性                                                                                                                                                       |
| `/statusline`             | 配置 Claude Code 的[状态行](/zh-CN/statusline)。描述您想要的内容，或不带参数运行以从您的 shell 提示自动配置                                                                                                         |
| `/stickers`               | 订购 Claude Code 贴纸                                                                                                                                                                  |
| `/tasks`                  | 列出和管理后台任务                                                                                                                                                                          |
| `/terminal-setup`         | 为 Shift+Enter 和其他快捷键配置终端快捷键。仅在需要它的终端中可见，如 VS Code、Alacritty 或 Warp                                                                                                                 |
| `/theme`                  | 更改颜色主题。包括浅色和深色变体、色盲无障碍（daltonized）主题和使用您终端的调色板的 ANSI 主题                                                                                                                            |
| `/upgrade`                | 打开升级页面以切换到更高的计划层级                                                                                                                                                                  |
| `/usage`                  | 显示计划使用限制和速率限制状态                                                                                                                                                                    |
| `/vim`                    | 在 Vim 和正常编辑模式之间切换                                                                                                                                                                  |

### MCP prompts

MCP servers 可以公开显示为命令的 prompts。这些使用格式 `/mcp__<server>__<prompt>`，并从连接的 servers 动态发现。有关详细信息，请参阅 [MCP prompts](/zh-CN/mcp#use-mcp-prompts-as-commands)。

## Vim 编辑器模式

使用 `/vim` 命令启用 vim 风格编辑，或通过 `/config` 永久配置。

### 模式切换

| 命令    | 操作           | 来自模式   |
| :---- | :----------- | :----- |
| `Esc` | 进入 NORMAL 模式 | INSERT |
| `i`   | 在光标前插入       | NORMAL |
| `I`   | 在行首插入        | NORMAL |
| `a`   | 在光标后插入       | NORMAL |
| `A`   | 在行尾插入        | NORMAL |
| `o`   | 在下方打开行       | NORMAL |
| `O`   | 在上方打开行       | NORMAL |

### 导航（NORMAL 模式）

| 命令              | 操作                  |
| :-------------- | :------------------ |
| `h`/`j`/`k`/`l` | 向左/下/上/右移动          |
| `w`             | 下一个单词               |
| `e`             | 单词末尾                |
| `b`             | 上一个单词               |
| `0`             | 行首                  |
| `$`             | 行尾                  |
| `^`             | 第一个非空白字符            |
| `gg`            | 输入开始                |
| `G`             | 输入结束                |
| `f{char}`       | 跳转到下一个字符出现处         |
| `F{char}`       | 跳转到上一个字符出现处         |
| `t{char}`       | 跳转到下一个字符出现处之前       |
| `T{char}`       | 跳转到上一个字符出现处之后       |
| `;`             | 重复最后一个 f/F/t/T 动作   |
| `,`             | 反向重复最后一个 f/F/t/T 动作 |

<Note>
  在 vim 正常模式中，如果光标在输入的开始或结束处且无法进一步移动，箭头键将导航命令历史。
</Note>

### 编辑（NORMAL 模式）

| 命令             | 操作          |
| :------------- | :---------- |
| `x`            | 删除字符        |
| `dd`           | 删除行         |
| `D`            | 删除到行尾       |
| `dw`/`de`/`db` | 删除单词/到末尾/向后 |
| `cc`           | 更改行         |
| `C`            | 更改到行尾       |
| `cw`/`ce`/`cb` | 更改单词/到末尾/向后 |
| `yy`/`Y`       | 复制行         |
| `yw`/`ye`/`yb` | 复制单词/到末尾/向后 |
| `p`            | 在光标后粘贴      |
| `P`            | 在光标前粘贴      |
| `>>`           | 缩进行         |
| `<<`           | 取消缩进行       |
| `J`            | 连接行         |
| `.`            | 重复最后一个更改    |

### 文本对象（NORMAL 模式）

文本对象与 `d`、`c` 和 `y` 等运算符一起工作：

| 命令        | 操作               |
| :-------- | :--------------- |
| `iw`/`aw` | 内部/周围单词          |
| `iW`/`aW` | 内部/周围 WORD（空白分隔） |
| `i"`/`a"` | 内部/周围双引号         |
| `i'`/`a'` | 内部/周围单引号         |
| `i(`/`a(` | 内部/周围括号          |
| `i[`/`a[` | 内部/周围方括号         |
| `i{`/`a{` | 内部/周围大括号         |

## 命令历史

Claude Code 为当前会话维护命令历史：

* 输入历史按工作目录存储
* 当您运行 `/clear` 以启动新会话时，输入历史会重置。上一个会话的对话会被保留，可以恢复。
* 使用上/下箭头导航（请参阅上面的快捷键）
* **注意**：历史扩展（`!`）默认禁用

### 使用 Ctrl+R 反向搜索

按 `Ctrl+R` 以交互方式搜索您的命令历史：

1. **开始搜索**：按 `Ctrl+R` 激活反向历史搜索
2. **输入查询**：输入文本以在以前的命令中搜索。搜索词在匹配结果中突出显示
3. **导航匹配**：再次按 `Ctrl+R` 以循环浏览较旧的匹配
4. **接受匹配**：
   * 按 `Tab` 或 `Esc` 接受当前匹配并继续编辑
   * 按 `Enter` 接受并立即执行命令
5. **取消搜索**：
   * 按 `Ctrl+C` 取消并恢复您的原始输入
   * 在空搜索上按 `Backspace` 以取消

搜索显示匹配的命令，搜索词突出显示，因此您可以找到并重用以前的输入。

## 后台 bash 命令

Claude Code 支持在后台运行 bash 命令，允许您在长时间运行的进程执行时继续工作。

### 后台运行的工作原理

当 Claude Code 在后台运行命令时，它异步运行命令并立即返回后台任务 ID。Claude Code 可以在命令继续在后台执行时响应新提示。

要在后台运行命令，您可以：

* 提示 Claude Code 在后台运行命令
* 按 Ctrl+B 将常规 Bash 工具调用移到后台。（Tmux 用户必须按两次 Ctrl+B，因为 tmux 的前缀键。）

**主要功能：**

* 输出被缓冲，Claude 可以使用 TaskOutput 工具检索它
* 后台任务有唯一的 ID 用于跟踪和输出检索
* 当 Claude Code 退出时，后台任务会自动清理

要禁用所有后台任务功能，请将 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 环境变量设置为 `1`。有关详细信息，请参阅[环境变量](/zh-CN/settings#environment-variables)。

**常见的后台命令：**

* 构建工具（webpack、vite、make）
* 包管理器（npm、yarn、pnpm）
* 测试运行器（jest、pytest）
* 开发服务器
* 长时间运行的进程（docker、terraform）

### 使用 `!` 前缀的 Bash 模式

通过在输入前加上 `!` 来直接运行 bash 命令，无需通过 Claude：

```bash  theme={null}
! npm test
! git status
! ls -la
```

Bash 模式：

* 将命令及其输出添加到对话上下文
* 显示实时进度和输出
* 支持相同的 `Ctrl+B` 后台运行以处理长时间运行的命令
* 不需要 Claude 解释或批准命令
* 支持基于历史的自动完成：输入部分命令并按 **Tab** 从当前项目中的上一个 `!` 命令完成
* 使用 `Escape`、`Backspace` 或在空提示上按 `Ctrl+U` 退出

这对于快速 shell 操作同时保持对话上下文很有用。

## 提示建议

当您首次打开会话时，灰显的示例命令会出现在提示输入中以帮助您入门。Claude Code 从您项目的 git 历史中选择此命令，因此它反映了您最近一直在处理的文件。

Claude 响应后，建议会根据您的对话历史继续出现，例如多部分请求的后续步骤或工作流的自然延续。

* 按 **Tab** 接受建议，或按 **Enter** 接受并提交
* 开始输入以关闭它

建议作为后台请求运行，重用父对话的 prompt cache，因此额外成本最小。当缓存冷时，Claude Code 会跳过建议生成以避免不必要的成本。

在对话的第一个回合、非交互模式和 plan mode 中，建议会自动跳过。

要完全禁用提示建议，请设置环境变量或在 `/config` 中切换设置：

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## 使用 /btw 的侧问题

使用 `/btw` 提出关于您当前工作的快速问题，无需添加到对话历史。当您想要快速答案但不想使主上下文混乱或使 Claude 偏离长时间运行的任务时，这很有用。

```
/btw what was the name of that config file again?
```

侧问题可以完全看到当前对话，因此您可以询问 Claude 已经读过的代码、它之前做出的决定或会话中的任何其他内容。问题和答案是短暂的：它们出现在可关闭的覆盖层中，永远不会进入对话历史。

* **在 Claude 工作时可用**：即使 Claude 正在处理响应，您也可以运行 `/btw`。侧问题独立运行，不会中断主回合。
* **无工具访问**：侧问题仅从已在上下文中的内容回答。Claude 在回答侧问题时无法读取文件、运行命令或搜索。
* **单一响应**：没有后续回合。如果您需要来回往复，请改用正常提示。
* **低成本**：侧问题重用父对话的 prompt cache，因此额外成本最小。

按 **Space**、**Enter** 或 **Escape** 关闭答案并返回提示。

`/btw` 是 [subagent](/zh-CN/sub-agents) 的反面：它看到您的完整对话但没有工具，而 subagent 有完整的工具但从空上下文开始。使用 `/btw` 询问 Claude 从此会话已知的内容；使用 subagent 去发现新的东西。

## 任务列表

在处理复杂的多步骤工作时，Claude 会创建任务列表来跟踪进度。任务出现在终端的状态区域中，指示器显示待处理、进行中或完成的内容。

* 按 `Ctrl+T` 切换任务列表视图。显示一次最多 10 个任务
* 要查看所有任务或清除它们，直接询问 Claude："show me all tasks"或"clear all tasks"
* 任务在上下文压缩中持续存在，帮助 Claude 在较大的项目上保持组织
* 要在会话之间共享任务列表，请设置 `CLAUDE_CODE_TASK_LIST_ID` 以使用 `~/.claude/tasks/` 中的命名目录：`CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* 要恢复到上一个 TODO 列表，请设置 `CLAUDE_CODE_ENABLE_TASKS=false`。

## PR 审查状态

在处理具有开放 pull request 的分支时，Claude Code 在页脚中显示可点击的 PR 链接（例如"PR #446"）。该链接有一个彩色下划线，指示审查状态：

* 绿色：已批准
* 黄色：待审查
* 红色：请求更改
* 灰色：草稿
* 紫色：已合并

`Cmd+click`（Mac）或 `Ctrl+click`（Windows/Linux）链接以在浏览器中打开 pull request。状态每 60 秒自动更新一次。

<Note>
  PR 状态需要安装并验证 `gh` CLI（`gh auth login`）。
</Note>

## 另请参阅

* [Skills](/zh-CN/skills) - 自定义提示和工作流
* [Checkpointing](/zh-CN/checkpointing) - 回退 Claude 的编辑并恢复以前的状态
* [CLI reference](/zh-CN/cli-reference) - 命令行标志和选项
* [Settings](/zh-CN/settings) - 配置选项
* [Memory management](/zh-CN/memory) - 管理 CLAUDE.md 文件
