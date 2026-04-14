> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用快速模式加快回應速度

> 在 Claude Code 中切換快速模式，以獲得更快的 Opus 4.6 回應。

<Note>
  快速模式處於[研究預覽](#research-preview)階段。該功能、定價和可用性可能會根據反饋而改變。
</Note>

快速模式是 Claude Opus 4.6 的高速配置，使模型速度提升 2.5 倍，但每個 token 的成本更高。當您需要速度進行互動式工作（如快速迭代或實時調試）時，使用 `/fast` 切換開啟，當成本比延遲更重要時，切換關閉。

快速模式不是不同的模型。它使用相同的 Opus 4.6，但採用不同的 API 配置，優先考慮速度而非成本效率。您獲得相同的品質和功能，只是回應速度更快。

<Note>
  快速模式需要 Claude Code v2.1.36 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

需要了解的事項：

* 使用 `/fast` 在 Claude Code CLI 中切換快速模式。也可在 Claude Code VS Code 擴充功能中透過 `/fast` 使用。
* Opus 4.6 快速模式定價起價為 \$30/150 MTok。快速模式在 2 月 16 日太平洋時間 11:59pm 之前以 50% 折扣提供給所有方案。
* 適用於訂閱方案（Pro/Max/Team/Enterprise）上的所有 Claude Code 使用者和 Claude Console。
* 對於訂閱方案（Pro/Max/Team/Enterprise）上的 Claude Code 使用者，快速模式僅透過額外使用提供，不包含在訂閱速率限制中。

本頁涵蓋如何[切換快速模式](#toggle-fast-mode)、其[成本權衡](#understand-the-cost-tradeoff)、[何時使用](#decide-when-to-use-fast-mode)、[要求](#requirements)、[每個工作階段選擇加入](#require-per-session-opt-in)和[速率限制行為](#handle-rate-limits)。

## 切換快速模式

透過以下任一方式切換快速模式：

* 輸入 `/fast` 並按 Tab 鍵切換開啟或關閉
* 在您的[使用者設定檔案](/zh-TW/settings)中設定 `"fastMode": true`

預設情況下，快速模式在工作階段之間保持。管理員可以配置快速模式在每個工作階段重設。詳見[要求每個工作階段選擇加入](#require-per-session-opt-in)。

為了獲得最佳成本效率，在工作階段開始時啟用快速模式，而不是在對話中途切換。詳見[了解成本權衡](#understand-the-cost-tradeoff)。

當您啟用快速模式時：

* 如果您使用不同的模型，Claude Code 會自動切換到 Opus 4.6
* 您會看到確認訊息："Fast mode ON"
* 快速模式啟用時，提示旁會出現一個小的 `↯` 圖示
* 隨時再次執行 `/fast` 以檢查快速模式是否開啟或關閉

當您再次使用 `/fast` 關閉快速模式時，您仍保持在 Opus 4.6 上。模型不會還原到您之前的模型。要切換到不同的模型，請使用 `/model`。

## 了解成本權衡

快速模式的每個 token 定價高於標準 Opus 4.6：

| 模式                       | 輸入 (MTok) | 輸出 (MTok) |
| ------------------------ | --------- | --------- |
| Opus 4.6 上的快速模式 (\<200K) | \$30      | \$150     |
| Opus 4.6 上的快速模式 (>200K)  | \$60      | \$225     |

快速模式與 1M token 擴展上下文視窗相容。

當您在對話中途切換到快速模式時，您需要為整個對話上下文支付完整的快速模式未快取輸入 token 價格。這比從一開始就啟用快速模式的成本更高。

## 決定何時使用快速模式

快速模式最適合用於回應延遲比成本更重要的互動式工作：

* 快速迭代程式碼變更
* 實時調試工作階段
* 時間敏感的工作，有緊迫的截止日期

標準模式更適合：

* 速度不那麼重要的長期自主任務
* 批次處理或 CI/CD 管道
* 成本敏感的工作負載

### 快速模式與努力等級

快速模式和努力等級都會影響回應速度，但方式不同：

| 設定          | 效果                        |
| ----------- | ------------------------- |
| **快速模式**    | 相同的模型品質、更低的延遲、更高的成本       |
| **較低的努力等級** | 較少的思考時間、更快的回應、複雜任務上可能品質較低 |

您可以結合兩者：在直接任務上使用快速模式搭配較低的[努力等級](/zh-TW/model-config#adjust-effort-level)以獲得最大速度。

## 要求

快速模式需要以下所有條件：

* **第三方雲端提供商上不可用**：快速模式在 Amazon Bedrock、Google Vertex AI 或 Microsoft Azure Foundry 上不可用。快速模式可透過 Anthropic Console API 和使用額外使用的 Claude 訂閱方案取得。
* **啟用額外使用**：您的帳戶必須啟用額外使用，這允許超出您方案包含使用量的計費。對於個人帳戶，在您的 [Console 計費設定](https://platform.claude.com/settings/organization/billing)中啟用此功能。對於 Teams 和 Enterprise，管理員必須為組織啟用額外使用。

<Note>
  快速模式使用直接計費到額外使用，即使您的方案上還有剩餘使用量。這意味著快速模式 token 不計入您方案的包含使用量，並從第一個 token 開始按快速模式費率計費。
</Note>

* **Teams 和 Enterprise 的管理員啟用**：快速模式預設對 Teams 和 Enterprise 組織禁用。管理員必須明確[啟用快速模式](#enable-fast-mode-for-your-organization)，使用者才能存取它。

<Note>
  如果您的管理員尚未為您的組織啟用快速模式，`/fast` 命令將顯示「Fast mode has been disabled by your organization.」
</Note>

### 為您的組織啟用快速模式

管理員可以在以下位置啟用快速模式：

* **Console**（API 客戶）：[Claude Code 偏好設定](https://platform.claude.com/claude-code/preferences)
* **Claude AI**（Teams 和 Enterprise）：[管理員設定 > Claude Code](https://claude.ai/admin-settings/claude-code)

另一個完全禁用快速模式的選項是設定 `CLAUDE_CODE_DISABLE_FAST_MODE=1`。詳見[環境變數](/zh-TW/env-vars)。

### 要求每個工作階段選擇加入

預設情況下，快速模式在工作階段之間保持：如果使用者啟用快速模式，它在未來工作階段中保持開啟。[Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) 或 [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) 方案上的管理員可以透過在[受管設定](/zh-TW/settings#settings-files)或[伺服器受管設定](/zh-TW/server-managed-settings)中將 `fastModePerSessionOptIn` 設定為 `true` 來防止這種情況。這會導致每個工作階段以快速模式關閉開始，要求使用者使用 `/fast` 明確啟用它。

```json  theme={null}
{
  "fastModePerSessionOptIn": true
}
```

這對於控制執行多個並行工作階段的使用者的組織成本很有用。使用者在需要速度時仍可以使用 `/fast` 啟用快速模式，但它在每個新工作階段開始時重設。使用者的快速模式偏好設定仍會保存，因此移除此設定會還原預設的持久行為。

## 處理速率限制

快速模式與標準 Opus 4.6 有不同的速率限制。當您達到快速模式速率限制或用完額外使用額度時：

1. 快速模式自動回退到標準 Opus 4.6
2. `↯` 圖示變灰以指示冷卻
3. 您以標準速度和定價繼續工作
4. 冷卻期過期時，快速模式自動重新啟用

要手動禁用快速模式而不是等待冷卻，請再次執行 `/fast`。

## 研究預覽

快速模式是研究預覽功能。這意味著：

* 該功能可能會根據反饋而改變
* 可用性和定價可能會改變
* 底層 API 配置可能會演變

透過您通常的 Anthropic 支援管道報告問題或反饋。

## 另請參閱

* [模型配置](/zh-TW/model-config)：切換模型和調整努力等級
* [有效管理成本](/zh-TW/costs)：追蹤 token 使用量並降低成本
* [狀態行配置](/zh-TW/statusline)：顯示模型和上下文資訊
