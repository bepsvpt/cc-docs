> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置沙箱化 Bash 工具

> 了解 Claude Code 的沙箱化 Bash 工具如何提供文件系统和网络隔离，以实现更安全、更自主的代理执行。

Bash 沙箱让 Claude 可以运行大多数 shell 命令，而无需停下来请求权限。与其批准每个命令不同，你定义命令可以接触哪些文件和网络域，操作系统为每个 Bash 命令及其子进程强制执行该边界。

本页涵盖如何：

* [启用沙箱](#get-started)并选择沙箱化命令的批准方式
* [配置](#configure-sandboxing)命令可以到达的路径和网络域
* [将沙箱与权限规则和权限模式结合](#how-sandboxing-relates-to-permissions-and-permission-modes)
* [在整个组织中强制执行沙箱](#configure-the-sandbox-for-your-organization)使用托管设置

<Note>
  要比较其他隔离方法，如开发容器、自定义容器和虚拟机，请参阅 [Sandbox environments](/zh-CN/sandbox-environments)。要减少 Bash 以外工具的权限提示，请参阅 [permission modes](/zh-CN/permission-modes)。
</Note>

## 入门

沙箱内置于 Claude Code 中，在 macOS、Linux 和 WSL2 上运行。不支持原生 Windows。在 Windows 上，在 WSL2 发行版内运行 Claude Code。

在 macOS 上，无需安装任何内容：沙箱使用内置的 Seatbelt 框架。在 Linux 和 WSL2 上，沙箱依赖两个包，详见 [Set up Linux and WSL2](#set-up-linux-and-wsl2)。即使你还没有安装它们，你也可以从 `/sandbox` 开始，因为它的面板显示是否缺少任何内容。

<Steps>
  <Step title="运行 /sandbox">
    启动 Claude Code 会话并运行 `/sandbox` 命令：

    ```text theme={null}
    /sandbox
    ```

    这会打开沙箱面板，有三个选项卡：

    * **Mode**：选择沙箱化命令的批准方式，在下一步中介绍
    * **Overrides**：选择在沙箱下失败的命令是否可以回退到运行非沙箱化。这是 [`allowUnsandboxedCommands`](/zh-CN/settings#sandbox-settings) 设置
    * **Config**：查看已解析的沙箱设置

    如果面板仅显示 Dependencies 选项卡，则缺少必需的包。按照 [Set up Linux and WSL2](#set-up-linux-and-wsl2) 中的说明安装它，重启 Claude Code，然后再次运行 `/sandbox`。
  </Step>

  <Step title="选择一个模式">
    在 Mode 选项卡上，选择自动允许或常规权限。自动允许在不提示的情况下运行沙箱化命令，常规权限即使在命令沙箱化时也保持常规权限提示。有关在自动允许模式下仍会提示哪些命令，请参阅 [Sandbox modes](#sandbox-modes)。
  </Step>

  <Step title="运行 Bash 命令">
    要求 Claude 运行一个命令，例如构建或测试套件。默认情况下，沙箱内的命令只能写入工作目录。命令第一次需要新的网络域时，Claude Code 会提示批准。

    无法沙箱化运行的命令会回退到常规权限流程。要扩大或缩小这些边界，请参阅 [Configure sandboxing](#configure-sandboxing)。
  </Step>
</Steps>

在面板中选择一个模式会写入你的项目的本地设置 `.claude/settings.local.json`，这些设置适用于当前项目，不会检入 git。要在所有项目中启用沙箱，请在 `~/.claude/settings.json` 的用户设置中将 [`sandbox.enabled`](/zh-CN/settings#sandbox-settings) 设置为 `true`。要为组织中的每个开发者强制执行沙箱，请使用 [managed settings](#enforce-sandboxing-with-managed-settings)。

<Warning>
  默认情况下，如果沙箱因缺少依赖项或不支持的平台而无法启动，Claude Code 会显示警告并在没有沙箱的情况下运行命令。要使其成为硬失败，请将 [`sandbox.failIfUnavailable`](/zh-CN/settings#sandbox-settings) 设置为 `true`。这适用于需要沙箱作为安全门的托管部署。
</Warning>

### 设置 Linux 和 WSL2

在 Linux 和 WSL2 上，沙箱依赖两个包：

* [`bubblewrap`](https://github.com/containers/bubblewrap)：无特权沙箱工具，强制执行文件系统隔离
* [`socat`](http://www.dest-unreach.org/socat/)：用于通过沙箱代理路由网络流量的中继

使用你的发行版的包管理器安装它们：

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

安装后，`/sandbox` 中的 Dependencies 选项卡显示 `ripgrep`、`bubblewrap`、`socat` 和 seccomp 过滤器是否在你的平台上可用。Ripgrep 与原生 Claude Code 二进制文件捆绑在一起。seccomp 过滤器是可选的，添加 Unix 域套接字阻止。如果缺少，请使用 `npm install -g @anthropic-ai/sandbox-runtime` 安装它。

当缺少必需的依赖项时，Dependencies 选项卡是唯一显示的选项卡，直到你安装它。依赖项检查在启动时运行，因此在安装包后重启 Claude Code，以便 `/sandbox` 检测到它们。

<AccordionGroup>
  <Accordion title="Ubuntu 24.04 及更高版本：允许 bubblewrap 创建用户命名空间">
    在 Ubuntu 24.04 及更高版本上，默认 AppArmor 策略阻止 bubblewrap 创建隔离所需的用户命名空间。

    要检查你的环境（包括 WSL2 内）是否强制执行此限制，请运行 `sysctl kernel.apparmor_restrict_unprivileged_userns`。如果密钥不存在或返回 `0`，请跳过此步骤。如果返回 `1`，请添加一个 AppArmor 配置文件，授予 `bwrap` 此功能：

    ```bash theme={null}
    sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
    abi <abi/4.0>,
    include <tunables/global>

    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }
    EOF
    ```

    该配置文件仅适用于 `bwrap` 本身，不适用于在沙箱内运行的命令。重新加载 AppArmor 以应用它：

    ```bash theme={null}
    sudo systemctl reload apparmor
    ```
  </Accordion>

  <Accordion title="WSL2 注意事项">
    使用 PowerShell 中的 `wsl -l -v` 检查你的 WSL 版本。如果你看到 `Sandboxing requires WSL2`，你的发行版运行的是 WSL1。将其升级到 WSL2 或在没有沙箱的情况下运行 Claude Code。

    在 WSL2 上，沙箱化命令无法启动 Windows 二进制文件，例如 `cmd.exe`、`powershell.exe` 或 `/mnt/c/` 下的任何内容。WSL 通过 Unix 套接字将这些交给 Windows 主机，沙箱会阻止这些。如果命令需要调用 Windows 二进制文件，请将其添加到 [`excludedCommands`](/zh-CN/settings#sandbox-settings)，以便它在沙箱外运行。
  </Accordion>
</AccordionGroup>

### 沙箱模式

Claude Code 提供两种沙箱模式：

**自动允许模式**：Bash 命令将尝试在沙箱内运行，并自动允许而无需权限。无法沙箱化的命令（例如需要访问非允许主机的网络访问的命令）会回退到常规权限流程，其中 Claude Code 检查你的 [permission rules](/zh-CN/permissions) 并为这些规则不允许的任何命令提示你。

即使在自动允许模式下，以下仍然适用：

* 显式 [deny rules](/zh-CN/permissions) 始终被尊重
* 针对 `/`、你的主目录或其他关键系统路径的 `rm` 或 `rmdir` 命令仍会触发权限提示
* [Ask rules](/zh-CN/permissions) 适用于回退到常规权限流程的命令

**常规权限模式**：所有 Bash 命令都通过常规权限流程，即使沙箱化也是如此。这提供了更多控制，但需要更多批准。

在两种模式中，沙箱都强制执行相同的文件系统和网络限制。区别仅在于沙箱化命令是自动批准还是需要明确权限。

某些命令根本无法在沙箱内运行，例如与其不兼容的工具或需要你未允许的主机的工具。与其让任务失败或要求你关闭沙箱，Claude Code 包括一个逃生舱：当命令因沙箱限制而失败时，Claude 分析失败，可能使用 `dangerouslyDisableSandbox` 参数重试命令。重试的命令在沙箱外运行，因此它通过常规权限流程进行，需要你的批准。

你可以通过在 [sandbox settings](/zh-CN/settings#sandbox-settings) 中设置 `"allowUnsandboxedCommands": false` 来禁用此逃生舱。禁用时，`/sandbox` Overrides 选项卡显示为 **Strict sandbox mode**，`dangerouslyDisableSandbox` 参数被完全忽略，所有命令必须沙箱化运行或在 `excludedCommands` 中明确列出。

<Info>
  自动允许模式独立于你的权限模式设置工作。即使你不在"接受编辑"模式中，启用自动允许时沙箱化的 Bash 命令也会自动运行。这意味着在沙箱边界内修改文件的 Bash 命令将执行而不提示，即使文件编辑工具通常需要批准。
</Info>

## 配置沙箱

通过 `settings.json` 文件自定义沙箱行为。有关完整的配置参考，请参阅 [Settings](/zh-CN/settings#sandbox-settings)。

默认情况下，沙箱化命令只能写入当前工作目录。如果子进程命令（如 `kubectl`、`terraform` 或 `npm`）需要在项目目录外写入，请使用 `sandbox.filesystem.allowWrite` 向特定路径授予访问权限：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

这些路径在操作系统级别强制执行，因此在沙箱内运行的所有命令（包括其子进程）都尊重它们。这是推荐的方法，当工具需要对特定位置的写入访问时，而不是使用 `excludedCommands` 将工具从沙箱中排除。

当在多个 [settings scopes](/zh-CN/settings#settings-precedence) 中定义相同的文件系统数组时，数组被合并：来自每个范围的路径被组合，而不是替换。

路径前缀控制路径的解析方式：

| 前缀        | 含义                                    | 示例                                                                |
| :-------- | :------------------------------------ | :---------------------------------------------------------------- |
| `/`       | 从文件系统根目录的绝对路径                         | `/tmp/build` 保持 `/tmp/build`                                      |
| `~/`      | 相对于主目录                                | `~/.kube` 变为 `$HOME/.kube`                                        |
| `./` 或无前缀 | 对于项目设置相对于项目根目录，或对于用户设置相对于 `~/.claude` | `.claude/settings.json` 中的 `./output` 解析为 `<project-root>/output` |

此语法与 [Read and Edit permission rules](/zh-CN/permissions#read-and-edit) 不同，后者使用 `//path` 表示绝对路径，`/path` 表示项目相对路径。沙箱文件系统路径使用标准约定：`/tmp/build` 是绝对路径。

你也可以使用 `sandbox.filesystem.denyWrite` 和 `sandbox.filesystem.denyRead` 拒绝写入或读取访问，以及使用 `sandbox.filesystem.allowRead` 重新允许被拒绝区域内的特定路径。

下面的示例阻止从整个主目录读取，同时仍允许从当前项目读取。将其放在你的项目的 `.claude/settings.json` 中，因为相对路径 `.` 仅在配置位于项目设置中时才解析为项目根目录：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

`allowRead` 中的 `.` 解析为项目根目录，因为此配置位于项目设置中。如果你将相同的配置放在 `~/.claude/settings.json` 中，`.` 将解析为 `~/.claude`，项目文件将保持被 `denyRead` 规则阻止。

## 沙箱如何工作

### 文件系统隔离

沙箱化 Bash 工具将文件系统访问限制在特定目录：

* **默认写入行为**：对当前工作目录及其子目录的读写访问
* **默认读取行为**：对整个计算机的读取访问，除了某些被拒绝的目录。注意此默认仍允许读取凭证文件，例如 `~/.aws/credentials` 和 `~/.ssh/`。将它们添加到 `denyRead` 以阻止它们。
* **被阻止的访问**：无法在没有明确权限的情况下修改当前工作目录外的文件，包括 shell 配置文件（例如 `~/.bashrc`）和 `/bin/` 中的系统二进制文件
* **可配置**：通过设置定义自定义允许和拒绝的路径

你可以使用设置中的 `sandbox.filesystem.allowWrite` 向其他路径授予写入访问权限。这些限制在操作系统级别强制执行，因此它们适用于所有子进程命令，包括 `kubectl`、`terraform` 和 `npm` 等工具，而不仅仅是 Claude 的文件工具。

### 网络隔离

网络访问通过在沙箱外运行的代理服务器进行控制：

* **域名限制**：没有预先允许的域名。命令第一次需要新的域名时，Claude Code 会提示批准。使用 [`allowedDomains`](/zh-CN/settings#sandbox-settings) 预先允许域名以避免提示。
* **托管锁定**：如果在托管设置中设置了 [`allowManagedDomainsOnly`](/zh-CN/settings#sandbox-settings)，非允许的域名会自动被阻止而不是提示，只有来自托管设置的 `allowedDomains` 被尊重。
* **自定义代理支持**：高级用户可以在出站流量上实现自定义规则
* **全面覆盖**：限制适用于所有脚本、程序和由命令生成的子进程

<Note>
  内置代理基于请求的主机名强制执行允许列表，不会终止或检查 TLS 流量。有关此设计的含义，请参阅 [Security limitations](#security-limitations)，如果你的威胁模型需要 TLS 检查，请参阅 [Custom proxy configuration](#custom-proxy-configuration)。
</Note>

### 操作系统级强制执行

沙箱化 Bash 工具利用操作系统安全原语：

* **macOS**：使用 Seatbelt 进行沙箱强制执行
* **Linux**：使用 [bubblewrap](https://github.com/containers/bubblewrap) 进行隔离
* **WSL2**：使用 bubblewrap，与 Linux 相同

不支持 WSL1，因为 bubblewrap 需要仅在 WSL2 中可用的内核功能。这些操作系统级限制确保由 Claude Code 命令生成的所有子进程都继承相同的安全边界。

这些相同的原语作为独立的 [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropic-experimental/sandbox-runtime) 包提供，[Sandbox environments](/zh-CN/sandbox-environments#sandbox-runtime) 页面将其作为包装整个 Claude Code 进程的单独方法进行介绍。

## 沙箱如何与权限和权限模式相关

沙箱、[permission rules](/zh-CN/permissions) 和 [permission modes](/zh-CN/permission-modes) 是互补的层。下面的部分介绍沙箱如何与每个交互。

### 权限规则

权限规则和沙箱控制不同的事物：

* **权限规则**控制 Claude Code 可以使用哪些工具，在任何工具运行之前进行评估。它们适用于所有工具：Bash、Read、Edit、WebFetch、MCP 和其他工具。
* **沙箱**提供操作系统级强制执行，限制 Bash 命令在文件系统和网络级别可以访问的内容。它仅适用于 Bash 命令及其子进程。

这两个层在强制执行方式上也有所不同。Claude Code 在命令运行之前根据命令字符串和（在自动模式下）单独分类器关于命令是否安全的判断来评估权限决定。操作系统在运行的进程上强制执行沙箱边界，因此无论模型选择运行什么，它都成立，即使允许的命令做的比其名称暗示的更多。

文件系统和网络限制通过沙箱设置和权限规则进行配置：

| 设置或规则                                                          | 它做什么                                                |
| :------------------------------------------------------------- | :-------------------------------------------------- |
| `sandbox.filesystem.allowWrite`                                | 向工作目录外的路径授予子进程写入访问权限                                |
| `sandbox.filesystem.denyWrite` 和 `sandbox.filesystem.denyRead` | 阻止子进程访问特定路径                                         |
| `sandbox.filesystem.allowRead`                                 | 重新允许读取被 `denyRead` 区域内的特定路径                         |
| `Edit` 允许规则                                                    | 授予对特定路径的写入访问权限，与 `sandbox.filesystem.allowWrite` 相同 |
| `Read` 和 `Edit` 拒绝规则                                           | 阻止访问特定文件或目录                                         |
| `WebFetch` 允许和拒绝规则                                             | 控制域名访问                                              |
| 沙箱 `allowedDomains`                                            | 控制 Bash 命令可以到达的域名                                   |
| 沙箱 `deniedDomains`                                             | 阻止特定域名，即使更广泛的 `allowedDomains` 通配符会允许它们             |

来自 `sandbox.filesystem` 设置和权限规则的路径被合并到最终沙箱配置中。

[claude-code repository 的示例目录](https://github.com/anthropics/claude-code/tree/main/examples/settings)包括常见部署场景的启动设置配置，包括沙箱特定的示例。使用这些作为起点，并根据你的需求调整它们。

### 权限模式

`/sandbox` 不是 [permission mode](/zh-CN/permission-modes)。权限模式决定工具调用是否运行以及是否首先提示你，而沙箱限制 Bash 命令运行后可以访问的内容。它们在控制的内容和替换每个操作提示的内容上有所不同：

|                                                                       | 它控制什么             | 替换提示的内容                                                                               |
| :-------------------------------------------------------------------- | :---------------- | :------------------------------------------------------------------------------------ |
| `/sandbox`                                                            | Bash 命令运行后可以访问的内容 | 沙箱边界本身，在 [auto-allow mode](#sandbox-modes) 中                                          |
| [Auto mode](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) | 每个工具调用是否运行        | 审查操作的分类器                                                                              |
| `--dangerously-skip-permissions`                                      | 每个工具调用是否运行        | 无。[Protected path](/zh-CN/permission-modes#protected-paths) 检查也被跳过；仅删除 `/` 或你的主目录仍会提示 |

沙箱的 [auto-allow mode](#sandbox-modes) 与 [auto mode](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 分开：自动允许批准 Bash 命令，因为沙箱边界包含它们，而自动模式使用分类器审查操作。两者独立工作，可以结合。要为无人值守运行选择隔离边界，请参阅 [Sandbox environments](/zh-CN/sandbox-environments#how-isolation-relates-to-permission-modes)。

## 为你的组织配置沙箱

管理员可以为每个用户要求沙箱，防止开发者扩大策略，并通过公司代理路由沙箱流量。

### 使用托管设置强制执行沙箱

要为每个开发者要求沙箱，通过 [managed settings](/zh-CN/settings#settings-files) 提供 `sandbox` 密钥，可以是由你的 MDM 管理的文件，也可以是通过 Claude.ai 上的 [server-managed settings](/zh-CN/server-managed-settings)。

以下托管设置配置启用沙箱，如果沙箱无法初始化则拒绝启动 Claude Code，并防止模型在沙箱外重试命令：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

超过 `enabled` 的两个密钥控制沙箱无法运行命令时会发生什么：

* **`failIfUnavailable`**：缺少的依赖项（例如 Linux 上的 bubblewrap）会阻止 Claude Code 启动，而不是显示警告并回退到非沙箱化执行
* **`allowUnsandboxedCommands: false`**：`dangerouslyDisableSandbox` 逃生舱被忽略，因此在沙箱下失败的命令无法在其外重试

值得考虑与它们一起添加两个补充。为任何必须在没有隔离的情况下运行的组织批准的工具添加 `excludedCommands`。为凭证目录（例如 `~/.aws` 和 `~/.ssh`）添加 [`denyRead`](#filesystem-isolation) 条目，默认读取策略仍允许这些。

沙箱不在原生 Windows 上运行，因此如果你的队伍包括 Windows 主机，请将此配置的范围限制在 macOS 和 Linux，或让这些用户在 WSL2 或容器内运行 Claude Code。

### 防止开发者扩大策略

对于布尔密钥（例如 `enabled` 和 `failIfUnavailable`），Claude Code 使用托管值并忽略开发者在本地设置的任何内容。对于数组密钥（例如 `excludedCommands` 和 `allowRead`），Claude Code 合并来自每个范围的条目，因此开发者可以追加扩大策略的条目。

在托管设置中将 `allowManagedReadPathsOnly` 设置为 `true`，以便仅尊重来自托管设置的 `allowRead` 条目。用户、项目和本地 `allowRead` 条目被忽略。这防止开发者扩大读取访问权限超过组织批准的路径。要以相同的方式将网络域锁定到托管值，请设置 [`allowManagedDomainsOnly`](/zh-CN/settings#sandbox-settings)。

`excludedCommands` 没有等效的仅托管锁定，因此开发者总是可以追加在沙箱外运行其他命令的条目。保持托管列表狭窄。

### 自定义代理配置

对于需要高级网络安全的组织，你可以实现自定义代理以：

* 解密和检查 HTTPS 流量
* 应用自定义过滤规则
* 记录所有网络请求
* 与现有安全基础设施集成

要将 Claude Code 指向你的代理，请在 [sandbox settings](/zh-CN/settings#sandbox-settings) 中设置代理端口：

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

## 故障排除

某些命令在沙箱内失败，即使它们在沙箱外工作。下面的修复涵盖最常见的情况。

* **命令因主机不允许错误而失败**：许多 CLI 工具需要到达特定的主机。在提示时授予权限会将主机添加到你的允许列表，以便该工具在将来在沙箱内运行。
* **`jest` 挂起或失败**：`watchman` 与沙箱不兼容。改为运行 `jest --no-watchman`。
* **Go 基础 CLI 在 macOS 上 TLS 验证失败**：`gh`、`gcloud` 和 `terraform` 等工具在 Seatbelt 下可能无法进行 TLS 验证。在 `excludedCommands` 中列出这些工具以在沙箱外运行它们。如果你使用 `httpProxyPort` 与 MITM 代理和自定义 CA，请改为将 [`enableWeakerNetworkIsolation`](/zh-CN/settings#sandbox-settings) 设置为 `true`。
* **`docker` 命令失败**：`docker` 与沙箱不兼容。将 `docker *` 添加到 `excludedCommands` 以在沙箱外运行它。
* **Bubblewrap 在容器内启动失败**：在无特权容器中，bubblewrap 无法挂载新的 `/proc` 文件系统。将 [`enableWeakerNestedSandbox`](/zh-CN/settings#sandbox-settings) 设置为 `true`，以便内部沙箱绑定挂载容器的现有 `/proc`。仅在外部容器已提供你需要的隔离边界时使用此设置，因为它向沙箱化命令公开进程信息，而新的 `/proc` 挂载会隐藏这些信息。
* **Linux 上的 Seccomp 过滤器**：seccomp 过滤器需要阻止 Unix 域套接字。`/sandbox` 中的 Dependencies 选项卡显示它是否可用。如果缺少，请运行 `npm install -g @anthropic-ai/sandbox-runtime` 以安装助手。
* **`--dangerously-skip-permissions` 以 root 身份失败**：当在 Linux 和 macOS 上以 root 身份或通过 sudo 运行时，此标志被阻止，因为 root 访问加上没有权限提示可以修改系统上的任何文件或服务。检查在识别的沙箱内自动跳过。要在容器中自主运行，请使用 [dev container](/zh-CN/devcontainer) 配置，它以非 root 用户身份运行 Claude Code。

## 限制

沙箱降低风险，但不是完整的隔离边界。在依赖它作为硬安全控制之前，请查看下面的限制。

### 安全限制

* **网络过滤**：网络过滤系统通过限制进程允许连接的域来运行。内置代理不会终止或对出站流量执行 TLS 检查，因此不会检查加密连接的内容。你负责确保只有受信任的域在你的策略中被允许。

<Warning>
  允许广泛的域名（例如 `github.com`）可能会为数据泄露创建路径。因为代理从客户端提供的主机名做出允许决定而不检查 TLS，在沙箱内运行的代码可能会使用 [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) 或类似技术来到达允许列表外的主机。如果你的威胁模型需要更强的保证，请配置一个 [custom proxy](#custom-proxy-configuration)，它终止 TLS 并检查流量，并在沙箱内安装其 CA 证书。更强的 TLS 感知网络隔离是一个活跃的开发领域。
</Warning>

* **通过 Unix 套接字的权限提升**：`allowUnixSockets` 配置可能会无意中授予对可能导致沙箱绕过的强大系统服务的访问权限。例如，允许访问 `/var/run/docker.sock` 有效地通过 Docker 套接字授予对主机系统的访问权限。仔细考虑你通过沙箱允许的任何 Unix 套接字。
* **文件系统权限提升**：过于宽泛的文件系统写入权限可能导致权限提升攻击。允许写入包含 `$PATH` 中的可执行文件、系统配置目录或用户 shell 配置文件（例如 `.bashrc` 或 `.zshrc`）的目录可能导致当其他用户或系统进程访问这些文件时在不同的安全上下文中执行代码。
* **Linux 沙箱强度**：Linux 实现提供强大的文件系统和网络隔离，但包括一个 `enableWeakerNestedSandbox` 模式，使其能够在 Docker 环境中工作而无需特权命名空间，或在禁用无特权用户命名空间的 Linux 主机上。此选项大大削弱了安全性，应仅在其他隔离被强制执行时使用。
* **设置文件受保护**：沙箱自动拒绝对 Claude Code 的 `settings.json` 文件在每个范围和托管设置目录的写入访问，因此沙箱化命令无法修改其自己的策略。

### 平台和工具兼容性

* **平台支持**：支持 macOS、Linux 和 WSL2。不支持 WSL1 和原生 Windows。
* **性能开销**：最小，但某些文件系统操作可能稍慢。
* **工具兼容性**：某些需要特定系统访问模式的工具可能需要配置调整，或可能需要在沙箱外运行。

### 范围

沙箱隔离 Bash 子进程。其他工具在不同的边界下运行：

* **内置文件工具**：Read、Edit 和 Write 直接使用权限系统，而不是通过沙箱运行。请参阅 [permissions](/zh-CN/permissions)。
* **计算机使用**：当 Claude 打开应用程序并控制你的屏幕时，它在你的实际桌面上运行，而不是在隔离的环境中。每个应用程序的权限提示控制每个应用程序。请参阅 [CLI 中的计算机使用](/zh-CN/computer-use) 或 [Desktop 中的计算机使用](/zh-CN/desktop#let-claude-use-your-computer)。
* **环境变量**：沙箱化 Bash 命令默认继承父进程环境，包括在那里设置的任何凭证。要从子进程中删除 Anthropic 和云提供商凭证，请设置 [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/zh-CN/env-vars)。
* **子代理**：[subagents](/zh-CN/sub-agents) 在与父会话相同的进程中运行，并使用相同的沙箱配置。当在父会话中启用沙箱时，子代理内的 Bash 命令被沙箱化。

<Warning>
  有效的沙箱需要**同时**进行文件系统和网络隔离。没有网络隔离，被破坏的代理可能会泄露敏感文件，如 SSH 密钥。没有文件系统隔离，被破坏的代理可能会后门系统资源以获得网络访问权限。当你扩大默认值时，检查 `allowWrite` 路径、广泛的 `allowedDomains` 条目或 `excludedCommands` 异常是否不会撤销另一侧的限制。
</Warning>

## 另请参阅

* [Sandbox environments](/zh-CN/sandbox-environments)：比较内置沙箱与开发容器、容器和虚拟机
* [Security](/zh-CN/security)：全面的安全功能和最佳实践
* [Permissions](/zh-CN/permissions)：权限配置和访问控制
* [Settings](/zh-CN/settings)：完整的配置参考
* [CLI reference](/zh-CN/cli-reference)：命令行选项
