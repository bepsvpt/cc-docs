> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 企業網路設定

> 為企業環境設定 Claude Code，包括代理伺服器、自訂憑證授權單位 (CA) 和相互傳輸層安全性 (mTLS) 驗證。

Claude Code 透過環境變數支援各種企業網路和安全設定。這包括透過公司代理伺服器路由流量、信任自訂憑證授權單位 (CA)，以及使用相互傳輸層安全性 (mTLS) 憑證進行驗證以增強安全性。

<Note>
  本頁面顯示的所有環境變數也可以在 [`settings.json`](/zh-TW/settings) 中設定。
</Note>

## 代理設定

### 環境變數

Claude Code 遵守標準代理環境變數：

```bash theme={null}
# HTTPS 代理（建議）
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP 代理（如果 HTTPS 不可用）
export HTTP_PROXY=http://proxy.example.com:8080

# 略過特定請求的代理 - 空格分隔格式
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# 略過特定請求的代理 - 逗號分隔格式
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# 略過所有請求的代理
export NO_PROXY="*"
```

<Note>
  Claude Code 不支援 SOCKS 代理。
</Note>

### 基本驗證

如果您的代理需要基本驗證，請在代理 URL 中包含認證資訊：

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  避免在指令碼中硬編碼密碼。改用環境變數或安全認證儲存。
</Warning>

<Tip>
  對於需要進階驗證（NTLM、Kerberos 等）的代理，請考慮使用支援您驗證方法的 LLM Gateway 服務。
</Tip>

## CA 憑證存放區

根據預設，Claude Code 信任其捆綁的 Mozilla CA 憑證和您作業系統的憑證存放區。企業 TLS 檢查代理（例如 CrowdStrike Falcon 和 Zscaler）在其根憑證安裝在作業系統信任存放區中時無需額外設定即可運作。

<Note>
  系統 CA 存放區整合需要原生 Claude Code 二進位分發。在 Node.js 執行時上執行時，系統 CA 存放區不會自動合併。在這種情況下，設定 `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` 以信任企業根 CA。
</Note>

`CLAUDE_CODE_CERT_STORE` 接受以逗號分隔的來源清單。認可的值為 `bundled`（Claude Code 隨附的 Mozilla CA 集合）和 `system`（作業系統信任存放區）。預設值為 `bundled,system`。

若只信任捆綁的 Mozilla CA 集合：

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

若只信任作業系統憑證存放區：

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` 在 `settings.json` 中沒有專用的架構金鑰。透過 `~/.claude/settings.json` 中的 `env` 區塊或直接在程序環境中設定。
</Note>

## 自訂 CA 憑證

如果您的企業環境使用自訂 CA，請設定 Claude Code 以直接信任它：

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 驗證

對於需要用戶端憑證驗證的企業環境：

```bash theme={null}
# 用於驗證的用戶端憑證
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# 用戶端私密金鑰
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# 選用：加密私密金鑰的密碼
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## 網路存取需求

Claude Code 需要存取以下 URL：

* `api.anthropic.com`：Claude API 端點
* `claude.ai`：claude.ai 帳戶驗證
* `platform.claude.com`：Anthropic Console 帳戶驗證

確保這些 URL 在您的代理設定和防火牆規則中被列入允許清單。這在容器化或受限網路環境中使用 Claude Code 時特別重要。

使用 [Bedrock](/zh-TW/amazon-bedrock)、[Vertex AI](/zh-TW/google-vertex-ai) 或 [Foundry](/zh-TW/microsoft-foundry) 時，模型流量會傳送到您的提供者，而不是 `api.anthropic.com`。WebFetch 工具仍會呼叫 `api.anthropic.com` 進行其[網域安全檢查](/zh-TW/data-usage#webfetch-domain-safety-check)，除非您在[設定](/zh-TW/settings)中設定 `skipWebFetchPreflight: true`。

原生安裝程式和更新檢查也需要以下 URL。請將兩者都列入允許清單，因為執行較舊 Claude Code 版本的用戶端從 `storage.googleapis.com` 擷取。如果您透過 npm 安裝 Claude Code 或管理自己的二進位分發，終端使用者可能不需要存取：

* `downloads.claude.ai`：Claude Code 二進位檔、自動更新程式、版本指標、資訊清單、安裝指令碼、簽署金鑰和外掛程式可執行檔的下載主機
* `storage.googleapis.com`：較舊用戶端使用的舊版下載主機

[Chrome 整合](/zh-TW/chrome)透過 WebSocket 橋接器連線到瀏覽器擴充功能。如果您在 Chrome 中使用 Claude，請為出站 WebSocket 連線列入允許清單 `bridge.claudeusercontent.com`。

[Claude Code on the web](/zh-TW/claude-code-on-the-web) 和 [Code Review](/zh-TW/code-review) 從 Anthropic 管理的基礎設施連線到您的儲存庫。如果您的 GitHub Enterprise Cloud 組織按 IP 位址限制存取，請啟用[已安裝 GitHub Apps 的 IP 允許清單繼承](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps)。Claude GitHub App 會註冊其 IP 範圍，因此啟用此設定可允許存取而無需手動設定。若要[手動將範圍新增到允許清單](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)，或設定其他防火牆，請參閱 [Anthropic API IP 位址](https://platform.claude.com/docs/en/api/ip-addresses)。

對於防火牆後的自託管 [GitHub Enterprise Server](/zh-TW/github-enterprise-server) 執行個體，請將相同的 [Anthropic API IP 位址](https://platform.claude.com/docs/en/api/ip-addresses) 列入允許清單，以便 Anthropic 基礎設施可以連線到您的 GHES 主機以複製儲存庫並發佈審查評論。

## 其他資源

* [Claude Code 設定](/zh-TW/settings)
* [環境變數參考](/zh-TW/env-vars)
* [疑難排解指南](/zh-TW/troubleshooting)
