> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 企业网络配置

> 为企业环境配置 Claude Code，支持代理服务器、自定义证书颁发机构 (CA) 和相互传输层安全 (mTLS) 身份验证。

Claude Code 通过环境变量支持各种企业网络和安全配置。这包括通过公司代理服务器路由流量、信任自定义证书颁发机构 (CA)，以及使用相互传输层安全 (mTLS) 证书进行身份验证以增强安全性。

<Note>
  本页面显示的所有环境变量也可以在 [`settings.json`](/zh-CN/settings) 中配置。
</Note>

## 代理配置

### 环境变量

Claude Code 遵守标准代理环境变量：

```bash theme={null}
# HTTPS 代理（推荐）
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP 代理（如果 HTTPS 不可用）
export HTTP_PROXY=http://proxy.example.com:8080

# 绕过特定请求的代理 - 空格分隔格式
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# 绕过特定请求的代理 - 逗号分隔格式
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# 绕过所有请求的代理
export NO_PROXY="*"
```

<Note>
  Claude Code 不支持 SOCKS 代理。
</Note>

### 基本身份验证

如果您的代理需要基本身份验证，请在代理 URL 中包含凭证：

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  避免在脚本中硬编码密码。改用环境变量或安全凭证存储。
</Warning>

<Tip>
  对于需要高级身份验证（NTLM、Kerberos 等）的代理，请考虑使用支持您的身份验证方法的 LLM 网关服务。
</Tip>

## CA 证书存储

默认情况下，Claude Code 信任其捆绑的 Mozilla CA 证书和您的操作系统的证书存储。企业 TLS 检查代理（如 CrowdStrike Falcon 和 Zscaler）在其根证书安装在操作系统信任存储中时无需额外配置即可工作。

<Note>
  系统 CA 存储集成需要本机 Claude Code 二进制分发。在 Node.js 运行时上运行时，系统 CA 存储不会自动合并。在这种情况下，设置 `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` 以信任企业根 CA。
</Note>

`CLAUDE_CODE_CERT_STORE` 接受逗号分隔的源列表。识别的值为 `bundled`（Claude Code 附带的 Mozilla CA 集）和 `system`（操作系统信任存储）。默认值为 `bundled,system`。

仅信任捆绑的 Mozilla CA 集：

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

仅信任操作系统证书存储：

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` 没有专用的 `settings.json` 架构密钥。通过 `~/.claude/settings.json` 中的 `env` 块或直接在进程环境中设置它。
</Note>

## 自定义 CA 证书

如果您的企业环境使用自定义 CA，请配置 Claude Code 以直接信任它：

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 身份验证

对于需要客户端证书身份验证的企业环境：

```bash theme={null}
# 用于身份验证的客户端证书
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# 客户端私钥
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# 可选：加密私钥的密码短语
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## 网络访问要求

Claude Code 需要访问以下 URL。在您的代理配置和防火墙规则中将这些 URL 列入白名单，特别是在容器化或受限网络环境中。

| URL                            | 用途                                                       |
| ------------------------------ | -------------------------------------------------------- |
| `api.anthropic.com`            | Claude API 请求                                            |
| `claude.ai`                    | claude.ai 账户身份验证                                         |
| `platform.claude.com`          | Anthropic 控制台账户身份验证                                      |
| `downloads.claude.ai`          | 插件可执行文件下载；原生安装程序和原生自动更新程序                                |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}2.1.116 版本之前的原生安装程序和原生自动更新程序 |
| `bridge.claudeusercontent.com` | [Chrome 中的 Claude](/zh-CN/chrome) 扩展 WebSocket 桥接        |

如果您通过 npm 安装 Claude Code 或管理自己的二进制分发，最终用户可能不需要访问 `downloads.claude.ai` 或 `storage.googleapis.com`。

使用 [Amazon Bedrock](/zh-CN/amazon-bedrock)、[Google Vertex AI](/zh-CN/google-vertex-ai) 或 [Microsoft Foundry](/zh-CN/microsoft-foundry) 时，模型流量和身份验证会转到您的提供商，而不是 `api.anthropic.com`、`claude.ai` 或 `platform.claude.com`。WebFetch 工具仍会调用 `api.anthropic.com` 进行其 [域名安全检查](/zh-CN/data-usage#webfetch-domain-safety-check)，除非您在 [settings](/zh-CN/settings) 中设置 `skipWebFetchPreflight: true`。

[Claude Code on the web](/zh-CN/claude-code-on-the-web) 和 [Code Review](/zh-CN/code-review) 从 Anthropic 管理的基础设施连接到您的存储库。如果您的 GitHub Enterprise Cloud 组织按 IP 地址限制访问，请启用 [已安装 GitHub Apps 的 IP 允许列表继承](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps)。Claude GitHub App 注册了其 IP 范围，因此启用此设置允许访问而无需手动配置。要 [手动将范围添加到您的允许列表](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)，或配置其他防火墙，请参阅 [Anthropic API IP 地址](https://platform.claude.com/docs/en/api/ip-addresses)。

对于防火墙后的自托管 [GitHub Enterprise Server](/zh-CN/github-enterprise-server) 实例，请将相同的 [Anthropic API IP 地址](https://platform.claude.com/docs/en/api/ip-addresses) 列入白名单，以便 Anthropic 基础设施可以访问您的 GHES 主机来克隆存储库和发布审查评论。

## 其他资源

* [Claude Code 设置](/zh-CN/settings)
* [环境变量参考](/zh-CN/env-vars)
* [故障排除指南](/zh-CN/troubleshooting)
