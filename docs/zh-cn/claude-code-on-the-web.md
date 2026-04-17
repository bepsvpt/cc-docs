> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 在网络上使用 Claude Code

> 配置云环境、设置脚本、网络访问和 Docker，在 Anthropic 的沙箱中运行。使用 `--remote` 和 `--teleport` 在网络和终端之间移动会话。

<Note>
  Claude Code on the web 处于研究预览阶段，适用于 Pro、Max 和 Team 用户，以及拥有高级席位或 Chat + Claude Code 席位的 Enterprise 用户。
</Note>

Claude Code on the web 在 [claude.ai/code](https://claude.ai/code) 的 Anthropic 管理的云基础设施上运行任务。会话即使在关闭浏览器后也会持续，你可以从 Claude 移动应用监控它们。

<Tip>
  初次使用 Claude Code on the web？从[入门](/zh-CN/web-quickstart)开始，连接你的 GitHub 账户并提交你的第一个任务。
</Tip>

本页涵盖：

* [GitHub 身份验证选项](#github-authentication-options)：两种连接 GitHub 的方式
* [云环境](#the-cloud-environment)：哪些配置会保留、安装了哪些工具以及如何配置环境
* [设置脚本](#setup-scripts)和依赖管理
* [网络访问](#network-access)：级别、代理和默认允许列表
* [在网络和终端之间移动任务](#move-tasks-between-web-and-terminal)，使用 `--remote` 和 `--teleport`
* [处理会话](#work-with-sessions)：审查、共享、归档、删除
* [自动修复拉取请求](#auto-fix-pull-requests)：自动响应 CI 失败和审查评论
* [安全和隔离](#security-and-isolation)：会话如何隔离
* [限制](#limitations)：速率限制和平台限制

## GitHub 身份验证选项

云会话需要访问你的 GitHub 存储库来克隆代码和推送分支。你可以通过两种方式授予访问权限：

| 方法               | 工作原理                                                                           | 最适合              |
| :--------------- | :----------------------------------------------------------------------------- | :--------------- |
| **GitHub App**   | 在[网络入门](/zh-CN/web-quickstart)期间在特定存储库上安装 Claude GitHub App。访问权限按存储库限定。        | 希望明确的按存储库授权的团队   |
| **`/web-setup`** | 在终端中运行 `/web-setup` 以将本地 `gh` CLI 令牌同步到你的 Claude 账户。访问权限与你的 `gh` 令牌可以看到的内容相匹配。 | 已经使用 `gh` 的个人开发者 |

两种方法都可以。[`/schedule`](/zh-CN/routines)检查任一形式的访问权限，如果都未配置，会提示你运行 `/web-setup`。有关 `/web-setup` 演练，请参阅[从终端连接](/zh-CN/web-quickstart#connect-from-your-terminal)。

GitHub App 是[自动修复](#auto-fix-pull-requests)所必需的，它使用该 App 接收 PR webhooks。如果你使用 `/web-setup` 连接，稍后想要自动修复，请在这些存储库上安装该 App。

Team 和 Enterprise 管理员可以在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 处使用快速网络设置切换来禁用 `/web-setup`。

<Note>
  启用了[零数据保留](/zh-CN/zero-data-retention)的组织无法使用 `/web-setup` 或其他云会话功能。
</Note>

## 云环境

每个会话在一个新的 Anthropic 管理的 VM 中运行，其中克隆了你的存储库。本节涵盖会话启动时可用的内容以及如何自定义它。

### 云会话中可用的内容

云会话从你的存储库的新克隆开始。任何提交到存储库的内容都可用。任何你仅在自己的机器上安装或配置的内容都不可用。

|                                                                | 在云会话中可用 | 原因                                                                                           |
| :------------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------- |
| 你的存储库的 `CLAUDE.md`                                             | 是       | 克隆的一部分                                                                                       |
| 你的存储库的 `.claude/settings.json` hooks                           | 是       | 克隆的一部分                                                                                       |
| 你的存储库的 `.mcp.json` MCP 服务器                                     | 是       | 克隆的一部分                                                                                       |
| 你的存储库的 `.claude/rules/`                                        | 是       | 克隆的一部分                                                                                       |
| 你的存储库的 `.claude/skills/`、`.claude/agents/`、`.claude/commands/` | 是       | 克隆的一部分                                                                                       |
| 在 `.claude/settings.json` 中声明的插件                               | 是       | 在会话启动时从你声明的[市场](/zh-CN/plugin-marketplaces)安装。需要网络访问才能到达市场源                                  |
| 你的用户 `~/.claude/CLAUDE.md`                                     | 否       | 存在于你的机器上，不在存储库中                                                                              |
| 仅在你的用户设置中启用的插件                                                 | 否       | 用户范围的 `enabledPlugins` 存在于 `~/.claude/settings.json` 中。改为在存储库的 `.claude/settings.json` 中声明它们 |
| 你使用 `claude mcp add` 添加的 MCP 服务器                               | 否       | 这些写入你的本地用户配置，不是存储库。改为在[`.mcp.json`](/zh-CN/mcp#project-scope)中声明服务器                          |
| 静态 API 令牌和凭证                                                   | 否       | 尚不存在专用的秘密存储。见下文                                                                              |
| 交互式身份验证，如 AWS SSO                                              | 否       | 不支持。SSO 需要无法在云会话中运行的基于浏览器的登录                                                                 |

要使配置在云会话中可用，请将其提交到存储库。尚不存在专用的秘密存储。环境变量和设置脚本都存储在环境配置中，对任何可以编辑该环境的人可见。如果你需要云会话中的秘密，请将它们添加为环境变量，并考虑这种可见性。

### 已安装的工具

云会话预装了常见的语言运行时、构建工具和数据库。下表按类别总结了包含的内容。

| 类别          | 包含                                                                    |
| :---------- | :-------------------------------------------------------------------- |
| **Python**  | Python 3.x，带有 pip、poetry、uv、black、mypy、pytest、ruff                    |
| **Node.js** | 20、21 和 22（通过 nvm），带有 npm、yarn、pnpm、bun¹、eslint、prettier、chromedriver |
| **Ruby**    | 3.1、3.2、3.3，带有 gem、bundler、rbenv                                      |
| **PHP**     | 8.4，带有 Composer                                                       |
| **Java**    | OpenJDK 21，带有 Maven 和 Gradle                                          |
| **Go**      | 最新稳定版本，带有模块支持                                                         |
| **Rust**    | rustc 和 cargo                                                         |
| **C/C++**   | GCC、Clang、cmake、ninja、conan                                           |
| **Docker**  | docker、dockerd、docker compose                                         |
| **数据库**     | PostgreSQL 16、Redis 7.0                                               |
| **实用工具**    | git、jq、yq、ripgrep、tmux、vim、nano                                       |

¹ Bun 已安装，但对于包获取有已知的[代理兼容性问题](#install-dependencies-with-a-sessionstart-hook)。

要了解确切版本，请要求 Claude 在云会话中运行 `check-tools`。此命令仅存在于云会话中。

### 处理 GitHub 问题和拉取请求

云会话包括内置的 GitHub 工具，让 Claude 可以读取问题、列出拉取请求、获取 diffs 和发布评论，无需任何设置。这些工具通过[GitHub 代理](#github-proxy)进行身份验证，使用你在[GitHub 身份验证选项](#github-authentication-options)下配置的任何方法，所以你的令牌永远不会进入容器。

`gh` CLI 未预装。如果你需要内置工具不涵盖的 `gh` 命令，如 `gh release` 或 `gh workflow run`，请自己安装和身份验证：

<Steps>
  <Step title="在设置脚本中安装 gh">
    将 `apt update && apt install -y gh` 添加到你的[设置脚本](#setup-scripts)。
  </Step>

  <Step title="提供令牌">
    将 `GH_TOKEN` 环境变量添加到你的[环境设置](#configure-your-environment)，使用 GitHub 个人访问令牌。`gh` 会自动读取 `GH_TOKEN`，所以不需要 `gh auth login` 步骤。
  </Step>
</Steps>

### 将工件链接回会话

每个云会话在 claude.ai 上都有一个成绩单 URL，会话可以从 `CLAUDE_CODE_REMOTE_SESSION_ID` 环境变量读取自己的 ID。使用这个在 PR 正文、提交消息、Slack 帖子或生成的报告中放置可追踪的链接，以便审查者可以打开生成它们的运行。

要求 Claude 从环境变量构造链接。以下命令打印 URL：

```bash theme={null}
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

### 运行测试、启动服务和添加包

Claude 作为处理任务的一部分运行测试。在你的提示中要求它，如"修复 `tests/` 中的失败测试"或"在每次更改后运行 pytest"。测试运行器如 pytest、jest 和 cargo test 开箱即用，因为它们已预装。

PostgreSQL 和 Redis 已预装但默认不运行。在会话期间要求 Claude 启动每一个：

```bash theme={null}
service postgresql start
```

```bash theme={null}
service redis-server start
```

Docker 可用于运行容器化服务。要求 Claude 运行 `docker compose up` 来启动你的项目的服务。拉取镜像的网络访问遵循你的环境的[访问级别](#access-levels)，[受信任的默认值](#default-allowed-domains)包括 Docker Hub 和其他常见注册表。

如果你的镜像很大或拉取速度很慢，请将 `docker compose pull` 或 `docker compose build` 添加到你的[设置脚本](#setup-scripts)。拉取的镜像保存在[缓存的环境](#environment-caching)中，所以每个新会话都在磁盘上有它们。缓存仅存储文件，不存储运行的进程，所以 Claude 仍然在每个会话中启动容器。

要添加未预装的包，请使用[设置脚本](#setup-scripts)。脚本的输出被[缓存](#environment-caching)，所以你在那里安装的包在每个会话开始时都可用，无需每次重新安装。你也可以要求 Claude 在会话期间安装包，但这些安装不会在会话之间持续。

### 资源限制

云会话运行时具有可能随时间变化的近似资源上限：

* 4 个 vCPU
* 16 GB RAM
* 30 GB 磁盘

需要明显更多内存的任务，如大型构建作业或内存密集型测试，可能会失败或被终止。对于超出这些限制的工作负载，使用[远程控制](/zh-CN/remote-control)在你自己的硬件上运行 Claude Code。

### 配置你的环境

环境控制[网络访问](#network-access)、环境变量和在会话启动前运行的[设置脚本](#setup-scripts)。有关不需要任何配置即可使用的内容，请参阅[已安装的工具](#installed-tools)。你可以从网络界面或终端管理环境：

| 操作                 | 如何操作                                                                            |
| :----------------- | :------------------------------------------------------------------------------ |
| 添加环境               | 选择当前环境以打开选择器，然后选择**添加环境**。对话框包括名称、网络访问级别、环境变量和设置脚本。                             |
| 编辑环境               | 选择环境名称右侧的设置图标。                                                                  |
| 归档环境               | 打开环境进行编辑并选择**归档**。归档的环境从选择器中隐藏，但现有会话继续运行。                                       |
| 为 `--remote` 设置默认值 | 在终端中运行 `/remote-env`。如果你有单个环境，此命令显示你的当前配置。`/remote-env` 仅选择默认值；从网络界面添加、编辑和归档环境。 |

环境变量使用 `.env` 格式，每行一个 `KEY=value` 对。不要用引号包装值，因为引号会存储为值的一部分。

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

## 设置脚本

设置脚本是一个 Bash 脚本，在新的云会话启动时运行，在 Claude Code 启动之前。使用设置脚本来安装依赖、配置工具或获取会话需要的任何未预装的内容。

脚本在 Ubuntu 24.04 上以 root 身份运行，所以 `apt install` 和大多数语言包管理器都可以工作。

要添加设置脚本，请打开环境设置对话框并在**设置脚本**字段中输入你的脚本。

此示例安装 `gh` CLI，它未预装：

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

如果脚本以非零值退出，会话将无法启动。将 `|| true` 附加到非关键命令以避免在不稳定的安装失败时阻止会话。

<Note>
  安装包的设置脚本需要网络访问才能到达注册表。默认**受信任**网络访问允许连接到[常见包注册表](#default-allowed-domains)，包括 npm、PyPI、RubyGems 和 crates.io。如果你的环境使用**无**网络访问，脚本将无法安装包。
</Note>

### 环境缓存

设置脚本在你首次在环境中启动会话时运行。完成后，Anthropic 会对文件系统进行快照，并将该快照重用作为后续会话的起点。新会话以你的依赖、工具和 Docker 镜像已在磁盘上开始，设置脚本步骤被跳过。这即使在脚本安装大型工具链或拉取容器镜像时也能保持启动速度快。

缓存捕获文件，不捕获运行的进程。设置脚本写入磁盘的任何内容都会保留。它启动的服务或容器不会，所以通过要求 Claude 或使用[SessionStart hook](#setup-scripts-vs-sessionstart-hooks)按会话启动这些。

当你更改环境的设置脚本或允许的网络主机时，以及当缓存在大约七天后达到过期时间时，设置脚本会再次运行以重建缓存。恢复现有会话永远不会重新运行设置脚本。

你不需要启用缓存或自己管理快照。

### 设置脚本与 SessionStart hooks

使用设置脚本来安装云需要但你的笔记本电脑已有的东西，如语言运行时或 CLI 工具。使用[SessionStart hook](/zh-CN/hooks#sessionstart)进行应该在任何地方运行的项目设置，云和本地，如 `npm install`。

两者都在会话开始时运行，但它们属于不同的地方：

|     | 设置脚本                      | SessionStart hooks               |
| --- | ------------------------- | -------------------------------- |
| 附加到 | 云环境                       | 你的存储库                            |
| 配置在 | 云环境 UI                    | 你的存储库中的 `.claude/settings.json`  |
| 运行  | 在 Claude Code 启动之前，仅在新会话上 | 在 Claude Code 启动之后，在每个会话上，包括已恢复的 |
| 范围  | 仅云环境                      | 本地和云                             |

SessionStart hooks 也可以在你的用户级 `~/.claude/settings.json` 中本地定义，但用户级设置不会传送到云会话。在云中，仅提交到存储库的 hooks 运行。

### 使用 SessionStart hook 安装依赖

要仅在云会话中安装依赖，请将 SessionStart hook 添加到你的存储库的 `.claude/settings.json`：

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

在 `scripts/install_pkgs.sh` 创建脚本并使用 `chmod +x` 使其可执行。`CLAUDE_CODE_REMOTE` 环境变量在云会话中设置为 `true`，所以你可以使用它来跳过本地执行：

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

SessionStart hooks 在云会话中有一些限制：

* **无云专用范围**：hooks 在本地和云会话中都运行。要跳过本地执行，请检查脚本中的 `CLAUDE_CODE_REMOTE` 环境变量，如上所示。
* **需要网络访问**：安装命令需要到达包注册表。如果你的环境使用**无**网络访问，这些 hooks 会失败。**受信任**下的[默认允许列表](#default-allowed-domains)涵盖 npm、PyPI、RubyGems 和 crates.io。
* **代理兼容性**：所有出站流量都通过[安全代理](#security-proxy)。某些包管理器不能与此代理正确配合使用。Bun 是一个已知的例子。
* **增加启动延迟**：hooks 在每次会话启动或恢复时运行，不像设置脚本那样受益于[环境缓存](#environment-caching)。通过在重新安装之前检查依赖是否已存在来保持安装脚本快速。

要为后续 Bash 命令持久化环境变量，请写入 `$CLAUDE_ENV_FILE` 处的文件。有关详情，请参阅[SessionStart hooks](/zh-CN/hooks#sessionstart)。

用你自己的 Docker 镜像替换基础镜像尚不支持。使用设置脚本在[提供的镜像](#installed-tools)之上安装你需要的内容，或使用 `docker compose` 与 Claude 并行运行你的镜像作为容器。

## 网络访问

网络访问控制来自云环境的出站连接。每个环境指定一个访问级别，你可以使用自定义允许的域来扩展它。默认值是**受信任**，它允许包注册表和其他[允许列表域](#default-allowed-domains)。

### 访问级别

在创建或编辑环境时选择访问级别：

| 级别      | 出站连接                                                 |
| :------ | :--------------------------------------------------- |
| **无**   | 无出站网络访问                                              |
| **受信任** | [允许列表域](#default-allowed-domains)仅：包注册表、GitHub、云 SDK |
| **完全**  | 任何域                                                  |
| **自定义** | 你自己的允许列表，可选地包括默认值                                    |

GitHub 操作使用独立于此设置的[单独代理](#github-proxy)。

### 允许特定域

要允许不在受信任列表中的域，在环境的网络访问设置中选择**自定义**。出现**允许的域**字段。每行输入一个域：

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

使用 `*.` 进行通配符子域匹配。检查**也包括常见包管理器的默认列表**以在自定义条目旁边保留[受信任的域](#default-allowed-domains)，或将其取消选中以仅允许你列出的内容。

### GitHub 代理

为了安全起见，所有 GitHub 操作都通过专用代理服务进行，该服务透明地处理所有 git 交互。在沙箱内，git 客户端使用自定义构建的作用域凭证进行身份验证。此代理：

* 安全地管理 GitHub 身份验证：git 客户端在沙箱内使用作用域凭证，代理验证并将其转换为你的实际 GitHub 身份验证令牌
* 限制 git push 操作到当前工作分支以确保安全
* 启用克隆、获取和 PR 操作，同时维护安全边界

### 安全代理

环境在 HTTP/HTTPS 网络代理后面运行，用于安全和滥用防止目的。所有出站互联网流量都通过此代理，该代理提供：

* 防止恶意请求
* 速率限制和滥用防止
* 增强安全性的内容过滤

### 默认允许的域

使用**受信任**网络访问时，默认允许以下域。标记为 `*` 的域表示通配符子域匹配，所以 `*.gcr.io` 允许 `gcr.io` 的任何子域。

<AccordionGroup>
  <Accordion title="Anthropic 服务">
    * api.anthropic.com
    * statsig.anthropic.com
    * docs.claude.com
    * platform.claude.com
    * code.claude.com
    * claude.ai
  </Accordion>

  <Accordion title="版本控制">
    * github.com
    * [www.github.com](http://www.github.com)
    * api.github.com
    * npm.pkg.github.com
    * raw\.githubusercontent.com
    * pkg-npm.githubusercontent.com
    * objects.githubusercontent.com
    * release-assets.githubusercontent.com
    * codeload.github.com
    * avatars.githubusercontent.com
    * camo.githubusercontent.com
    * gist.github.com
    * gitlab.com
    * [www.gitlab.com](http://www.gitlab.com)
    * registry.gitlab.com
    * bitbucket.org
    * [www.bitbucket.org](http://www.bitbucket.org)
    * api.bitbucket.org
  </Accordion>

  <Accordion title="容器注册表">
    * registry-1.docker.io
    * auth.docker.io
    * index.docker.io
    * hub.docker.com
    * [www.docker.com](http://www.docker.com)
    * production.cloudflare.docker.com
    * download.docker.com
    * gcr.io
    * \*.gcr.io
    * ghcr.io
    * mcr.microsoft.com
    * \*.data.mcr.microsoft.com
    * public.ecr.aws
  </Accordion>

  <Accordion title="云平台">
    * cloud.google.com
    * accounts.google.com
    * gcloud.google.com
    * \*.googleapis.com
    * storage.googleapis.com
    * compute.googleapis.com
    * container.googleapis.com
    * azure.com
    * portal.azure.com
    * microsoft.com
    * [www.microsoft.com](http://www.microsoft.com)
    * \*.microsoftonline.com
    * packages.microsoft.com
    * dotnet.microsoft.com
    * dot.net
    * visualstudio.com
    * dev.azure.com
    * \*.amazonaws.com
    * \*.api.aws
    * oracle.com
    * [www.oracle.com](http://www.oracle.com)
    * java.com
    * [www.java.com](http://www.java.com)
    * java.net
    * [www.java.net](http://www.java.net)
    * download.oracle.com
    * yum.oracle.com
  </Accordion>

  <Accordion title="JavaScript 和 Node 包管理器">
    * registry.npmjs.org
    * [www.npmjs.com](http://www.npmjs.com)
    * [www.npmjs.org](http://www.npmjs.org)
    * npmjs.com
    * npmjs.org
    * yarnpkg.com
    * registry.yarnpkg.com
  </Accordion>

  <Accordion title="Python 包管理器">
    * pypi.org
    * [www.pypi.org](http://www.pypi.org)
    * files.pythonhosted.org
    * pythonhosted.org
    * test.pypi.org
    * pypi.python.org
    * pypa.io
    * [www.pypa.io](http://www.pypa.io)
  </Accordion>

  <Accordion title="Ruby 包管理器">
    * rubygems.org
    * [www.rubygems.org](http://www.rubygems.org)
    * api.rubygems.org
    * index.rubygems.org
    * ruby-lang.org
    * [www.ruby-lang.org](http://www.ruby-lang.org)
    * rubyforge.org
    * [www.rubyforge.org](http://www.rubyforge.org)
    * rubyonrails.org
    * [www.rubyonrails.org](http://www.rubyonrails.org)
    * rvm.io
    * get.rvm.io
  </Accordion>

  <Accordion title="Rust 包管理器">
    * crates.io
    * [www.crates.io](http://www.crates.io)
    * index.crates.io
    * static.crates.io
    * rustup.rs
    * static.rust-lang.org
    * [www.rust-lang.org](http://www.rust-lang.org)
  </Accordion>

  <Accordion title="Go 包管理器">
    * proxy.golang.org
    * sum.golang.org
    * index.golang.org
    * golang.org
    * [www.golang.org](http://www.golang.org)
    * goproxy.io
    * pkg.go.dev
  </Accordion>

  <Accordion title="JVM 包管理器">
    * maven.org
    * repo.maven.org
    * central.maven.org
    * repo1.maven.org
    * repo.maven.apache.org
    * jcenter.bintray.com
    * gradle.org
    * [www.gradle.org](http://www.gradle.org)
    * services.gradle.org
    * plugins.gradle.org
    * kotlinlang.org
    * [www.kotlinlang.org](http://www.kotlinlang.org)
    * spring.io
    * repo.spring.io
  </Accordion>

  <Accordion title="其他包管理器">
    * packagist.org (PHP Composer)
    * [www.packagist.org](http://www.packagist.org)
    * repo.packagist.org
    * nuget.org (.NET NuGet)
    * [www.nuget.org](http://www.nuget.org)
    * api.nuget.org
    * pub.dev (Dart/Flutter)
    * api.pub.dev
    * hex.pm (Elixir/Erlang)
    * [www.hex.pm](http://www.hex.pm)
    * cpan.org (Perl CPAN)
    * [www.cpan.org](http://www.cpan.org)
    * metacpan.org
    * [www.metacpan.org](http://www.metacpan.org)
    * api.metacpan.org
    * cocoapods.org (iOS/macOS)
    * [www.cocoapods.org](http://www.cocoapods.org)
    * cdn.cocoapods.org
    * haskell.org
    * [www.haskell.org](http://www.haskell.org)
    * hackage.haskell.org
    * swift.org
    * [www.swift.org](http://www.swift.org)
  </Accordion>

  <Accordion title="Linux 发行版">
    * archive.ubuntu.com
    * security.ubuntu.com
    * ubuntu.com
    * [www.ubuntu.com](http://www.ubuntu.com)
    * \*.ubuntu.com
    * ppa.launchpad.net
    * launchpad.net
    * [www.launchpad.net](http://www.launchpad.net)
    * \*.nixos.org
  </Accordion>

  <Accordion title="开发工具和平台">
    * dl.k8s.io (Kubernetes)
    * pkgs.k8s.io
    * k8s.io
    * [www.k8s.io](http://www.k8s.io)
    * releases.hashicorp.com (HashiCorp)
    * apt.releases.hashicorp.com
    * rpm.releases.hashicorp.com
    * archive.releases.hashicorp.com
    * hashicorp.com
    * [www.hashicorp.com](http://www.hashicorp.com)
    * repo.anaconda.com (Anaconda/Conda)
    * conda.anaconda.org
    * anaconda.org
    * [www.anaconda.com](http://www.anaconda.com)
    * anaconda.com
    * continuum.io
    * apache.org (Apache)
    * [www.apache.org](http://www.apache.org)
    * archive.apache.org
    * downloads.apache.org
    * eclipse.org (Eclipse)
    * [www.eclipse.org](http://www.eclipse.org)
    * download.eclipse.org
    * nodejs.org (Node.js)
    * [www.nodejs.org](http://www.nodejs.org)
    * developer.apple.com
    * developer.android.com
    * pkg.stainless.com
    * binaries.prisma.sh
  </Accordion>

  <Accordion title="云服务和监控">
    * statsig.com
    * [www.statsig.com](http://www.statsig.com)
    * api.statsig.com
    * sentry.io
    * \*.sentry.io
    * downloads.sentry-cdn.com
    * http-intake.logs.datadoghq.com
    * \*.datadoghq.com
    * \*.datadoghq.eu
    * api.honeycomb.io
  </Accordion>

  <Accordion title="内容交付和镜像">
    * sourceforge.net
    * \*.sourceforge.net
    * packagecloud.io
    * \*.packagecloud.io
    * fonts.googleapis.com
    * fonts.gstatic.com
  </Accordion>

  <Accordion title="架构和配置">
    * json-schema.org
    * [www.json-schema.org](http://www.json-schema.org)
    * json.schemastore.org
    * [www.schemastore.org](http://www.schemastore.org)
  </Accordion>

  <Accordion title="Model Context Protocol">
    * \*.modelcontextprotocol.io
  </Accordion>
</AccordionGroup>

## 在网络和终端之间移动任务

这些工作流需要[Claude Code CLI](/zh-CN/quickstart)登录到相同的 claude.ai 账户。你可以从终端启动新的云会话，或将云会话拉入终端以在本地继续。云会话即使在关闭笔记本电脑后也会持续，你可以从任何地方（包括 Claude 移动应用）监控它们。

<Note>
  从 CLI，会话切换是单向的：你可以使用 `--teleport` 将云会话拉入终端，但不能将现有的终端会话推送到网络。`--remote` 标志为你的当前存储库创建一个新的云会话。[Desktop 应用](/zh-CN/desktop#continue-in-another-surface)提供了一个"在...中继续"菜单，可以将本地会话发送到网络。
</Note>

### 从终端到网络

使用 `--remote` 标志从命令行启动云会话：

```bash theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

这在 claude.ai 上创建一个新的云会话。会话克隆你当前目录的 GitHub 远程，位于你的当前分支，所以如果你有本地提交，请先推送，因为 VM 从 GitHub 而不是你的机器克隆。`--remote` 一次只能处理单个存储库。任务在云中运行，而你继续在本地工作。

<Note>
  `--remote` 创建云会话。`--remote-control` 无关：它公开本地 CLI 会话以从网络进行监控。请参阅[远程控制](/zh-CN/remote-control)。
</Note>

在 Claude Code CLI 中使用 `/tasks` 检查进度，或在 claude.ai 或 Claude 移动应用上打开会话以直接交互。从那里你可以引导 Claude、提供反馈或回答问题，就像任何其他对话一样。

#### 云任务的提示

**在本地规划，远程执行**：对于复杂的任务，在 Plan Mode 中启动 Claude 以协作制定方法，然后将工作发送到云：

```bash theme={null}
claude --permission-mode plan
```

在 Plan Mode 中，Claude 读取文件、运行命令来探索并提出计划，而不编辑源代码。一旦你满意，将计划保存到存储库、提交和推送，以便云 VM 可以克隆它。然后为自主执行启动云会话：

```bash theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

这种模式让你可以控制策略，同时让 Claude 在云中自主执行。

**在云中使用 ultraplan 规划**：要在网络会话中起草和审查计划本身，请使用[ultraplan](/zh-CN/ultraplan)。Claude 在 Claude Code on the web 上生成计划，而你继续工作，然后你在浏览器中对部分进行评论，并选择远程执行或将计划发送回终端。

**并行运行任务**：每个 `--remote` 命令创建自己的云会话，独立运行。你可以启动多个任务，它们都将在单独的会话中同时运行：

```bash theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

使用 Claude Code CLI 中的 `/tasks` 监控所有会话。当会话完成时，你可以从网络界面创建 PR 或[传送](#from-web-to-terminal)会话到终端以继续工作。

#### 发送没有 GitHub 的本地存储库

当你从未连接到 GitHub 的存储库运行 `claude --remote` 时，Claude Code 会捆绑你的本地存储库并直接上传到云会话。捆绑包包括你的完整存储库历史，跨所有分支，加上对跟踪文件的任何未提交更改。

当 GitHub 访问不可用时，此回退会自动激活。要即使在 GitHub 已连接时也强制它，请设置 `CCR_FORCE_BUNDLE=1`：

```bash theme={null}
CCR_FORCE_BUNDLE=1 claude --remote "Run the test suite and fix any failures"
```

捆绑的存储库必须满足这些限制：

* 目录必须是具有至少一个提交的 git 存储库
* 捆绑的存储库必须在 100 MB 以下。较大的存储库回退到仅捆绑当前分支，然后回退到工作树的单个压缩快照，仅在快照仍然太大时失败
* 未跟踪的文件不包括；在你想要云会话看到的文件上运行 `git add`
* 从捆绑创建的会话无法推送回远程，除非你也配置了[GitHub 身份验证](#github-authentication-options)

### 从网络到终端

使用以下任何方式将云会话拉入终端：

* **使用 `--teleport`**：从命令行，运行 `claude --teleport` 以获得交互式会话选择器，或 `claude --teleport <session-id>` 以直接恢复特定会话。如果你有未提交的更改，系统会提示你先隐藏它们。
* **使用 `/teleport`**：在现有 CLI 会话内，运行 `/teleport`（或 `/tp`）以打开相同的会话选择器，无需重启 Claude Code。
* **从 `/tasks`**：运行 `/tasks` 以查看你的后台会话，然后按 `t` 传送到其中一个
* **从网络界面**：选择**在 CLI 中打开**以复制可以粘贴到终端中的命令

当你传送一个会话时，Claude 验证你在正确的存储库中，从云会话获取并检出分支，并将完整的对话历史加载到终端中。

`--teleport` 不同于 `--resume`。`--resume` 从此机器的本地历史重新打开对话，不列出云会话；`--teleport` 拉取云会话及其分支。

#### 传送要求

传送在恢复会话之前检查这些要求。如果任何要求未满足，你会看到错误或被提示解决问题。

| 要求         | 详情                                    |
| ---------- | ------------------------------------- |
| 干净的 git 状态 | 你的工作目录必须没有未提交的更改。如果需要，传送会提示你隐藏更改。     |
| 正确的存储库     | 你必须从同一存储库的检出运行 `--teleport`，而不是从分叉运行。 |
| 分支可用       | 云会话中的分支必须已被推送到远程。传送会自动获取并检出它。         |
| 相同账户       | 你必须认证到云会话中使用的相同 claude.ai 账户。         |

#### `--teleport` 不可用

传送需要 claude.ai 订阅身份验证。如果你通过 API 密钥、Bedrock、Vertex AI 或 Microsoft Foundry 进行身份验证，请运行 `/login` 以改为使用你的 claude.ai 账户登录。如果你已通过 claude.ai 登录，`--teleport` 仍不可用，你的组织可能已禁用云会话。

## 处理会话

会话出现在 claude.ai/code 的侧边栏中。从那里你可以审查更改、与队友共享、归档完成的工作或永久删除会话。

### 管理上下文

云会话支持产生文本输出的[内置命令](/zh-CN/commands)。打开交互式终端选择器的命令，如 `/model` 或 `/config`，不可用。

对于上下文管理特别是：

| 命令         | 在云会话中工作 | 注释                                                     |
| :--------- | :------ | :----------------------------------------------------- |
| `/compact` | 是       | 总结对话以释放上下文。接受可选的焦点指令，如 `/compact keep the test output` |
| `/context` | 是       | 显示当前在上下文窗口中的内容                                         |
| `/clear`   | 否       | 从侧边栏启动新会话                                              |

自动压缩在上下文窗口接近容量时自动运行，与 CLI 中相同。要更早触发它，在你的[环境变量](#configure-your-environment)中设置 [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/zh-CN/env-vars)。例如，`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` 在 70% 容量而不是默认 \~95% 时压缩。要更改压缩计算的有效窗口大小，请使用 [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/zh-CN/env-vars)。

[Subagents](/zh-CN/sub-agents)的工作方式与本地相同。Claude 可以使用 Task 工具生成它们，以将研究或并行工作卸载到单独的上下文窗口中，保持主对话更轻。在你的存储库的 `.claude/agents/` 中定义的 Subagents 会自动被拾取。[Agent teams](/zh-CN/agent-teams)默认关闭，但可以通过将 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 添加到你的[环境变量](#configure-your-environment)来启用。

### 审查更改

每个会话显示一个 diff 指示器，显示添加和删除的行数，如 `+42 -18`。选择它以打开 diff 视图，在特定行上留下内联评论，并使用你的下一条消息将它们发送给 Claude。有关完整演练（包括 PR 创建），请参阅[审查和迭代](/zh-CN/web-quickstart#review-and-iterate)。要让 Claude 自动监控 PR 以查找 CI 失败和审查评论，请参阅[自动修复拉取请求](#auto-fix-pull-requests)。

### 共享会话

要共享会话，请根据下面的账户类型切换其可见性。之后，按原样共享会话链接。打开链接时，收件人会看到最新状态，但他们的视图不会实时更新。

#### 从 Enterprise 或 Team 账户共享

对于 Enterprise 和 Team 账户，两个可见性选项是**私有**和**团队**。团队可见性使会话对你的 claude.ai 组织的其他成员可见。默认情况下启用存储库访问验证，基于连接到收件人账户的 GitHub 账户。你的账户显示名称对所有有访问权限的收件人可见。[Claude in Slack](/zh-CN/slack) 会话会自动以团队可见性共享。

#### 从 Max 或 Pro 账户共享

对于 Max 和 Pro 账户，两个可见性选项是**私有**和**公开**。公开可见性使会话对任何登录到 claude.ai 的用户可见。

在共享之前检查你的会话是否包含敏感内容。会话可能包含来自私有 GitHub 存储库的代码和凭证。默认情况下不启用存储库访问验证。

要要求收件人拥有存储库访问权限，或从共享会话中隐藏你的名称，请转到设置 > Claude Code > 共享设置。

### 归档会话

你可以归档会话以保持你的会话列表有序。归档的会话从默认会话列表中隐藏，但可以通过筛选已归档会话来查看。

要归档会话，请在侧边栏中悬停在会话上并选择归档图标。

### 删除会话

删除会话会永久删除会话及其数据。此操作无法撤销。你可以通过两种方式删除会话：

* **从侧边栏**：筛选已归档会话，然后悬停在你想删除的会话上并选择删除图标
* **从会话菜单**：打开会话，选择会话标题旁的下拉菜单，然后选择**删除**

删除会话前会要求你确认。

## 自动修复拉取请求

Claude 可以监视拉取请求并自动响应 CI 失败和审查评论。Claude 订阅 PR 上的 GitHub 活动，当检查失败或审查者留下评论时，Claude 会调查并推送修复（如果有明确的修复）。

<Note>
  自动修复需要在你的存储库上安装 Claude GitHub App。如果你还没有，请从 [GitHub App 页面](https://github.com/apps/claude)安装它，或在[设置](/zh-CN/web-quickstart#connect-github-and-create-an-environment)期间出现提示时安装。
</Note>

根据 PR 来自何处以及你使用的设备，有几种方法可以打开自动修复：

* **在 Claude Code on the web 中创建的 PR**：打开 CI 状态栏并选择**自动修复**
* **从终端**：在 PR 的分支上运行 [`/autofix-pr`](/zh-CN/commands)。Claude Code 使用 `gh` 检测打开的 PR，生成网络会话，并一步启用自动修复
* **从移动应用**：告诉 Claude 自动修复 PR，例如"监视此 PR 并修复任何 CI 失败或审查评论"
* **任何现有 PR**：将 PR URL 粘贴到会话中并告诉 Claude 自动修复它

### Claude 如何响应 PR 活动

当自动修复处于活动状态时，Claude 接收 PR 的 GitHub 事件，包括新的审查评论和 CI 检查失败。对于每个事件，Claude 调查并决定如何进行：

* **明确的修复**：如果 Claude 对修复有信心且不与早期指令冲突，Claude 会进行更改、推送它，并在会话中解释所做的工作
* **模糊的请求**：如果审查者的评论可以以多种方式解释或涉及架构上重要的内容，Claude 会在采取行动前询问你
* **重复或无操作事件**：如果事件是重复的或不需要更改，Claude 会在会话中记录它并继续

Claude 可能会作为解决审查评论线程的一部分在 GitHub 上回复它们。这些回复使用你的 GitHub 账户发布，所以它们出现在你的用户名下，但每个回复都标记为来自 Claude Code，以便审查者知道它是由代理编写的，而不是由你直接编写的。

<Warning>
  如果你的存储库使用注释触发的自动化，例如 Atlantis、Terraform Cloud 或在 `issue_comment` 事件上运行的自定义 GitHub Actions，请注意 Claude 可以代表你回复，这可能会触发这些工作流。在启用自动修复之前审查你的存储库的自动化，并考虑为可能部署基础设施或运行特权操作的 PR 注释的存储库禁用自动修复。
</Warning>

## 安全和隔离

每个云会话通过多个层与你的机器和其他会话分离：

* **隔离的虚拟机**：每个会话在隔离的、Anthropic 管理的 VM 中运行
* **网络访问控制**：网络访问默认受限，可以禁用。在禁用网络访问的情况下运行时，Claude Code 仍然可以与 Anthropic API 通信，这可能允许数据从 VM 中退出。
* **凭证保护**：敏感凭证（如 git 凭证或签名密钥）永远不会在沙箱内与 Claude Code 一起。身份验证通过使用作用域凭证的安全代理处理。
* **安全分析**：代码在隔离的 VM 内分析和修改，然后创建 PR

## 限制

在依赖云会话进行工作流之前，请考虑这些约束：

* **速率限制**：Claude Code on the web 与你账户内所有其他 Claude 和 Claude Code 使用共享速率限制。并行运行多个任务会按比例消耗更多速率限制。云 VM 没有单独的计算费用。
* **存储库身份验证**：你只能在认证到相同账户时将会话从网络移动到本地
* **平台限制**：存储库克隆和拉取请求创建需要 GitHub。自托管[GitHub Enterprise Server](/zh-CN/github-enterprise-server) 实例支持 Team 和 Enterprise 计划。GitLab、Bitbucket 和其他非 GitHub 存储库可以作为[本地捆绑](#send-local-repositories-without-github)发送到云会话，但会话无法将结果推送回远程

## 相关资源

* [Ultraplan](/zh-CN/ultraplan)：在云会话中起草计划并在浏览器中审查
* [Ultrareview](/zh-CN/ultrareview)：在云沙箱中运行深度多代理代码审查
* [Routines](/zh-CN/routines)：按计划、通过 API 调用或响应 GitHub 事件自动化工作
* [Hooks 配置](/zh-CN/hooks)：在会话生命周期事件处运行脚本
* [设置参考](/zh-CN/settings)：所有配置选项
* [安全](/zh-CN/security)：隔离保证和数据处理
* [数据使用](/zh-CN/data-usage)：Anthropic 从云会话保留的内容
