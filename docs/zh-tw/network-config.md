> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 企業網路配置

> 為企業環境配置 Claude Code，支援代理伺服器、自訂憑證授權單位 (CA) 和相互傳輸層安全性 (mTLS) 驗證。

Claude Code 透過環境變數支援各種企業網路和安全配置。這包括透過公司代理伺服器路由流量、信任自訂憑證授權單位 (CA)，以及使用相互傳輸層安全性 (mTLS) 憑證進行驗證以增強安全性。

<Note>
  本頁面顯示的所有環境變數也可以在 [`settings.json`](/zh-TW/settings) 中配置。
</Note>

## 代理配置

### 環境變數

Claude Code 遵守標準代理環境變數：

```bash  theme={null}
# HTTPS 代理（建議）
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP 代理（如果 HTTPS 不可用）
export HTTP_PROXY=http://proxy.example.com:8080

# 繞過特定請求的代理 - 空格分隔格式
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# 繞過特定請求的代理 - 逗號分隔格式
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# 繞過所有請求的代理
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
  對於需要進階驗證（NTLM、Kerberos 等）的代理，請考慮使用支援您的驗證方法的 LLM Gateway 服務。
</Tip>

## 自訂 CA 憑證

如果您的企業環境使用自訂 CA 進行 HTTPS 連線（無論是透過代理還是直接 API 存取），請配置 Claude Code 以信任它們：

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
* `claude.ai`：claude.ai 帳戶的驗證
* `platform.claude.com`：Anthropic Console 帳戶的驗證

確保這些 URL 在您的代理配置和防火牆規則中被列入白名單。這在容器化或受限網路環境中使用 Claude Code 時特別重要。

## 其他資源

* [Claude Code 設定](/zh-TW/settings)
* [環境變數參考](/zh-TW/settings#environment-variables)
* [疑難排解指南](/zh-TW/troubleshooting)
