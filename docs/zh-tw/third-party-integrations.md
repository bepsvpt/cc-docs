> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 企業部署概述

> 了解 Claude Code 如何與各種第三方服務和基礎設施整合，以滿足企業部署需求。

本頁面提供可用部署選項的概述，並幫助您為組織選擇正確的配置。

## 提供商比較

<table>
  <thead>
    <tr>
      <th>功能</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>區域</td>
      <td>支援的[國家](https://www.anthropic.com/supported-countries)</td>
      <td>多個 AWS [區域](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>多個 GCP [區域](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>多個 Azure [區域](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>提示快取</td>
      <td>預設啟用</td>
      <td>預設啟用</td>
      <td>預設啟用</td>
      <td>預設啟用</td>
    </tr>

    <tr>
      <td>身份驗證</td>
      <td>API 金鑰</td>
      <td>API 金鑰或 AWS 認證</td>
      <td>GCP 認證</td>
      <td>API 金鑰或 Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>成本追蹤</td>
      <td>儀表板</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>企業功能</td>
      <td>團隊、使用情況監控</td>
      <td>IAM 政策、CloudTrail</td>
      <td>IAM 角色、Cloud Audit Logs</td>
      <td>RBAC 政策、Azure Monitor</td>
    </tr>
  </tbody>
</table>

## 雲端提供商

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/zh-TW/amazon-bedrock">
    透過 AWS 基礎設施使用 Claude 模型，支援 API 金鑰或基於 IAM 的身份驗證和 AWS 原生監控
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/zh-TW/google-vertex-ai">
    透過 Google Cloud Platform 存取 Claude 模型，具有企業級安全性和合規性
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/zh-TW/microsoft-foundry">
    透過 Azure 存取 Claude，支援 API 金鑰或 Microsoft Entra ID 身份驗證和 Azure 計費
  </Card>
</CardGroup>

## 企業基礎設施

<CardGroup cols={2}>
  <Card title="企業網路" icon="shield" href="/zh-TW/network-config">
    配置 Claude Code 以與組織的代理伺服器和 SSL/TLS 需求相容
  </Card>

  <Card title="LLM Gateway" icon="server" href="/zh-TW/llm-gateway">
    部署集中式模型存取，具有使用情況追蹤、預算編制和稽核日誌
  </Card>
</CardGroup>

## 配置概述

Claude Code 支援靈活的配置選項，允許您組合不同的提供商和基礎設施：

<Note>
  了解以下差異：

  * **企業代理**：用於路由流量的 HTTP/HTTPS 代理（透過 `HTTPS_PROXY` 或 `HTTP_PROXY` 設定）
  * **LLM Gateway**：處理身份驗證並提供提供商相容端點的服務（透過 `ANTHROPIC_BASE_URL`、`ANTHROPIC_BEDROCK_BASE_URL` 或 `ANTHROPIC_VERTEX_BASE_URL` 設定）

  兩種配置可以同時使用。
</Note>

### 使用 Bedrock 搭配企業代理

透過企業 HTTP/HTTPS 代理路由 Bedrock 流量：

```bash  theme={null}
# 啟用 Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# 配置企業代理
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### 使用 Bedrock 搭配 LLM Gateway

使用提供 Bedrock 相容端點的閘道服務：

```bash  theme={null}
# 啟用 Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# 配置 LLM 閘道
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # 如果閘道處理 AWS 身份驗證
```

### 使用 Foundry 搭配企業代理

透過企業 HTTP/HTTPS 代理路由 Azure 流量：

```bash  theme={null}
# 啟用 Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # 或省略以使用 Entra ID 身份驗證

# 配置企業代理
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### 使用 Foundry 搭配 LLM Gateway

使用提供 Azure 相容端點的閘道服務：

```bash  theme={null}
# 啟用 Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# 配置 LLM 閘道
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # 如果閘道處理 Azure 身份驗證
```

### 使用 Vertex AI 搭配企業代理

透過企業 HTTP/HTTPS 代理路由 Vertex AI 流量：

```bash  theme={null}
# 啟用 Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# 配置企業代理
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### 使用 Vertex AI 搭配 LLM Gateway

將 Google Vertex AI 模型與 LLM 閘道結合以進行集中式管理：

```bash  theme={null}
# 啟用 Vertex
export CLAUDE_CODE_USE_VERTEX=1

# 配置 LLM 閘道
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # 如果閘道處理 GCP 身份驗證
```

### 身份驗證配置

Claude Code 在需要時使用 `ANTHROPIC_AUTH_TOKEN` 作為 `Authorization` 標頭。`SKIP_AUTH` 標誌（`CLAUDE_CODE_SKIP_BEDROCK_AUTH`、`CLAUDE_CODE_SKIP_VERTEX_AUTH`）用於 LLM 閘道場景，其中閘道處理提供商身份驗證。

## 選擇正確的部署配置

選擇部署方法時，請考慮以下因素：

### 直接提供商存取

最適合以下組織：

* 希望最簡單的設定
* 已有 AWS 或 GCP 基礎設施
* 需要提供商原生監控和合規性

### 企業代理

最適合以下組織：

* 有現有的企業代理需求
* 需要流量監控和合規性
* 必須透過特定網路路徑路由所有流量

### LLM Gateway

最適合以下組織：

* 需要跨團隊的使用情況追蹤
* 希望在模型之間動態切換
* 需要自訂速率限制或預算
* 需要集中式身份驗證管理

## 除錯

除錯部署時：

* 使用 `claude /status` [斜線命令](/zh-TW/slash-commands)。此命令提供對任何應用的身份驗證、代理和 URL 設定的可觀測性。
* 設定環境變數 `export ANTHROPIC_LOG=debug` 以記錄請求。

## 組織的最佳實踐

### 1. 投資文件和記憶

我們強烈建議投資文件，以便 Claude Code 了解您的程式碼庫。組織可以在多個級別部署 CLAUDE.md 檔案：

* **組織範圍**：部署到系統目錄，如 `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS），用於公司範圍的標準
* **存放庫級別**：在存放庫根目錄中建立 `CLAUDE.md` 檔案，包含專案架構、建置命令和貢獻指南。將這些簽入原始碼控制，以便所有使用者受益

  [了解更多](/zh-TW/memory)。

### 2. 簡化部署

如果您有自訂開發環境，我們發現建立「一鍵」安裝 Claude Code 的方式是在組織中推動採用的關鍵。

### 3. 從引導式使用開始

鼓勵新使用者嘗試 Claude Code 進行程式碼庫問答，或在較小的錯誤修復或功能請求上使用。要求 Claude Code 制定計畫。檢查 Claude 的建議，如果偏離軌道，請提供反饋。隨著時間推移，當使用者更好地理解這種新範例時，他們將更有效地讓 Claude Code 更自主地運行。

### 4. 配置安全政策

安全團隊可以配置受管權限，以確定 Claude Code 允許和不允許執行的操作，這些操作無法被本地配置覆蓋。[了解更多](/zh-TW/security)。

### 5. 利用 MCP 進行整合

MCP 是為 Claude Code 提供更多資訊的絕佳方式，例如連接到票證管理系統或錯誤日誌。我們建議一個中央團隊配置 MCP 伺服器，並將 `.mcp.json` 配置簽入程式碼庫，以便所有使用者受益。[了解更多](/zh-TW/mcp)。

在 Anthropic，我們信任 Claude Code 為每個 Anthropic 程式碼庫的開發提供動力。我們希望您享受使用 Claude Code 就像我們一樣。

## 後續步驟

* [設定 Amazon Bedrock](/zh-TW/amazon-bedrock) 進行 AWS 原生部署
* [配置 Google Vertex AI](/zh-TW/google-vertex-ai) 進行 GCP 部署
* [設定 Microsoft Foundry](/zh-TW/microsoft-foundry) 進行 Azure 部署
* [配置企業網路](/zh-TW/network-config) 以滿足網路需求
* [部署 LLM Gateway](/zh-TW/llm-gateway) 進行企業管理
* [設定](/zh-TW/settings) 以了解配置選項和環境變數
