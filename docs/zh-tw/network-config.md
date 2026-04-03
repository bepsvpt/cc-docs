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

```bash  theme={null}
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

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  避免在指令碼中硬編碼密碼。改用環境變數或安全認證儲存。
</Warning>

<Tip>
  對於需要進階驗證（NTLM、Kerberos 等）的代理，請考慮使用支援您驗證方法的 LLM Gateway 服務。
</Tip>

## 自訂 CA 憑證

如果您的企業環境使用自訂 CA 進行 HTTPS 連線（無論是透過代理還是直接 API 存取），請設定 Claude Code 以信任它們：

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 驗證

對於需要用戶端憑證驗證的企業環境：

```bash  theme={null}
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

原生安裝程式和更新檢查也需要以下 URL。請將兩者都列入允許清單，因為安裝程式和自動更新程式從 `storage.googleapis.com` 擷取，而外掛程式下載使用 `downloads.claude.ai`。如果您透過 npm 安裝 Claude Code 或管理自己的二進位分發，終端使用者可能不需要存取：

* `storage.googleapis.com`：Claude Code 二進位檔和自動更新程式的下載儲存庫
* `downloads.claude.ai`：CDN 託管安裝指令碼、版本指標、資訊清單、簽署金鑰和外掛程式可執行檔

[Claude Code on the web](/zh-TW/claude-code-on-the-web) 和 [Code Review](/zh-TW/code-review) 從 Anthropic 管理的基礎設施連線到您的儲存庫。如果您的 GitHub Enterprise Cloud 組織按 IP 位址限制存取，請啟用[已安裝 GitHub Apps 的 IP 允許清單繼承](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps)。Claude GitHub App 會註冊其 IP 範圍，因此啟用此設定可允許存取而無需手動設定。若要[手動將範圍新增到允許清單](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)，或設定其他防火牆，請參閱 [Anthropic API IP 位址](https://platform.claude.com/docs/en/api/ip-addresses)。

對於防火牆後的自託管 [GitHub Enterprise Server](/zh-TW/github-enterprise-server) 執行個體，請將相同的 [Anthropic API IP 位址](https://platform.claude.com/docs/en/api/ip-addresses) 列入允許清單，以便 Anthropic 基礎設施可以連線到您的 GHES 主機以複製儲存庫並發佈審查評論。

## 其他資源

* [Claude Code 設定](/zh-TW/settings)
* [環境變數參考](/zh-TW/env-vars)
* [疑難排解指南](/zh-TW/troubleshooting)
