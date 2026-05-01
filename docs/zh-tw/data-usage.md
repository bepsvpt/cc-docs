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

### 使用 `/feedback` 命令的回饋

如果您選擇使用 `/feedback` 命令向我們發送有關 Claude Code 的回饋，我們可能會使用您的回饋來改進我們的產品和服務。透過 `/feedback` 共享的文字記錄會保留 5 年。

### 工作階段品質調查

當您在 Claude Code 中看到「Claude 在此工作階段中表現如何？」提示時，回應此調查（包括選擇「關閉」），只會記錄您的評分。我們不會作為此評分提示本身的一部分收集或儲存任何對話文字記錄、輸入、輸出或其他工作階段資料。與豎起大拇指/向下大拇指回饋或 `/feedback` 報告不同，此工作階段品質調查是一個簡單的產品滿意度指標。

在評分提示之後，您可能會看到一個單獨的後續提問「Anthropic 可以查看您的工作階段文字記錄以幫助我們改進 Claude Code 嗎？」。這是一個與評分不同的可選第二步：

* **是**：將您的對話文字記錄、任何子代理文字記錄和磁碟中的原始工作階段日誌檔案上傳至 Anthropic。已知的 API 金鑰和權杖模式在上傳前會被編輯。原始程式碼、檔案內容和其他對話內容會按原樣上傳。共享的文字記錄會保留最多 6 個月。
* **否**：拒絕而不發送任何內容
* **不再詢問**：拒絕並停止此後續提問在未來工作階段中出現

除非您明確選擇**是**，否則不會上傳任何內容。具有[零資料保留](/zh-TW/zero-data-retention)的組織，或組織政策停用產品回饋的組織，永遠不會看到此後續提問。您對此調查的回應（包括評分提示後提交的工作階段文字記錄）不會影響您的資料訓練偏好設定，也不能用於訓練我們的 AI 模型。

若要停用這些調查，請設定 `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`。當設定 `DISABLE_TELEMETRY` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 時，調查也會停用。若要控制頻率而不是停用，請在您的設定檔中設定 [`feedbackSurveyRate`](/zh-TW/settings#available-settings) 為 `0` 到 `1` 之間的機率。

### 資料保留

Anthropic 根據您的帳戶類型和偏好設定保留 Claude Code 資料。

**消費者使用者（免費、Pro 和 Max 方案）**：

* 允許資料用於模型改進的使用者：5 年保留期，以支持模型開發和安全改進
* 不允許資料用於模型改進的使用者：30 天保留期
* 隱私設定可以隨時在 [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) 變更。

**商業使用者（Team、Enterprise 和 API）**：

* 標準：30 天保留期
* [零資料保留](/zh-TW/zero-data-retention)：適用於 Claude for Enterprise 上的 Claude Code。ZDR 按組織啟用；每個新組織必須由您的帳戶團隊單獨啟用 ZDR
* 本機快取：Claude Code 用戶端在 `~/.claude/projects/` 下以純文字形式本機儲存工作階段文字記錄，預設為 30 天，以啟用工作階段繼續。使用 `cleanupPeriodDays` 調整期間。請參閱[應用程式資料](/zh-TW/claude-directory#application-data)以了解儲存的內容以及如何清除。

您可以隨時刪除網路上的個別 Claude Code 工作階段。刪除工作階段會永久移除工作階段的事件資料。如需有關如何刪除工作階段的說明，請參閱[刪除工作階段](/zh-TW/claude-code-on-the-web#delete-sessions)。

在我們的[隱私中心](https://privacy.anthropic.com/)了解更多有關資料保留實踐的資訊。

如需完整詳細資訊，請查閱我們的[商業服務條款](https://www.anthropic.com/legal/commercial-terms)（適用於 Team、Enterprise 和 API 使用者）或[消費者條款](https://www.anthropic.com/legal/consumer-terms)（適用於免費、Pro 和 Max 使用者）和[隱私政策](https://www.anthropic.com/legal/privacy)。

## 資料存取

對於所有第一方使用者，您可以了解更多有關為[本機 Claude Code](#local-claude-code-data-flow-and-dependencies) 和[遠端 Claude Code](#cloud-execution-data-flow-and-dependencies) 記錄的資料。[遠端控制](/zh-TW/remote-control)工作階段遵循本機資料流，因為所有執行都在您的機器上進行。請注意，對於遠端 Claude Code，Claude 會存取您啟動 Claude Code 工作階段的儲存庫。Claude 不會存取您已連接但尚未在其中啟動工作階段的儲存庫。

## 本機 Claude Code：資料流和相依性

下圖顯示 Claude Code 在安裝和正常操作期間如何連接到外部服務。實線表示必需的連接，而虛線表示可選或使用者啟動的資料流。

<img src="https://mintcdn.com/claude-code/YcBW2H7CArGcduPb/images/claude-code-data-flow.svg?fit=max&auto=format&n=YcBW2H7CArGcduPb&q=85&s=b600a89f84fc86f9ff7be00a466c0635" alt="顯示 Claude Code 外部連接的圖表：安裝/更新連接到發佈伺服器，使用者請求連接到 Anthropic 服務，包括 Console 驗證、public-api，以及可選的 Statsig、Sentry 和錯誤報告" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code 在本機執行。為了與 LLM 互動，Claude Code 透過網路發送資料。此資料包括所有使用者提示和模型輸出，在傳輸中透過 TLS 1.2+ 加密。Claude Code 與大多數流行的 VPN 和 LLM 代理相容。

靜止時的加密取決於您的模型提供者：

| 提供者                    | 靜止時加密                                                                 |
| ---------------------- | --------------------------------------------------------------------- |
| Anthropic API          | 基礎設施層級磁碟加密 (AES-256)。啟用[零資料保留](/zh-TW/zero-data-retention)以避免伺服器端持久化。 |
| Amazon Bedrock         | AES-256 搭配 AWS 管理的金鑰。客戶管理的金鑰可透過 AWS KMS 取得。                           |
| Google Cloud Vertex AI | Google 管理的加密金鑰。CMEK 可用。                                               |
| Microsoft Foundry      | 請求路由到 Anthropic 基礎設施，具有 AES-256 磁碟加密。                                 |

Claude Code 建立在 Anthropic 的 API 上。有關 API 安全控制的詳細資訊，包括 API 記錄程序，請參閱 [Anthropic 信任中心](https://trust.anthropic.com)中的合規性文件。

### 雲端執行：資料流和相依性

使用[網路上的 Claude Code](/zh-TW/claude-code-on-the-web)時，工作階段在 Anthropic 管理的虛擬機器中執行，而不是在本機執行。在雲端環境中：

* \*\*程式碼和資料儲存：\*\*您的儲存庫被複製到隔離的 VM。程式碼和工作階段資料受您帳戶類型的保留和使用政策約束（請參閱上面的資料保留部分）
* \*\*認證：\*\*GitHub 驗證透過安全代理進行；您的 GitHub 認證永遠不會進入沙箱
* \*\*網路流量：\*\*所有出站流量都透過安全代理進行，用於稽核記錄和濫用防止
* \*\*工作階段資料：\*\*提示、程式碼變更和輸出遵循與本機 Claude Code 使用相同的資料政策

有關雲端執行的安全詳細資訊，請參閱[安全性](/zh-TW/security#cloud-execution-security)。

## 遙測服務

Claude Code 從使用者的機器連接到 Statsig 服務，以記錄延遲、可靠性和使用模式等操作指標。此記錄不包括任何程式碼或檔案路徑。資料在傳輸中使用 TLS 加密，在靜止時使用 256 位 AES 加密。在 [Statsig 安全文件](https://www.statsig.com/trust/security)中閱讀更多資訊。若要選擇退出 Statsig 遙測，請設定 `DISABLE_TELEMETRY` 環境變數。

Claude Code 從使用者的機器連接到 Sentry 進行操作錯誤記錄。資料在傳輸中使用 TLS 加密，在靜止時使用 256 位 AES 加密。在 [Sentry 安全文件](https://sentry.io/security/)中閱讀更多資訊。若要選擇退出錯誤記錄，請設定 `DISABLE_ERROR_REPORTING` 環境變數。

當使用者執行 `/feedback` 命令時，他們的完整對話歷史記錄（包括程式碼）的副本會發送到 Anthropic。資料在傳輸中使用 TLS 加密。可選地，在公開儲存庫中建立 GitHub 問題。若要選擇退出，請設定 `DISABLE_FEEDBACK_COMMAND` 環境變數為 `1`。

## 按 API 提供者的預設行為

根據預設，當使用 Bedrock、Vertex 或 Foundry 時，錯誤報告、遙測和錯誤報告會停用。工作階段品質調查和 WebFetch 網域安全檢查是例外，無論提供者為何都會執行。您可以透過設定 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 一次選擇退出所有非必要流量，包括調查。此變數不會影響 WebFetch 檢查，該檢查有其自己的選擇退出。以下是完整的預設行為：

| 服務                             | Claude API                                                            | Vertex API                                                            | Bedrock API                                                           | Foundry API                                                           |
| ------------------------------ | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Statsig（指標）**                | 預設開啟。<br />`DISABLE_TELEMETRY=1` 以停用。                                 | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。                            | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。                           | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。                           |
| **Sentry（錯誤）**                 | 預設開啟。<br />`DISABLE_ERROR_REPORTING=1` 以停用。                           | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。                            | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。                           | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。                           |
| **Claude API（`/feedback` 報告）** | 預設開啟。<br />`DISABLE_FEEDBACK_COMMAND=1` 以停用。                          | 預設關閉。<br />`CLAUDE_CODE_USE_VERTEX` 必須為 1。                            | 預設關閉。<br />`CLAUDE_CODE_USE_BEDROCK` 必須為 1。                           | 預設關閉。<br />`CLAUDE_CODE_USE_FOUNDRY` 必須為 1。                           |
| **工作階段品質調查**                   | 預設開啟。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 以停用。               | 預設開啟。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 以停用。               | 預設開啟。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 以停用。               | 預設開啟。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 以停用。               |
| **WebFetch 網域安全檢查**            | 預設開啟。<br />[設定](/zh-TW/settings)中的 `skipWebFetchPreflight: true` 以停用。 | 預設開啟。<br />[設定](/zh-TW/settings)中的 `skipWebFetchPreflight: true` 以停用。 | 預設開啟。<br />[設定](/zh-TW/settings)中的 `skipWebFetchPreflight: true` 以停用。 | 預設開啟。<br />[設定](/zh-TW/settings)中的 `skipWebFetchPreflight: true` 以停用。 |

所有環境變數都可以簽入 `settings.json`（請參閱[設定參考](/zh-TW/settings)）。

自 v2.1.126 起，當主機平台設定 `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` 時，Statsig 指標在 Vertex、Bedrock 和 Foundry 上預設為開啟，並遵循標準 `DISABLE_TELEMETRY` 選擇退出。Sentry 錯誤報告和 `/feedback` 報告在這些提供者上仍預設為關閉。

### WebFetch 網域安全檢查

在擷取 URL 之前，WebFetch 工具會將請求的主機名稱發送到 `api.anthropic.com`，以根據 Anthropic 維護的安全封鎖清單進行檢查。只會發送主機名稱，不會發送完整 URL、路徑或頁面內容。結果按主機名稱快取五分鐘。

無論您使用哪個模型提供者，此檢查都會執行，並且不受 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 影響。如果您的網路封鎖 `api.anthropic.com`，WebFetch 請求會失敗，直到您允許清單該網域或在[設定](/zh-TW/settings)中設定 `skipWebFetchPreflight: true`。停用檢查意味著 WebFetch 會嘗試擷取任何 URL，而不查詢封鎖清單，因此如果您需要限制 Claude 可以存取的網域，請將其與 [`WebFetch` 權限規則](/zh-TW/permissions#webfetch)結合。
