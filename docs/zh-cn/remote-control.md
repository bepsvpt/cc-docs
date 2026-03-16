> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 Remote Control 从任何设备继续本地会话

> 使用 Remote Control 从您的手机、平板电脑或任何浏览器继续本地 Claude Code 会话。适用于 claude.ai/code 和 Claude 移动应用。

<Note>
  Remote Control 在所有计划中都可用。Team 和 Enterprise 管理员必须首先在[管理员设置](https://claude.ai/admin-settings/claude-code)中启用 Claude Code。
</Note>

Remote Control 将 [claude.ai/code](https://claude.ai/code) 或 Claude 应用（[iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 和 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)）连接到在您的机器上运行的 Claude Code 会话。在您的办公桌上启动任务，然后从沙发上的手机或另一台计算机上的浏览器继续。

当您在机器上启动 Remote Control 会话时，Claude 会在整个过程中在本地运行，因此没有任何内容会移到云端。使用 Remote Control，您可以：

* **远程使用您的完整本地环境**：您的文件系统、[MCP servers](/zh-CN/mcp)、工具和项目配置都保持可用
* **同时在两个界面上工作**：对话在所有连接的设备上保持同步，因此您可以从终端、浏览器和手机交替发送消息
* **应对中断**：如果您的笔记本电脑进入睡眠状态或网络断开，当您的机器重新上线时，会话会自动重新连接

与在云基础设施上运行的 [Claude Code on the web](/zh-CN/claude-code-on-the-web) 不同，Remote Control 会话直接在您的机器上运行并与您的本地文件系统交互。Web 和移动界面只是该本地会话的一个窗口。

<Note>
  Remote Control 需要 Claude Code v2.1.51 或更高版本。使用 `claude --version` 检查您的版本。
</Note>

本页涵盖设置、如何启动和连接到会话，以及 Remote Control 与 Claude Code on the web 的比较。

## 要求

在使用 Remote Control 之前，请确认您的环境满足以下条件：

* **订阅**：在 Pro、Max、Team 和 Enterprise 计划中可用。Team 和 Enterprise 管理员必须首先在[管理员设置](https://claude.ai/admin-settings/claude-code)中启用 Claude Code。不支持 API 密钥。
* **身份验证**：运行 `claude` 并使用 `/login` 通过 claude.ai 登录（如果您还没有登录）。
* **工作区信任**：在您的项目目录中至少运行一次 `claude` 以接受工作区信任对话框。

## 启动 Remote Control 会话

您可以直接在 Remote Control 中启动新会话，或连接已经运行的会话。

<Tabs>
  <Tab title="新会话">
    导航到您的项目目录并运行：

    ```bash  theme={null}
    claude remote-control
    ```

    该过程在您的终端中保持运行，等待远程连接。它显示一个会话 URL，您可以使用该 URL 从另一个设备[连接](#connect-from-another-device)，您可以按空格键显示 QR 码以从您的手机快速访问。当远程会话处于活动状态时，终端显示连接状态和工具活动。

    此命令支持以下标志：

    * **`--name "My Project"`**：设置在 claude.ai/code 的会话列表中可见的自定义会话标题。您也可以将名称作为位置参数传递：`claude remote-control "My Project"`
    * **`--verbose`**：显示详细的连接和会话日志
    * **`--sandbox`** / **`--no-sandbox`**：启用或禁用[沙箱](/zh-CN/sandboxing)以在会话期间进行文件系统和网络隔离。默认情况下沙箱处于关闭状态。
  </Tab>

  <Tab title="从现有会话">
    如果您已经在 Claude Code 会话中并想远程继续它，请使用 `/remote-control`（或 `/rc`）命令：

    ```text  theme={null}
    /remote-control
    ```

    将名称作为参数传递以设置自定义会话标题：

    ```text  theme={null}
    /remote-control My Project
    ```

    这启动一个 Remote Control 会话，该会话继承您当前的对话历史记录，并显示一个会话 URL 和 QR 码，您可以使用它从另一个设备[连接](#connect-from-another-device)。`--verbose`、`--sandbox` 和 `--no-sandbox` 标志不适用于此命令。
  </Tab>
</Tabs>

### 从另一个设备连接

一旦 Remote Control 会话处于活动状态，您有几种方式从另一个设备连接：

* **打开会话 URL** 在任何浏览器中直接转到 [claude.ai/code](https://claude.ai/code) 上的会话。`claude remote-control` 和 `/remote-control` 都在终端中显示此 URL。
* **扫描 QR 码** 显示在会话 URL 旁边，直接在 Claude 应用中打开它。使用 `claude remote-control` 时，按空格键切换 QR 码显示。
* **打开 [claude.ai/code](https://claude.ai/code) 或 Claude 应用**，在会话列表中按名称查找会话。Remote Control 会话在联机时显示带有绿色状态点的计算机图标。

远程会话从 `--name` 参数（或传递给 `/remote-control` 的名称）、您的最后一条消息、您的 `/rename` 值或"Remote Control session"（如果没有对话历史记录）获取其名称。如果环境已经有活动会话，系统会询问您是否继续它或启动新会话。

如果您还没有 Claude 应用，请在 Claude Code 中使用 `/mobile` 命令显示 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 或 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) 的下载 QR 码。

### 为所有会话启用 Remote Control

默认情况下，Remote Control 仅在您显式运行 `claude remote-control` 或 `/remote-control` 时激活。要为每个会话自动启用它，请在 Claude Code 中运行 `/config` 并将**为所有会话启用 Remote Control** 设置为 `true`。将其设置回 `false` 以禁用。

每个 Claude Code 实例一次支持一个远程会话。如果您运行多个实例，每个实例都有自己的环境和会话。

## 连接和安全

您的本地 Claude Code 会话仅发出出站 HTTPS 请求，从不在您的机器上打开入站端口。当您启动 Remote Control 时，它向 Anthropic API 注册并轮询工作。当您从另一个设备连接时，服务器通过流连接在 Web 或移动客户端与您的本地会话之间路由消息。

所有流量都通过 TLS 上的 Anthropic API 传输，与任何 Claude Code 会话的传输安全相同。连接使用多个短期凭证，每个凭证的范围限定为单一目的并独立过期。

## Remote Control 与 Claude Code on the web 的比较

Remote Control 和 [Claude Code on the web](/zh-CN/claude-code-on-the-web) 都使用 claude.ai/code 界面。关键区别在于会话运行的位置：Remote Control 在您的机器上执行，因此您的本地 MCP servers、工具和项目配置保持可用。Claude Code on the web 在 Anthropic 管理的云基础设施中执行。

当您在本地工作中途并想从另一个设备继续时，使用 Remote Control。当您想在没有任何本地设置的情况下启动任务、处理您没有克隆的存储库或并行运行多个任务时，使用 Claude Code on the web。

## 限制

* **一次一个远程会话**：每个 Claude Code 会话支持一个远程连接。
* **终端必须保持打开**：Remote Control 作为本地进程运行。如果您关闭终端或停止 `claude` 进程，会话将结束。再次运行 `claude remote-control` 以启动新会话。
* **扩展网络中断**：如果您的机器处于唤醒状态但无法在大约 10 分钟以上的时间内到达网络，会话将超时并且进程退出。再次运行 `claude remote-control` 以启动新会话。

## 相关资源

* [Claude Code on the web](/zh-CN/claude-code-on-the-web)：在 Anthropic 管理的云环境中运行会话，而不是在您的机器上
* [身份验证](/zh-CN/authentication)：设置 `/login` 并管理 claude.ai 的凭证
* [CLI 参考](/zh-CN/cli-reference)：包括 `claude remote-control` 的标志和命令的完整列表
* [安全](/zh-CN/security)：Remote Control 会话如何适应 Claude Code 安全模型
* [数据使用](/zh-CN/data-usage)：在本地和远程会话期间通过 Anthropic API 流动的数据
