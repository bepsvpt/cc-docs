> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置权限

> 通过细粒度权限规则、模式和托管策略来控制 Claude Code 可以访问和执行的操作。

Claude Code 支持细粒度权限，因此您可以精确指定代理允许执行的操作和不允许执行的操作。权限设置可以检入版本控制并分发给组织中的所有开发人员，也可以由个别开发人员自定义。

## 权限系统

Claude Code 使用分层权限系统来平衡功能和安全性：

| 工具类型    | 示例            | 需要批准 | "是，不再询问"行为    |
| :------ | :------------ | :--- | :------------ |
| 只读      | 文件读取、Grep     | 否    | 不适用           |
| Bash 命令 | Shell 执行      | 是    | 每个项目目录和命令永久有效 |
| 文件修改    | Edit/Write 文件 | 是    | 直到会话结束        |

## 管理权限

您可以使用 `/permissions` 查看和管理 Claude Code 的工具权限。此 UI 列出所有权限规则和它们来自的 settings.json 文件。

* **Allow** 规则让 Claude Code 使用指定的工具而无需手动批准。
* **Ask** 规则在 Claude Code 尝试使用指定工具时提示确认。
* **Deny** 规则防止 Claude Code 使用指定的工具。

规则按顺序评估：**deny -> ask -> allow**。第一个匹配的规则获胜，因此 deny 规则始终优先。

## 权限模式

Claude Code 支持多种权限模式来控制工具的批准方式。请参阅[权限模式](/zh-CN/permission-modes)了解何时使用每种模式。在您的[设置文件](/zh-CN/settings#settings-files)中设置 `defaultMode`：

| 模式                  | 描述                                                                               |
| :------------------ | :------------------------------------------------------------------------------- |
| `default`           | 标准行为：在首次使用每个工具时提示权限                                                              |
| `acceptEdits`       | 自动接受工作目录或 `additionalDirectories` 中路径的文件编辑和常见文件系统命令（`mkdir`、`touch`、`mv`、`cp` 等） |
| `plan`              | Plan Mode：Claude 可以分析但不能修改文件或执行命令                                                |
| `auto`              | 自动批准工具调用，并进行后台安全检查以验证操作与您的请求一致。目前处于研究预览阶段                                        |
| `dontAsk`           | 自动拒绝工具，除非通过 `/permissions` 或 `permissions.allow` 规则预先批准                          |
| `bypassPermissions` | 跳过权限提示，除了对受保护目录的写入（请参见下面的警告）                                                     |

<Warning>
  `bypassPermissions` 模式跳过权限提示。对 `.git`、`.claude`、`.vscode`、`.idea` 和 `.husky` 目录的写入仍然会提示确认，以防止意外损坏存储库状态、编辑器配置和 git hooks。对 `.claude/commands`、`.claude/agents` 和 `.claude/skills` 的写入被豁免，不会提示，因为 Claude 在创建技能、子代理和命令时经常在那里写入。仅在隔离环境（如容器或虚拟机）中使用此模式，其中 Claude Code 无法造成损害。管理员可以通过在[托管设置](#managed-settings)中将 `permissions.disableBypassPermissionsMode` 设置为 `"disable"` 来防止此模式。
</Warning>

为了防止使用 `bypassPermissions` 或 `auto` 模式，在任何[设置文件](/zh-CN/settings#settings-files)中将 `permissions.disableBypassPermissionsMode` 或 `permissions.disableAutoMode` 设置为 `"disable"`。这些在[托管设置](#managed-settings)中最有用，因为它们无法被覆盖。

## 权限规则语法

权限规则遵循格式 `Tool` 或 `Tool(specifier)`。

### 匹配工具的所有使用

要匹配工具的所有使用，只需使用工具名称而不带括号：

| 规则         | 效果           |
| :--------- | :----------- |
| `Bash`     | 匹配所有 Bash 命令 |
| `WebFetch` | 匹配所有网络获取请求   |
| `Read`     | 匹配所有文件读取     |

`Bash(*)` 等同于 `Bash` 并匹配所有 Bash 命令。

### 使用说明符进行细粒度控制

在括号中添加说明符以匹配特定的工具使用：

| 规则                             | 效果                      |
| :----------------------------- | :---------------------- |
| `Bash(npm run build)`          | 匹配确切的命令 `npm run build` |
| `Read(./.env)`                 | 匹配读取当前目录中的 `.env` 文件    |
| `WebFetch(domain:example.com)` | 匹配对 example.com 的获取请求   |

### 通配符模式

Bash 规则支持带有 `*` 的 glob 模式。通配符可以出现在命令中的任何位置。此配置允许 npm 和 git commit 命令，同时阻止 git push：

```json theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

`*` 前的空格很重要：`Bash(ls *)` 匹配 `ls -la` 但不匹配 `lsof`，而 `Bash(ls*)` 匹配两者。`:*` 后缀是编写尾部通配符的等效方式，因此 `Bash(ls:*)` 匹配与 `Bash(ls *)` 相同的命令。

当您为命令前缀选择"是，不再询问"时，权限对话框会写入空格分隔的形式。`:*` 形式仅在模式末尾被识别。在像 `Bash(git:* push)` 这样的模式中，冒号被视为文字字符，不会匹配 git 命令。

## 工具特定的权限规则

### Bash

Bash 权限规则支持带有 `*` 的通配符匹配。通配符可以出现在命令中的任何位置，包括开头、中间或结尾：

* `Bash(npm run build)` 匹配确切的 Bash 命令 `npm run build`
* `Bash(npm run test *)` 匹配以 `npm run test` 开头的 Bash 命令
* `Bash(npm *)` 匹配任何以 `npm ` 开头的命令
* `Bash(* install)` 匹配任何以 ` install` 结尾的命令
* `Bash(git * main)` 匹配 `git checkout main` 和 `git log --oneline main` 等命令

单个 `*` 匹配任何字符序列，包括空格，因此一个通配符可以跨越多个参数。`Bash(git *)` 匹配 `git log --oneline --all`，`Bash(git * main)` 匹配 `git push origin main` 以及 `git merge main`。

当 `*` 出现在末尾且前面有空格时（如 `Bash(ls *)`），它强制执行单词边界，要求前缀后跟空格或字符串结尾。例如，`Bash(ls *)` 匹配 `ls -la` 但不匹配 `lsof`。相比之下，`Bash(ls*)` 没有空格匹配 `ls -la` 和 `lsof` 两者，因为没有单词边界约束。

#### 复合命令

<Tip>
  Claude Code 知道 shell 运算符，所以像 `Bash(safe-cmd *)` 这样的规则不会给它权限运行命令 `safe-cmd && other-cmd`。识别的命令分隔符是 `&&`、`||`、`;`、`|`、`|&`、`&` 和换行符。规则必须独立匹配每个子命令。
</Tip>

当您使用"是，不再询问"批准复合命令时，Claude Code 会为需要批准的每个子命令保存一个单独的规则，而不是为完整的复合字符串保存单个规则。例如，批准 `git status && npm test` 会为 `npm test` 保存一个规则，因此将来的 `npm test` 调用被识别，无论 `&&` 前面是什么。诸如 `cd` 进入子目录之类的子命令会为该路径生成自己的 Read 规则。单个复合命令最多可能保存 5 个规则。

#### 进程包装器

在匹配 Bash 规则之前，Claude Code 会剥离一组固定的进程包装器，因此像 `Bash(npm test *)` 这样的规则也匹配 `timeout 30 npm test`。识别的包装器是 `timeout`、`time`、`nice`、`nohup` 和 `stdbuf`。

裸 `xargs` 也被剥离，所以 `Bash(grep *)` 匹配 `xargs grep pattern`。剥离仅在 `xargs` 没有标志时适用：像 `xargs -n1 grep pattern` 这样的调用被匹配为 `xargs` 命令，因此为内部命令编写的规则不涵盖它。

此包装器列表是内置的，不可配置。开发环境运行器，如 `direnv exec`、`devbox run`、`mise exec`、`npx` 和 `docker exec` 不在列表中。因为这些工具将其参数作为命令执行，像 `Bash(devbox run *)` 这样的规则匹配 `run` 之后的任何内容，包括 `devbox run rm -rf .`。要批准环境运行器内的工作，请编写一个包含运行器和内部命令的特定规则，如 `Bash(devbox run npm test)`。为您想要允许的每个内部命令添加一个规则。

Exec 包装器，如 `watch`、`setsid`、`ionice` 和 `flock` 总是提示，无法通过像 `Bash(watch *)` 这样的前缀规则自动批准。同样适用于带有 `-exec` 或 `-delete` 的 `find`：`Bash(find *)` 规则不涵盖这些形式。要批准特定调用，请为完整命令字符串编写精确匹配规则。

#### 只读命令

Claude Code 将一组内置 Bash 命令识别为只读，并在每种模式下无需权限提示即可运行它们。这些包括 `ls`、`cat`、`head`、`tail`、`grep`、`find`、`wc`、`diff`、`stat`、`du`、`cd` 和 `git` 的只读形式。该集合不可配置；要对其中一个命令要求提示，请为其添加 `ask` 或 `deny` 规则。

对于每个标志都是只读的命令，允许未引用的 glob 模式，因此 `ls *.ts` 和 `wc -l src/*.py` 无需提示即可运行。带有写入能力或执行能力标志的命令，如 `find`、`sort`、`sed` 和 `git`，在存在未引用的 glob 时仍然提示，因为 glob 可能扩展为像 `-delete` 这样的标志。

`cd` 进入工作目录或[其他目录](#working-directories)内的路径也是只读的。像 `cd packages/api && ls` 这样的复合命令在每个部分都符合条件时无需提示即可运行。在一个复合命令中组合 `cd` 和 `git` 总是提示，无论目标目录如何。

<Warning>
  尝试约束命令参数的 Bash 权限模式很脆弱。例如，`Bash(curl http://github.com/ *)` 旨在将 curl 限制为 GitHub URL，但不会匹配以下变体：

  * URL 前的选项：`curl -X GET http://github.com/...`
  * 不同的协议：`curl https://github.com/...`
  * 重定向：`curl -L http://bit.ly/xyz`（重定向到 github）
  * 变量：`URL=http://github.com && curl $URL`
  * 额外空格：`curl  http://github.com`

  为了更可靠的 URL 过滤，请考虑：

  * **限制 Bash 网络工具**：使用 deny 规则阻止 `curl`、`wget` 和类似命令，然后对允许的域使用带有 `WebFetch(domain:github.com)` 权限的 WebFetch 工具
  * **使用 PreToolUse hooks**：实现一个 hook 来验证 Bash 命令中的 URL 并阻止不允许的域
  * 通过 CLAUDE.md 指示 Claude Code 关于您允许的 curl 模式

  请注意，仅使用 WebFetch 不会阻止网络访问。如果允许 Bash，Claude 仍然可以使用 `curl`、`wget` 或其他工具来访问任何 URL。
</Warning>

### Read 和 Edit

`Edit` 规则适用于所有编辑文件的内置工具。Claude 尽力将 `Read` 规则应用于所有读取文件的内置工具，如 Grep 和 Glob。

<Warning>
  Read 和 Edit deny 规则适用于 Claude 的内置文件工具，不适用于 Bash 子进程。`Read(./.env)` deny 规则阻止 Read 工具，但不会阻止 Bash 中的 `cat .env`。为了获得阻止所有进程访问路径的 OS 级别强制执行，请[启用沙箱](/zh-CN/sandboxing)。
</Warning>

Read 和 Edit 规则都遵循 [gitignore](https://git-scm.com/docs/gitignore) 规范，具有四种不同的模式类型：

| 模式                | 含义                 | 示例                               | 匹配                             |
| ----------------- | ------------------ | -------------------------------- | ------------------------------ |
| `//path`          | 来自文件系统根目录的**绝对**路径 | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`          | 来自**主**目录的路径       | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`           | **相对于项目根目录**的路径    | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` 或 `./path` | **相对于当前目录**的路径     | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  像 `/Users/alice/file` 这样的模式不是绝对路径。它相对于项目根目录。对于绝对路径，使用 `//Users/alice/file`。
</Warning>

在 Windows 上，路径在匹配前被规范化为 POSIX 形式。`C:\Users\alice` 变成 `/c/Users/alice`，因此使用 `//c/**/.env` 来匹配该驱动器上的 `.env` 文件。要在所有驱动器上匹配，使用 `//**/.env`。

示例：

* `Edit(/docs/**)`：编辑 `<project>/docs/` 中的文件（不是 `/docs/` 也不是 `<project>/.claude/docs/`）
* `Read(~/.zshrc)`：读取您主目录的 `.zshrc`
* `Edit(//tmp/scratch.txt)`：编辑绝对路径 `/tmp/scratch.txt`
* `Read(src/**)`：从 `<current-directory>/src/` 读取

<Note>
  在 gitignore 模式中，`*` 匹配单个目录中的文件，而 `**` 递归匹配目录。要允许所有文件访问，只需使用工具名称而不带括号：`Read`、`Edit` 或 `Write`。
</Note>

当 Claude 访问符号链接时，权限规则检查两个路径：符号链接本身和它解析到的文件。Allow 和 deny 规则对该对的处理方式不同：allow 规则回退到提示您，而 deny 规则直接阻止。

* **Allow 规则**：仅在符号链接路径及其目标都匹配时适用。允许目录内的符号链接指向其外部仍然会提示您。
* **Deny 规则**：当符号链接路径或其目标匹配时适用。指向被拒绝文件的符号链接本身被拒绝。

例如，使用 `Read(./project/**)` 允许和 `Read(~/.ssh/**)` 拒绝，`./project/key` 处的符号链接指向 `~/.ssh/id_rsa` 被阻止：目标未通过 allow 规则，并匹配 deny 规则。

### WebFetch

* `WebFetch(domain:example.com)` 匹配对 example.com 的获取请求

### MCP

* `mcp__puppeteer` 匹配由 `puppeteer` 服务器提供的任何工具（在 Claude Code 中配置的名称）
* `mcp__puppeteer__*` 通配符语法，也匹配来自 `puppeteer` 服务器的所有工具
* `mcp__puppeteer__puppeteer_navigate` 匹配由 `puppeteer` 服务器提供的 `puppeteer_navigate` 工具

### Agent（subagents）

使用 `Agent(AgentName)` 规则来控制 Claude 可以使用哪些[子代理](/zh-CN/sub-agents)：

* `Agent(Explore)` 匹配 Explore 子代理
* `Agent(Plan)` 匹配 Plan 子代理
* `Agent(my-custom-agent)` 匹配名为 `my-custom-agent` 的自定义子代理

将这些规则添加到您的设置中的 `deny` 数组，或使用 `--disallowedTools` CLI 标志来禁用特定代理。要禁用 Explore 代理：

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## 使用 hooks 扩展权限

[Claude Code hooks](/zh-CN/hooks-guide)提供了一种方法来注册自定义 shell 命令以在运行时执行权限评估。当 Claude Code 进行工具调用时，PreToolUse hooks 在权限提示之前运行。hook 输出可以拒绝工具调用、强制提示或跳过提示以让调用继续。

Hook 决定不会绕过权限规则。Deny 和 ask 规则在 hook 返回 `"allow"` 或 `"ask"` 后仍然被评估，因此匹配的 deny 规则仍然会阻止调用，匹配的 ask 规则即使在 hook 返回 `"allow"` 或 `"ask"` 时仍然提示。这保留了[管理权限](#manage-permissions)中描述的 deny 优先级，包括在托管设置中设置的 deny 规则。

阻止 hook 也优先于 allow 规则。以退出代码 2 退出的 hook 在权限规则被评估之前停止工具调用，因此即使 allow 规则会让调用继续，阻止也适用。要运行所有 Bash 命令而无需提示，除了您想要阻止的少数几个，将 `"Bash"` 添加到您的 allow 列表，并注册一个 PreToolUse hook 来拒绝那些特定命令。请参见[阻止对受保护文件的编辑](/zh-CN/hooks-guide#block-edits-to-protected-files)以获取您可以调整的 hook 脚本。

## 工作目录

默认情况下，Claude 可以访问启动它的目录中的文件。您可以扩展此访问：

* **启动期间**：使用 `--add-dir <path>` CLI 参数
* **会话期间**：使用 `/add-dir` 命令
* **持久配置**：添加到[设置文件](/zh-CN/settings#settings-files)中的 `additionalDirectories`

其他目录中的文件遵循与原始工作目录相同的权限规则：它们变为可读的而无需提示，文件编辑权限遵循当前权限模式。

### 其他目录授予文件访问权限，而不是配置

添加目录扩展 Claude 可以读取和编辑文件的位置。它不会使该目录成为完整的配置根目录：大多数 `.claude/` 配置不是从其他目录发现的，尽管有几种类型作为例外被加载。

以下配置类型从 `--add-dir` 目录加载：

| 配置                                                                 | 从 `--add-dir` 加载                                                                                |
| :----------------------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| `.claude/skills/` 中的 [Skills](/zh-CN/skills)                       | 是，带有实时重新加载                                                                                      |
| `.claude/settings.json` 中的插件设置                                     | 仅 `enabledPlugins` 和 `extraKnownMarketplaces`                                                   |
| [CLAUDE.md](/zh-CN/memory) 文件、`.claude/rules/` 和 `CLAUDE.local.md` | 仅当设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` 时。`CLAUDE.local.md` 另外需要 `local` 设置源，默认启用 |

其他所有内容，包括子代理、命令、输出样式、hooks 和其他设置，仅从当前工作目录及其父目录、您在 `~/.claude/` 的用户目录和托管设置中发现。要在项目间共享该配置，请使用以下方法之一：

* **用户级配置**：将文件放在 `~/.claude/agents/`、`~/.claude/output-styles/` 或 `~/.claude/settings.json` 中，使其在每个项目中可用
* **插件**：将配置打包并分发为[插件](/zh-CN/plugins)，团队可以安装
* **从配置目录启动**：从包含您想要的 `.claude/` 配置的目录运行 Claude Code

## 权限如何与沙箱交互

权限和[沙箱](/zh-CN/sandboxing)是互补的安全层：

* **权限**控制 Claude Code 可以使用哪些工具以及它可以访问哪些文件或域。它们适用于所有工具（Bash、Read、Edit、WebFetch、MCP 和其他）。
* **沙箱**提供 OS 级别的强制执行，限制 Bash 工具的文件系统和网络访问。它仅适用于 Bash 命令及其子进程。

使用两者进行深度防御：

* 权限 deny 规则阻止 Claude 甚至尝试访问受限资源
* 沙箱限制防止 Bash 命令到达定义边界之外的资源，即使提示注入绕过 Claude 的决策制定
* 沙箱中的文件系统限制使用 Read 和 Edit deny 规则，而不是单独的沙箱配置
* 网络限制结合 WebFetch 权限规则与沙箱的 `allowedDomains` 和 `deniedDomains` 列表

当沙箱启用 `autoAllowBashIfSandboxed: true`（这是默认值）时，沙箱化的 Bash 命令无需提示即可运行，即使您的权限包括 `ask: Bash(*)`。沙箱边界替代了每个命令的提示。显式 deny 规则仍然适用，针对 `/`、您的主目录或其他关键系统路径的 `rm` 或 `rmdir` 命令仍然会触发提示。请参见[沙箱模式](/zh-CN/sandboxing#sandbox-modes)以更改此行为。

## 托管设置

对于需要对 Claude Code 配置进行集中控制的组织，管理员可以部署无法被用户或项目设置覆盖的托管设置。这些策略设置遵循与常规设置文件相同的格式，可以通过 MDM/OS 级别策略、托管设置文件或[服务器托管设置](/zh-CN/server-managed-settings)传递。有关传递机制和文件位置，请参见[设置文件](/zh-CN/settings#settings-files)。

### 仅托管设置

以下设置仅在托管设置中有效。将它们放在用户或项目设置文件中无效。

| 设置                                             | 描述                                                                                                                                           |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | 可能推送消息的频道插件的允许列表。设置时替换默认 Anthropic 允许列表。需要 `channelsEnabled: true`。请参见[限制哪些频道插件可以运行](/zh-CN/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | 当为 `true` 时，仅加载托管 hooks、SDK hooks 和托管设置 `enabledPlugins` 中强制启用的插件中的 hooks。用户、项目和所有其他插件 hooks 被阻止                                             |
| `allowManagedMcpServersOnly`                   | 当为 `true` 时，仅尊重来自托管设置的 `allowedMcpServers`。`deniedMcpServers` 仍然从所有来源合并。请参见[托管 MCP 配置](/zh-CN/mcp#managed-mcp-configuration)                 |
| `allowManagedPermissionRulesOnly`              | 当为 `true` 时，防止用户和项目设置定义 `allow`、`ask` 或 `deny` 权限规则。仅应用托管设置中的规则                                                                              |
| `blockedMarketplaces`                          | 市场来源的黑名单。在下载前检查被阻止的来源，因此它们永远不会接触文件系统。请参见[托管市场限制](/zh-CN/plugin-marketplaces#managed-marketplace-restrictions)                                |
| `channelsEnabled`                              | 允许 Team 和 Enterprise 用户使用[频道](/zh-CN/channels)。未设置或 `false` 会阻止频道消息传递，无论用户传递什么给 `--channels`                                                 |
| `forceRemoteSettingsRefresh`                   | 当为 `true` 时，阻止 CLI 启动直到远程托管设置被新鲜获取，如果获取失败则退出。请参见[故障关闭强制执行](/zh-CN/server-managed-settings#enforce-fail-closed-startup)                       |
| `pluginTrustMessage`                           | 自定义消息，附加到安装前显示的插件信任警告                                                                                                                        |
| `sandbox.filesystem.allowManagedReadPathsOnly` | 当为 `true` 时，仅尊重来自托管设置的 `filesystem.allowRead` 路径。`denyRead` 仍然从所有来源合并                                                                        |
| `sandbox.network.allowManagedDomainsOnly`      | 当为 `true` 时，仅尊重来自托管设置的 `allowedDomains` 和 `WebFetch(domain:...)` allow 规则。非允许的域被自动阻止，不提示用户。被拒绝的域仍然从所有来源合并                                    |
| `strictKnownMarketplaces`                      | 控制用户可以添加和安装插件的插件市场来源。请参见[托管市场限制](/zh-CN/plugin-marketplaces#managed-marketplace-restrictions)                                                |

`disableBypassPermissionsMode` 通常放在托管设置中以强制执行组织策略，但它可以从任何范围工作。用户可以在自己的设置中设置它以将自己锁定在绕过模式之外。

<Note>
  对[远程控制](/zh-CN/remote-control)和[网络会话](/zh-CN/claude-code-on-the-web)的访问不由托管设置密钥控制。在 Team 和 Enterprise 计划上，管理员在[Claude Code 管理设置](https://claude.ai/admin-settings/claude-code)中启用或禁用这些功能。
</Note>

## 设置优先级

权限规则遵循与所有其他 Claude Code 设置相同的[设置优先级](/zh-CN/settings#settings-precedence)：

1. **托管设置**：无法被任何其他级别覆盖，包括命令行参数
2. **命令行参数**：临时会话覆盖
3. **本地项目设置**（`.claude/settings.local.json`）
4. **共享项目设置**（`.claude/settings.json`）
5. **用户设置**（`~/.claude/settings.json`）

如果工具在任何级别被拒绝，没有其他级别可以允许它。例如，托管设置 deny 无法被 `--allowedTools` 覆盖，`--disallowedTools` 可以添加超出托管设置定义的限制。

如果权限在用户设置中被允许但在项目设置中被拒绝，项目设置优先，权限被阻止。

## 示例配置

此[存储库](https://github.com/anthropics/claude-code/tree/main/examples/settings)包括常见部署场景的启动设置配置。将这些用作起点并根据您的需要调整它们。

## 另请参见

* [Settings](/zh-CN/settings)：完整的配置参考，包括权限设置表
* [Configure auto mode](/zh-CN/auto-mode-config)：告诉自动模式分类器您的组织信任哪些基础设施
* [Sandboxing](/zh-CN/sandboxing)：Bash 命令的 OS 级文件系统和网络隔离
* [Authentication](/zh-CN/authentication)：设置用户对 Claude Code 的访问
* [Security](/zh-CN/security)：安全保障和最佳实践
* [Hooks](/zh-CN/hooks-guide)：自动化工作流并扩展权限评估
