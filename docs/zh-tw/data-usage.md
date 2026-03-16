> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 資料使用

> 了解 Anthropic 對 Claude 資料使用政策

## 資料政策

### 資料訓練政策

**消費者使用者（免費、Pro 和 Max 方案）**：
我們讓您可以選擇是否允許您的資料用於改進未來的 Claude 模型。當此設定開啟時，我們將使用來自免費、Pro 和 Max 帳戶的資料來訓練新模型（包括當您從這些帳戶使用 Claude Code 時）。

**商業使用者**：（Team 和 Enterprise 方案、API、第三方平台和 Claude Gov）維持現有政策：除非客戶選擇向我們提供資料以改進模型（例如，[開發者合作夥伴計畫](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)），否則 Anthropic 不會在商業條款下使用發送至 Claude Code 的程式碼或提示來訓練生成模型。

### 開發者合作夥伴計畫

如果您明確選擇加入向我們提供訓練材料的方法，例如透過[開發者合作夥伴計畫](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)，我們可能會使用所提供的材料來訓練我們的模型。組織管理員可以明確選擇為其組織加入開發者合作夥伴計畫。請注意，此計畫僅適用於 Anthropic 第一方 API，不適用於 Bedrock 或 Vertex 使用者。

### 使用 `/bug` 命令的回饋

如果您選擇使用 `/bug` 命令向我們發送有關 Claude Code 的回饋，我們可能會使用您的回饋來改進我們的產品和服務。透過 `/bug` 共享的文字記錄會保留 5 年。

### 工作階段品質調查

當您在 Claude Code 中看到「Claude 在此工作階段中表現如何？」提示時，回應此調查（包括選擇「關閉」），只會記錄您的數字評分（1、2、3 或關閉）。我們不會作為此調查的一部分收集或儲存任何對話文字記錄、輸入、輸出或其他工作階段資料。與豎起大拇指/向下大拇指回饋或 `/bug` 報告不同，此工作階段品質調查是一個簡單的產品滿意度指標。您對此調查的回應不會影響您的資料訓練偏好設定，也不能用於訓練我們的 AI 模型。

若要停用這些調查，請設定 `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`。使用第三方提供者（Bedrock、Vertex、Foundry）或停用遙測時，調查也會自動停用。

### 資料保留

Anthropic 根據您的帳戶類型和偏好設定保留 Claude Code 資料。

**消費者使用者（免費、Pro 和 Max 方案）**：

* 允許資料用於模型改進的使用者：5 年保留期，以支持模型開發和安全改進
* 不允許資料用於模型改進的使用者：30 天保留期
* 隱私設定可以隨時在 [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) 變更。

**商業使用者（Team、Enterprise 和 API）**：

* 標準：30 天保留期
* [零資料保留](/zh-TW/zero-data-retention)：適用於 Claude for Enterprise 上的 Claude Code。ZDR 按組織啟用；每個新組織必須由您的帳戶團隊單獨啟用 ZDR
* 本機快取：Claude Code 用戶端可能會在本機儲存工作階段長達 30 天，以啟用工作階段繼續（可配置）

您可以隨時刪除網路上的個別 Claude Code 工作階段。刪除工作階段會永久移除工作階段的事件資料。如需有關如何刪除工作階段的說明，請參閱[管理工作階段](/zh-TW/claude-code-on-the-web#managing-sessions)。

在我們的[隱私中心](https://privacy.anthropic.com/)了解更多有關資料保留實踐的資訊。

如需完整詳細資訊，請查閱我們的[商業服務條款](https://www.anthropic.com/legal/commercial-terms)（適用於 Team、Enterprise 和 API 使用者）或[消費者條款](https://www.anthropic.com/legal/consumer-terms)（適用於免費、Pro 和 Max 使用者）和[隱私政策](https://www.anthropic.com/legal/privacy)。

## 資料存取

對於所有第一方使用者，您可以了解更多有關為[本機 Claude Code](#local-claude-code-data-flow-and-dependencies) 和[遠端 Claude Code](#cloud-execution-data-flow-and-dependencies) 記錄的資料。[遠端控制](/zh-TW/remote-control)工作階段遵循本機資料流，因為所有執行都在您的機器上進行。請注意，對於遠端 Claude Code，Claude 會存取您啟動 Claude Code 工作階段的儲存庫。Claude 不會存取您已連接但尚未在其中啟動工作階段的儲存庫。

## 本機 Claude Code：資料流和相依性

下圖顯示 Claude Code 在安裝和正常操作期間如何連接到外部服務。實線表示必需的連接，而虛線表示可選或使用者啟動的資料流。

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/claude-code-data-flow.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=b3f71c69d743bff63343207dfb7ad6ce" alt="顯示 Claude Code 外部連接的圖表：安裝/更新連接到 NPM，使用者請求連接到 Anthropic 服務，包括 Console 驗證、public-api，以及可選的 Statsig、Sentry 和錯誤報告" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code 從 [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code) 安裝。Claude Code 在本機執行。為了與 LLM 互動，Claude Code 透過網路發送資料。此資料包括所有使用者提示和模型輸出。資料在傳輸中透過 TLS 加密，在靜止時未加密。Claude Code 與大多數流行的 VPN 和 LLM 代理相容。

Claude Code 建立在 Anthropic 的 API 上。有關我們 API 的安全控制詳細資訊，包括我們的 API 記錄程序，請參閱 [Anthropic 信任中心](https://trust.anthropic.com)中提供的合規性文件。

### 雲端執行：資料流和相依性

使用[網路上的 Claude Code](/zh-TW/claude-code-on-the-web) 時，工作階段在 Anthropic 管理的虛擬機器中執行，而不是在本機執行。在雲端環境中：

* \*\*程式碼和資料儲存：\*\*您的儲存庫被複製到隔離的 VM。程式碼和工作階段資料受您帳戶類型的保留和使用政策約束（請參閱上面的資料保留部分）
* \*\*認證：\*\*GitHub 驗證透過安全代理進行；您的 GitHub 認證永遠不會進入沙箱
* \*\*網路流量：\*\*所有出站流量都透過安全代理進行，用於稽核記錄和濫用防止
* \*\*工作階段資料：\*\*提示、程式碼變更和輸出遵循與本機 Claude Code 使用相同的資料政策

有關雲端執行的安全詳細資訊，請參閱[安全性](/zh-TW/security#cloud-execution-security)。

## 遙測服務

Claude Code 從使用者的機器連接到 Statsig 服務，以記錄延遲、可靠性和使用模式等操作指標。此記錄不包括任何程式碼或檔案路徑。資料在傳輸中使用 TLS 加密，在靜止時使用 256 位 AES 加密。在 [Statsig 安全文件](https://www.statsig.com/trust/security)中閱讀更多資訊。若要選擇退出 Statsig 遙測，請設定 `DISABLE_TELEMETRY` 環境變數。

Claude Code 從使用者的機器連接到 Sentry 進行操作錯誤記錄。資料在傳輸中使用 TLS 加密，在靜止時使用 256 位 AES 加密。在 [Sentry 安全文件](https://sentry.io/security/)中閱讀更多資訊。若要選擇退出錯誤記錄，請設定 `DISABLE_ERROR_REPORTING` 環境變數。

當使用者執行 `/bug` 命令時，他們的完整對話歷史記錄（包括程式碼）的副本會發送到 Anthropic。資料在傳輸中和靜止時加密。可選地，在我們的公開儲存庫中建立 Github 問題。若要選擇退出錯誤報告，請設定 `DISABLE_BUG_COMMAND` 環境變數。

## 按 API 提供者的預設行為

根據預設，當使用 Bedrock、Vertex 或 Foundry 時，我們會停用所有非必要流量（包括錯誤報告、遙測、錯誤報告功能和工作階段品質調查）。您也可以透過設定 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 環境變數一次選擇退出所有這些。以下是完整的預設行為：

| 服務                        | Claude API                                              | Vertex API                                 | Bedrock API                                 | Foundry API                                 |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------ | ------------------------------------------- | ------------------------------------------- |
| **Statsig（指標）**           | 預設開啟。<br />`DISABLE_TELEMETRY=1` 以停用。                   | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。 |
| **Sentry（錯誤）**            | 預設開啟。<br />`DISABLE_ERROR_REPORTING=1` 以停用。             | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。 |
| **Claude API（`/bug` 報告）** | 預設開啟。<br />`DISABLE_BUG_COMMAND=1` 以停用。                 | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。 |
| **工作階段品質調查**              | 預設開啟。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 以停用。 | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。 | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。 |

所有環境變數都可以簽入 `settings.json`（[閱讀更多](/zh-TW/settings)）。
